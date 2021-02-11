"use strict";

/** Leaflet map object */
let map = undefined;
/** current latlng that was clicked on map */
let currentLocation = undefined;

/** form fields */
const formFields = ["firstname", "lastname", "email", "latitude", "longitude"]

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
    function put_markers_to_map(data, textStatus, request) {
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
    function addPopUp(e) {

        //remove old marker
        if (currentMarker) {
            map.removeLayer(currentMarker);
        }
        let location = e.latlng;
        currentMarker = createMarker(location, false)

        // Only locations inside Finland's borders are allowed
        if (insideFinland == false) {
            let content = `<p>${requireTranslation("Only locations inside borders of Finland are allowed.")}</p>`;
            let popup = L.popup()
                .setLatLng(location)
                .setContent(content)
                .openOn(map);
            FORM.clearForm();
            currentMarker = undefined;
            closePanel();
            
            return;
        }

        let content = createPopupContentNew(currentMarker);
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
            return markers.find(m => m.getLatLng().equals(marker.getLatLng(), 0.00004));
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
        formFields.forEach(field => document.getElementById(field).value = "");
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

        fetch("/save", {
            method: "POST",
            body: formData,
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
}



/** 
 * Content showing user information about selected suggestion
 * @param marker: leaflet marker object
 * @param id: suggestion id
 * @param confirmed: boolean
 * @return HTMLElement
*/
function createPopupContent(marker, confirmed) {
    let latlng = marker.getLatLng();

    let div = document.createElement("div");
    div.textContent = requireTranslation("Chosen location");
    let p = document.createElement("p");
    p.textContent = `${requireTranslation("Latitude")}: ${latlng.lat}`;

    let p2 = document.createElement("p");
    p2.textContent = `${requireTranslation("Longitude")}: ${latlng.lng}`;

    div.appendChild(p);
    div.appendChild(p2);

    if (confirmed) {
        let p3 = document.createElement("p");
        p3.textContent = requireTranslation("Confirmed");
        div.appendChild(p3);
    }

    return div;
}

/** 
 * Content showing user information about created marker
 * @param marker: leaflet marker object
 * @return HTMLElement
*/
function createPopupContentNew(marker) {
    let latlng = marker.getLatLng();

    let div = document.createElement("div");
    div.textContent = requireTranslation("Chosen location");
    let p = document.createElement("p");
    p.textContent = `${requireTranslation("Latitude")}: ${latlng.lat}`;

    let p2 = document.createElement("p");
    p2.textContent = `${requireTranslation("Longitude")}: ${latlng.lng}`;

    div.appendChild(p);
    div.appendChild(p2);

    let button = document.createElement("button");
    button.textContent = requireTranslation("Choose")
    button.addEventListener("click", openPanel)

    div.appendChild(button);
    return div;
}

function createPopupContentError() {
    return `<p>${requireTranslation("A marker already exists close by. Please, pick another location.")}</p>`
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