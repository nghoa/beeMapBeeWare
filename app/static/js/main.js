"use strict";

/** Leaflet map object */
let map = undefined;
/** current latlng that was clicked on map */
let currentLocation = undefined;
/** all markers on map except for the one user has possibly created */
let markers = [];
/** most recent created marker */
let currentMarker = []

window.onload = () => {
    initMap();
    map.on("click", addPopUp);

    // testin the putting the locations to the map
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

    let name = document.getElementById("name").value;
    let latitude = document.getElementById("latitude").value;
    let longitude = document.getElementById("longitude").value;

    const formData = new FormData();
    formData.append("name", name);
    formData.append("latitude", latitude);
    formData.append("longitude", longitude);

    fetch("/save", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        handleSaveErrors(data)
        getLocations();
    })
    .catch(e => console.error(e));
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
 */
function handleSaveErrors(data) {
    for (let field of ["latitude", "longitude", "name"]) {
        let div = document.getElementById(field).parentElement;
        let errorDiv = div.querySelector("div");
        if (field in data) {
            let fieldErrors = data[field].join(" ");
            errorDiv.textContent = fieldErrors;
        }    
        else {
            errorDiv.textContent = "";
        }
    }
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
    
    let message = `Chosen location<br />lat: ${location.lat} lon: ${location.lng}<br /><button onclick="togglePanel()">Choose location</button>`;

    currentMarker.addTo(map)
        .bindPopup(message)
        .openPopup();

    //put information to form
    let latitude = location.lat;
    let longitude = location.lng;
    document.getElementById("latitude").value = latitude;
    document.getElementById("longitude").value = longitude;

    currentLocation = location;
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

    //transform fetched data to markers
    markers = data.map(element => {
        return L.marker([element["latitude"], element["longitude"]])
    })

    //add markers to map
    //add popup
    markers.forEach(marker => {
        marker.addTo(map)
        let latlng = marker.getLatLng();
        let message = `Chosen location<br />lat: ${latlng.lat} lon: ${latlng.lng}<br />`;
        marker.bindPopup(message);
    });

    //show popup with information about selected marker
    markers.forEach(marker => {
        marker.on("click", e => {
            //hide panel if shown because user can't modify existing suggestions
            document.getElementById("panel").classList.add("hidden");

            if (currentMarker) {
                map.removeLayer(currentMarker);
                currentMarker = undefined;
            }

            marker.openPopup();
        })
    })

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