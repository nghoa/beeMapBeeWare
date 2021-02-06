"use strict";

/** Leaflet map object */
let map = undefined;
/** current latlng that was clicked on map */
let currentLocation = undefined;
/** all markers on map except for the one user has possibly created */
let markers = [];
/** most recent created marker */
let currentMarker = []

/** form fields */
const formFields = ["firstname", "lastname", "email", "latitude", "longitude"]

window.onload = () => {
    initMap();
    map.on("click", addPopUp);

    // put the markers from the datastore into the map
    getLocations();

    document.getElementById("userForm").addEventListener("submit", handleFormSubmit);

    document.getElementById("hide-button").addEventListener("click", togglePanel)

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
    const existingMarker = isThereAlreadyMarker(latitude, longitude);

    if (existingMarker) {
        console.log("a marker already exists there!");
        let content = `<p>${requireTranslation("A marker already exists close by. Please, pick another location.")}</p>`
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
    } catch(err) {
        return null;
    }

}


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
 * removes element's children
 */
function removeChildren(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
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
    currentMarker = L.marker(location);

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
    button.addEventListener("click", togglePanel)

    div.appendChild(button);
    return div;
}

/**
 * Get translation for given text
 */
function requireTranslation(name) {
    /* translationData is defined in html file */
    return translationData[name];
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
 * Put the fetched markers to the map
 */
function put_markers_to_map(data, textStatus, request) {
    //remove old markers
    markers.forEach(marker => map.removeLayer(marker))

    markers = []
    for (let element of data) {
        //transform fetched data to markers
        let marker = L.marker([element["latitude"], element["longitude"]]);

        // add marker to the marker collection (array)
        markers.push(marker);

        //add markers to map
        marker.addTo(map)

        //add popup
        let id = element["id"];
        let content = createPopupContent(marker, id, element["confirmed"]);
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
 * Content showing user information about selected suggestion
 * @param marker: leaflet marker object
 * @param id: suggestion id
 * @param confirmed: boolean
 * @return HTMLElement
*/
function createPopupContent(marker, id, confirmed) {
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

    let button = document.createElement("button");
    button.textContent = requireTranslation("Delete");
    button.addEventListener("click", e => {
        deleteLocation(marker, id);
    });

    div.appendChild(button);

    return div;
}

/**
 * Delete suggestion 
 * delete marker from map
 * @param marker leaflet marker object to delete
 * @param id id of suggestion to delete
 */
function deleteLocation(marker, id) {
    map.removeLayer(marker);
    fetch(`/delete/${id}`, {
        method: "GET"
    })
        .then(res => res.text())
        .then(text => console.log(text))
        .catch(e => console.error(e))
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
        success: put_markers_to_map,
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