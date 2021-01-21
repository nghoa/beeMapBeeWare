"use strict";

/** Leaflet map object */
let map = undefined;

window.onload = () => {
    initMap();
    map.on("click", showPanel);
}

/**
 * Adds a popup where user clicks
 * 
 * @param e event
*/
function addPopUp(e) {
    console.log("addPopUp");
    let location = e.latlng;
    let popup = L.popup();
    //let message = `Valittu sijainti<br />${location.toString()}<br /><a href="#infoform">Valitse</a>`;
    let message = `Chosen location<br />${location.toString()}<br /><button onclick="showLeftPanel">Choose location</button>`;
    popup
        .setLatLng(location)
        .setContent(message)
        .openOn(map);
}

/** 
Shows form on left side of map
adds location to form
@param e event
*/
function showPanel(e) {
    let location = e.latlng;
    let locationInput = document.getElementById("location");
    locationInput.value = location.toString();

    let panel = document.getElementById("panel");
    panel.classList.toggle("hidden");
}

/* 
Hides form panel
*/
function hidePanel(e) {
    let panel = document.getElementById("panel");
    panel.classList.toggle("hidden");
}

/**
 * Adds map to document
*/
function initMap() {
    // initialize Leaflet
    map = L.map('map').setView({ lon: 25.72088, lat: 62.24147 }, 6);

    // add the OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(map);

    // show the scale bar on the lower left corner
    L.control.scale().addTo(map);

    // show a marker on the map
    //L.marker({lon: 25.72088, lat: 62.24147}).bindPopup('Jyväskylä').addTo(map);
}