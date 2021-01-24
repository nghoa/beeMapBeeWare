"use strict";

/** Leaflet map object */
let map = undefined;
/** current latlng that was clicked on map */
let currentLocation = undefined;

window.onload = () => {
    initMap();
    map.on("click", addPopUp);

    // testin the putting the locations to the map
    getLocations();

    document.getElementById("userForm").addEventListener("submit", handleFormSubmit);
}

/**
 *  send form asynchronously to server 
 */
function handleFormSubmit(e) {
    //don't send form normally
    e.preventDefault();

    let location = document.getElementById("location").value;
    let name = document.getElementById("name").value;

    console.log(location, name)

    let data = {
        "location": location,
        "name": name
    }
    fetch("/map/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        let errors = response.json();
        //TODO: errors
        console.log(errors);
    })
    .catch(e => console.error(e))
}


/**
 * Adds a popup where user clicks
 * save the location
 * adds location to form
 * @param e event
*/
function addPopUp(e) {
    let location = e.latlng;
    let popup = L.popup();
    //let message = `Valittu sijainti<br />${location.toString()}<br /><a href="#infoform">Valitse</a>`;
    let message = `Chosen location<br />${location.toString()}<br /><button onclick="togglePanel()">Choose location</button>`;
    popup
        .setLatLng(location)
        .setContent(message)
        .openOn(map);

    let locationInput = document.getElementById("location");
    locationInput.value = location.toString();

    currentLocation = location;
}

/** 
 * Shows form panel
*/
function togglePanel() {
    if (currentLocation) {
        map.panTo(currentLocation);
    }
    let panel = document.getElementById("panel");
    panel.classList.toggle("hidden");


}


/**
 * Adds map to document
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

    // show a marker on the map
    //L.marker({lon: 25.72088, lat: 62.24147}).bindPopup('Jyväskylä').addTo(map);
}

/**
 * Put the fetched markers to the map
 */
function put_markers_to_map(data, textStatus, request) {

    let locations = [];

    for (let i = 0; i < data.length; i++) {
        locations.push(L.marker(data[i]));
    }

    let locations_layer = L.layerGroup(locations);
    locations_layer.addTo(map);

}

/**
 * Get the locations
 */
function getLocations() {
    $.ajax({
        async: true,
        url: "/map/locations",
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
}