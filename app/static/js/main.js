"use strict";

/** Leaflet map object */
let map = undefined;
/** current latlng that was clicked on map */
let currentLocation = undefined;

var geocodeService = undefined;

/** How many decimals are displayed to user on the latitude and longitude values  */
const coordinateDecimals = 6;

/** form fields */
const formFields = ["firstname", "lastname", "email", "latitude", "longitude", "csrf_token", "suggestee", "suggesteeType"]

let insideFinland = false;

/**
 * namespace for marker related functionality
 */
var MARKERS = (function() {
    /** all markers on map except for the one user has possibly created */
    let markers = [];
    /** most recent created marker */
    let currentMarker = undefined;

    /**
     * Put the fetched markers to the map
     */
    async function put_markers_to_map(data, textStatus, request) {
        //remove old markers
        markers.forEach(marker => map.removeLayer(marker["marker"]))

        markers = []
        for (let element of data) {
            //transform fetched data to markers
            let lat = element["latitude"];
            let lng = element["longitude"];
            let confirmed = element["confirmed"]
            let marker = createMarker(L.latLng(lat, lng), confirmed);

            // add marker to the marker collection (array)
            markers.push({
                "marker": marker,
                "confirmed": confirmed
            });

            //add markers to map
            marker.addTo(map)

            //add popup
            let content = createPopupContent(marker, element["confirmed"]);
            marker.bindPopup(content);

            //show popup with information about selected marker
            marker.on("click", e => {
                //hide panel if shown because user can't modify existing suggestions
                document.getElementById("panel").classList.add("hidden");

                if (currentMarker) {
                    map.removeLayer(currentMarker);
                    currentMarker = undefined;
                }

                marker.openPopup();
            })
        }
    }

    /**
     * Shows some of markers based on selected filter
     */
    function createFiltering() {
        let select = document.getElementById("suggestion-select");
        select.addEventListener("change", (e) => {
            markers.forEach(marker => map.removeLayer(marker["marker"]));
            switch (select.value) {
                case "All":
                    //remove all first so there are not dublicates
                    markers.forEach(marker => {
                        if (marker["confirmed"]) {
                            L.Icon.Default.prototype.options.className = "icon-confirmed"
                        } else {
                            L.Icon.Default.prototype.options.className = "icon-not-confirmed"
                        }
                        marker["marker"].addTo(map)
                    });
                    break;
                case "Confirmed":
                    markers.filter((marker, index, array) => {
                        return marker["confirmed"]
                    }).forEach(marker => {
                        L.Icon.Default.prototype.options.className = "icon-confirmed"
                        marker["marker"].addTo(map)
                    });
                    break;
                case "Unconfirmed":
                    markers.filter((marker, index, array) => {
                        return !marker["confirmed"]
                    }).forEach(marker => {
                        L.Icon.Default.prototype.options.className = "icon-not-confirmed"
                        marker["marker"].addTo(map)
                    })
                    break;
                default:
                    console.err("something else filetering")
                    break;
            }        
        });
    }


    function createFinlandLayer() {
        // style of Finland layer
        var exteriorStyle = {
            "color": "#ffffff",
            "weight": 0,
            "fillOpacity": 0.0
        };
        // Finland's borders
        let finlandLayer = L.geoJSON(geoFinland, { style: exteriorStyle }).addTo(map)
        
        function onMapClick(e) {
            insideFinland = true;
        }
        finlandLayer.on('click', onMapClick);
    }

    /**
     * Adds a popup where user clicks
     * save the location
     * adds location to form
     * @param e event
    */
    async function addPopUp(e) {

        //remove old marker
        if (currentMarker) {
            map.removeLayer(currentMarker);
        }
        let location = e.latlng;
        currentMarker = createMarker(location, false)

        // Only locations inside Finland's borders are allowed
        if (insideFinland == false) {
            let content = `<p><i class="fas fa-ban fa-lg" style="color: red;"></i><br>${requireTranslation("Only locations inside borders of Finland are allowed.")}</p>`;
            let popup = L.popup()
                .setLatLng(location)
                .setContent(content)
                .openOn(map);
            FORM.clearForm();
            currentMarker = undefined;
            closePanel();
            
            return;
        }

        let content = await createPopupContentNew(currentMarker);
        currentMarker.addTo(map)
            .bindPopup(content)
            .openPopup();

        //put information to form
        let latitude = location.lat;
        let longitude = location.lng;
        document.getElementById("latitude").value = latitude;
        document.getElementById("longitude").value = longitude;

        currentLocation = location;

        insideFinland = false;
    }

    /** 
     * Create markers with assigned css class
     * @param latlng L.latLng object
     * @param confirmed Boolean
     * @return L.marker object
     */
    function createMarker(latlng, confirmed) {
        if (confirmed) {
            L.Icon.Default.prototype.options.className = "icon-confirmed"
        }
        else {
            L.Icon.Default.prototype.options.className = "icon-not-confirmed"
        }
        return L.marker(latlng);
    }

    /**
     * Check if a marker (location recommendation) already exists on given location within some margin
     * (10 or so meters). If lat and lon are not floats returns null
     *
     * @return truthy value if exists else falsy value
     */
    function isThereAlreadyMarker(lat, lon) {
        try {
            const marker = L.marker(L.latLng(lat, lon));
            return markers.find(m => m.getLatLng().equals(marker.getLatLng(), 0.0004));
        } catch (err) {
            return null;
        }

    }

    return {
        createMarker: createMarker,
        isThereAlreadyMarker: isThereAlreadyMarker,
        createFinlandLayer: createFinlandLayer,
        addPopUp: addPopUp,
        put_markers_to_map: put_markers_to_map,
        createFiltering: createFiltering
    }
})();

