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

    let data = {
        "name": name,
        "latitude": latitude,
        "longitude": longitude
    }

    fetch("/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
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
            errorDiv.textContent = data[field];
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
    let location = e.latlng;
    let popup = L.popup();
    //let message = `Valittu sijainti<br />${location.toString()}<br /><a href="#infoform">Valitse</a>`;
    let message = `Chosen location<br />${"lat: " + location.lat + " lon: " + location.lng}<br /><button onclick="togglePanel()">Choose location</button>`;
    popup
        .setLatLng(location)
        .setContent(message)
        .openOn(map);

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
    if (currentLocation) {
        map.panTo(currentLocation);
    }
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

    // show a marker on the map
    //L.marker({lon: 25.72088, lat: 62.24147}).bindPopup('Jyväskylä').addTo(map);
}

/**
 * Put the fetched markers to the map
 */
function put_markers_to_map(data, textStatus, request) {
    const locations = data.map(L.marker)

    // Bind mouse click to show popup that displays clicked location's data
    locations.forEach(marker => {
        marker.bindPopup("Location: " + marker.getLatLng().toString()).openPopup();

        marker.on("click", event => {
            event.target.openPopup();
        })
    });

    let locations_layer = L.layerGroup(locations);
    locations_layer.addTo(map);
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