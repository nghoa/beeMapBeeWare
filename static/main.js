"use strict";

var MAP = undefined;

window.onload = () => {
    MAP = createMap();
    MAP.on("click", addPopUp);

}

/* 
adds a popup where user clicks
*/
function addPopUp(e) {
    let location = e.latlng;
    let popup = L.popup();
    let message = `Valittu sijainti<br />${location.toString()}<br /><a href="#infoform">Valitse</a>`;
    popup
        .setLatLng(location)
        .setContent(message)
        .openOn(MAP);
}

function createMap() {
    // initialize Leaflet
    const map = L.map('map').setView({lon: 25.72088, lat: 62.24147}, 6);

    // add the OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(map);

    // show the scale bar on the lower left corner
    L.control.scale().addTo(map);

    // show a marker on the map
    //L.marker({lon: 25.72088, lat: 62.24147}).bindPopup('Jyväskylä').addTo(map);

    return map;
}