/**
 * namespace for form functionality
 */
var FORM = (function() {
    /**
     * Show success message
     * clear form 
     */
    function handleSuccess() {
        let feedback = document.getElementById("feedback");
        feedback.textContent = requireTranslation("Suggestion was saved succesfully")
        //clear message after a while
        setTimeout(() => {
            feedback.textContent = "";
        }, 6000);
        clearForm();
    }

    /** 
     * Clear form fields
    */
    function clearForm() {
        formFields.forEach(field => {
            let element = document.getElementById(field);
            if (element.id != "suggesteeType") {
                element.value = "";
            }
        });
    }


    /** 
     * Add errors to fields
     * removes old ones
     * @return true if form was valid false otherwise
     */
    function handleSaveErrors(data) {
        let valid = true;

        for (let field of formFields) {
            let div = document.getElementById(field).parentElement;
            let errorDiv = div.querySelector("div");
            if (field in data) {
                valid = false;
                let fieldErrors = data[field].join(" ");
                errorDiv.textContent = fieldErrors;
            } else {
                errorDiv.textContent = "";
            }
        }
        return valid;
    }

    /**
     *  send form asynchronously to server 
     */
    function handleFormSubmit(e) {
        //don't send form normally
        e.preventDefault();

        const formData = new FormData();
        for (let field of formFields) {
            let value = document.getElementById(field).value
            formData.append(field, value)
        }
        let latitude = document.getElementById("latitude").value;
        let longitude = document.getElementById("longitude").value;
        const existingMarker = MARKERS.isThereAlreadyMarker(latitude, longitude);

        if (existingMarker) {
            console.log("a marker already exists there!");
            let content = createPopupContentError();
            L.popup()
                .setLatLng(existingMarker.getLatLng())
                .setContent(content)
                .openOn(map);

            return; // just return and don't save duplicate marker
        }

        let headers = new Headers();
        let csrf_token =  document.getElementById("csrf_token").value
        headers.append("X-CSRFToken", csrf_token)

        fetch("/save", {
            method: "POST",
            body: formData,
            headers: headers
        })
            .then(response => response.json())
            .then(data => {
                let valid = handleSaveErrors(data)
                if (valid) {
                    handleSuccess();
                }
                getLocations();
            })
            .catch(e => console.error(e));
    }
    return {
        handleFormSubmit: handleFormSubmit,
        clearForm: clearForm
    }
})()

window.onload = () => {
    initMap();
    map.on("click", MARKERS.addPopUp);

    MARKERS.createFinlandLayer();
    MARKERS.createFiltering();
    
    // put the markers from the datastore into the map
    getLocations();

    document.getElementById("userForm").addEventListener("submit", FORM.handleFormSubmit);

    document.getElementById("hide-button").addEventListener("click", togglePanel)
    
    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function() {

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");

    });

        
}

/** 
 * Shows panel that contains the location recommendation form.
*/
function togglePanel() {
    //check if anything has been clicked and center map a bit
    if (currentLocation) {
        map.panTo(currentLocation);
    }
    //make panel visible
    let panel = document.getElementById("panel");
    panel.classList.toggle("hidden");
}





/**
 * Get translation for given text
 */
function requireTranslation(name) {
    /* translationData is defined in html file */
    return translationData[name];
}


function closePanel() {
    document.getElementById("panel").classList.add("hidden");
}

function openPanel() {
    //check if anything has been clicked and center map a bit
    if (currentLocation) {
        map.panTo(currentLocation);
    }
    document.getElementById("panel").classList.remove("hidden");
}


/**
 * Adds map and its controls to document
*/
function initMap() {
    // initialize Leaflet
    map = L.map('map', { "zoomControl": false }).setView({ lon: 25.72088, lat: 62.24147 }, 6);
    let control = L.control.zoom({ "position": "topright" })
    map.addControl(control);

    // add the OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(map);

    // show the scale bar on the lower left corner
    L.control.scale({ "imperial": false, "position": "bottomright" }).addTo(map);

    geocodeService = L.esri.Geocoding.geocodeService();
}



/** 
 * Content showing user information about selected suggestion
 * @param marker: leaflet marker object
 * @param id: suggestion id
 * @param confirmed: boolean
 * @return HTMLElement
*/

// already setted markers -> popup description
function createPopupContent(marker, confirmed) {
    let latlng = marker.getLatLng();

    let div = document.createElement("div");
    let title = document.createElement("h1");
    title.textContent = requireTranslation("Chosen location");
    $(title).addClass("title").addClass("is-5");
    let p = document.createElement("p");
    p.textContent = `${requireTranslation("Latitude")}: ${latlng.lat.toFixed(coordinateDecimals)}, ${requireTranslation("Longitude")}: ${latlng.lng.toFixed(coordinateDecimals)}`;
    $(p).addClass("light-font");

    div.appendChild(title);
    div.appendChild(p);

    if (confirmed) {
        let successTag = document.createElement("span");
        $(successTag).addClass("tag").addClass("is-success");
        successTag.textContent = requireTranslation("Confirmed");
        div.appendChild(successTag);
    } else {
        let noSuccessTag = document.createElement("span");
        $(noSuccessTag).addClass("tag").addClass("is-warning");
        noSuccessTag.textContent = requireTranslation("Unconfirmed");
        div.appendChild(noSuccessTag);
    }

    return div;
}

/** 
 * Content showing user information about created marker
 * @param marker: leaflet marker object
 * @return HTMLElement
*/
// popup when clicking new field
async function createPopupContentNew(marker) {
    let latlng = marker.getLatLng();

    // get geocodeObject through Esri
    let geoObject = await reverseGeocoding(latlng);

    let div = document.createElement("div");
    let title = document.createElement("h1");
    title.textContent = requireTranslation("Chosen location");
    $(title).addClass("title").addClass("is-5");

    let addressSpan = document.createElement("span");
    $(addressSpan).addClass("thick-address");
    addressSpan.innerHTML = geoObject.address.Address;

    let citySpan = document.createElement("p");
    citySpan.textContent = geoObject.address.Postal + " " + geoObject.address.City;

    let p = document.createElement("p");
    p.textContent = `${requireTranslation("Latitude")}: ${latlng.lat.toFixed(coordinateDecimals)}, ${requireTranslation("Longitude")}: ${latlng.lng.toFixed(coordinateDecimals)}`;
    $(p).addClass("light-font");

    // Build together div bubble
    div.appendChild(title);
    div.appendChild(addressSpan);
    div.appendChild(citySpan);
    div.appendChild(p);

    let button = document.createElement("button");
    $(button).addClass("button").addClass("is-link").addClass("is-rounded").addClass("is-small");
    button.textContent = requireTranslation("Choose")
    button.addEventListener("click", openPanel)

    div.appendChild(button);
    return div;

}


// Wrapper function for geocodeService
async function reverseGeocoding(latlng) {
    var promise = new Promise((resolve, reject) => {
        geocodeService.reverse().latlng(latlng).run(function (error, result) {
            if (error) {
                console.log(error);
            }
            resolve(result);
        });
    });

    var geocodeObject = await promise;
    return geocodeObject;
}



/**
 * 
 */
function createPopupContentError() {
    const content =
            `<p>
                <i class="fas fa-ban fa-lg" style="color: red;"></i>
                <br>
                ${requireTranslation("A marker already exists close by. Please, pick another location.")}
            </p>`
    return content;

}




/**
 * Get the locations from backend
 */
function getLocations() {
    $.ajax({
        async: true,
        url: "/locations",
        dataType: "json",
        type: "GET",
        success: MARKERS.put_markers_to_map,
        error: ajax_error
    });
}

/**
 * Catch the ajax error
 */
function ajax_error(xhr, status, error) {
    console.log("Error: " + error);
    console.log("Status: " + status);
    console.log(xhr);
    // TODO: display errors to user in a meaningful way
}
