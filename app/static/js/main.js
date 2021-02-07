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

let insideFinland = false;

let geoFinland = {"type":"Feature","properties":null,"geometry":{"type":"MultiPolygon","coordinates":[[[[19.0832038920896,60.1916933464304],[19.2443186170417,60.0808986613783],[19.3252435673695,60.0248779268473],[19.4236525602077,59.9564182506396],[19.6582850040363,59.7916940455435],[19.9406313857353,59.5950606354975],[19.9962934908449,59.59059086412],[20.2843073361168,59.4660821029671],[20.3264211148615,59.4554241912066],[20.3731891716823,59.4558202712195],[20.7608424869772,59.5324822484344],[21.179719972206,59.4992051495534],[21.4966655585993,59.4756414613716],[22.0980873617657,59.5010738787032],[22.3965363353683,59.5130927645348],[22.6589214998962,59.6110037650124],[22.8633528313763,59.6350789238945],[23.2153471341435,59.6511875571346],[23.3580604280772,59.6570911806248],[23.9863717006538,59.7516949387957],[24.2815893611734,59.7915662113389],[24.4906032847468,59.8181577680512],[24.8316636335145,59.9010872051575],[24.9422989811848,59.922489218421],[25.1585606142025,59.9424534139897],[25.3292851724598,59.9371033746756],[25.5826792792856,59.9281971866356],[26.0173036531947,59.976789718272],[26.0750614512953,60.0140563179977],[26.2712971313679,60.0446926332515],[26.4919512959522,60.1535138306201],[26.6563950430497,60.1713275416351],[26.8753340646249,60.2003359585126],[27.2931182227401,60.2002119721681],[27.4664461370577,60.2294045281442],[27.6495306369658,60.3449221494737],[27.7258231273361,60.3916275638843],[27.6869203723197,60.4335723697176],[27.7479498085635,60.4511708940291],[27.7744098423473,60.5335732522288],[27.8887416813714,60.6129423469304],[27.9912825272202,60.6689848920987],[28.5246048315027,60.9571045659096],[28.6550013330735,60.9494993422551],[28.7766485390011,61.0792549641005],[28.8506338361851,61.129653097596],[28.9537125118911,61.1506734759461],[29.0219658685355,61.1884893956044],[29.0842641391906,61.210434721122],[29.2448290869186,61.2706899428937],[29.4443052502288,61.424473719726],[29.5321377788836,61.4909053598118],[29.64523457729,61.5201549447776],[30.1439574360617,61.8522422147816],[30.483086874011,62.0638439427301],[30.6694611621693,62.1939151674908],[30.7891820025584,62.2508028426824],[30.9196436804062,62.3090607832639],[30.9667910437678,62.3379709938531],[31.0935218477168,62.4166116682057],[31.1695193437691,62.467799297791],[31.2266272982478,62.5035563481379],[31.3731571575361,62.6497217056697],[31.4392088181993,62.7848829062527],[31.5867058506984,62.9087069617745],[31.4629865988883,63.024245724113],[31.2721272015566,63.1076277654002],[31.2382471949049,63.1951328920411],[30.9344437151197,63.3554524001032],[30.4840102655112,63.4667029328009],[29.9718935859892,63.7571653280208],[30.2604141745607,63.8220093328828],[30.331780422378,63.9127525281393],[30.4985994569077,64.0206879789222],[30.553557623577,64.1016864218741],[30.5483286358326,64.1367034814114],[30.4886680336493,64.1801660964309],[30.482440762727,64.2623262984778],[30.3882763861512,64.2690690758481],[30.2777566525682,64.3311756840786],[30.083057096991,64.3767146795269],[30.0280282441984,64.4896965361313],[29.9897717579612,64.5871446242342],[30.1301111661279,64.6347281880408],[30.0413968313075,64.7411930017949],[30.1009069834387,64.7612234540869],[30.0457846768682,64.795613791862],[29.7396284232142,64.7897838370828],[29.6618627573805,64.8525860486766],[29.6109945637451,64.9273111934954],[29.626976362782,65.0605966778966],[29.8968593305052,65.1051402845749],[29.8193338136238,65.1442788880306],[29.8856599339199,65.2062960739117],[29.6340017685677,65.2315851175702],[29.6017868746672,65.2599324054876],[29.7465810250473,65.3474016419722],[29.754713953508,65.4973656893719],[29.8639044763928,65.5604441277604],[29.7218695971293,65.6370848398994],[30.0171126303968,65.696479185386],[30.1384672249255,65.6686789192909],[30.1340741283328,65.6997241360024],[30.0755769118911,65.8810444035062],[29.9232900056247,66.1271435136028],[29.6969966467514,66.2719433059059],[29.5729298173824,66.4328532043208],[29.3611413401472,66.6388597571845],[29.1295119677268,66.7891705331989],[29.0658439253869,66.8514292673851],[29.0336371763302,66.9421322659691],[29.1846990397146,67.0652909571018],[29.4911381806536,67.2591639266897],[29.5225548279479,67.3099040328582],[29.6439452073872,67.3357543016877],[29.6981604953192,67.3877383359706],[29.9302245035771,67.5225242385888],[30.0170436211245,67.673553259513],[29.6594050839051,67.8029592451858],[29.327089313933,68.0745414834979],[28.6461525992282,68.1963035523995],[28.478982094947,68.4661906694009],[28.4339319008515,68.5396716695169],[28.7064081747953,68.7322376708507],[28.8007858917525,68.8692846964368],[28.4680149348274,68.8854350965329],[28.4157879993063,68.9154507724599],[28.9292920759074,69.0519153468213],[28.8054298041895,69.1111555485437],[28.8315406595443,69.2243606450356],[29.189109385573,69.3826059093611],[29.3364967864817,69.4783220327101],[29.1339034514315,69.6953405418356],[28.3304761175685,69.8491925382525],[28.3452680472709,69.8808321199645],[28.1607127695676,69.9209936834823],[27.984285246604,70.0139706640238],[27.9593814143109,70.0920997296961],[27.7601103040558,70.0716960364157],[27.6124553923087,70.0745602518489],[27.5259867917309,70.0234637958038],[27.4092810315971,70.0123186747974],[27.288789307435,69.984517750992],[27.3006654264487,69.9547326134081],[27.0418132097363,69.9108218184226],[26.8486723062176,69.9601955357023],[26.4677073478562,69.940416210841],[26.3850223836116,69.8548691625991],[26.2586463819609,69.8091863484047],[26.1476897877975,69.7490449912711],[26.0154224730786,69.7198696261152],[25.8914907306645,69.6655028742289],[25.9765765392004,69.6102428836166],[25.8582085472379,69.5417626919496],[25.8504235697772,69.4971990743518],[25.8208455960971,69.4346832003748],[25.8466476337963,69.3938351127031],[25.7584057939074,69.3318658622986],[25.7020398981764,69.2536623013953],[25.738374212966,69.1475801004183],[25.7772654692242,69.0179098314686],[25.6534780699752,68.9070229927112],[25.5881394888163,68.883259690617],[25.4748027523225,68.904516799283],[25.243288425554,68.8414235337414],[25.1422035269685,68.7872303484266],[25.116388980916,68.6395883305666],[24.9169239793072,68.6052466227186],[24.9031657817504,68.5545918308583],[24.7834245817865,68.6362346150976],[24.5878922450566,68.6826316038492],[24.2509647827582,68.7271320690877],[24.1529623055335,68.7535910430354],[24.075591585759,68.7799668345721],[23.9914008786302,68.8209813045671],[23.8714607673088,68.8365191845573],[23.7753913889281,68.8188511193203],[23.673520205748,68.7055213730138],[23.4406356578474,68.6921634916774],[23.1675822870621,68.6285189258868],[23.0459520446681,68.6893433177216],[22.8008240391557,68.6875480149318],[22.5353893252795,68.7445119668787],[22.3745218970771,68.7166665655402],[22.3407806481006,68.8272248947003],[22.1757623959589,68.9563243008063],[21.6270863244425,69.2765883025064],[21.2788207816323,69.3118840153646],[21.0940221221219,69.2595471443146],[21.0081980650981,69.2216503332088],[20.9867202308417,69.1932767867613],[21.1086751240358,69.1039291229572],[21.0575439123718,69.0362896679019],[20.7173223261905,69.1197904927556],[20.552327775899,69.060076309098],[20.776311473738,69.0322011332034],[20.9252230782975,68.9562894775521],[20.8447994810384,68.9358820869022],[20.9046188966139,68.8929886355438],[20.9990590312867,68.8961504547797],[21.2084765352059,68.8222375435045],[21.2990835422031,68.7624026022946],[21.3838588082339,68.7648523411152],[21.4203140202443,68.6958769892414],[21.623065944988,68.6609161453619],[21.7053428281711,68.6261634379548],[21.7048399962544,68.594751727306],[21.8903219324874,68.5838906066336],[21.9874391747765,68.5316319165396],[22.0432474501604,68.479665831758],[22.3468346693919,68.4822284078827],[22.3417595866246,68.4448739361086],[22.4321604228387,68.4649127729264],[22.5501384047218,68.4359163542084],[22.6368345363258,68.4239909978638],[22.7179879175657,68.3966832914631],[22.8264362947994,68.3874578480811],[22.8997096848469,68.341389004971],[23.0593597815882,68.3016376457989],[23.144072110671,68.2462989314706],[23.1523892811278,68.1367293828421],[23.2866982181351,68.154273008972],[23.3879202144534,68.0481348524659],[23.5500487685173,67.9951584622748],[23.6646120796915,67.9414539133645],[23.4776191884126,67.8425778371791],[23.4870987317386,67.6984014665877],[23.5542168796901,67.6175838909503],[23.3937107600774,67.4850921540259],[23.4948552318844,67.4466142003969],[23.5404899056752,67.4610448947765],[23.7645816646832,67.4282143153293],[23.7307020685931,67.3864284277335],[23.7558288184239,67.3322440419558],[23.7297366191289,67.288339433988],[23.575282493257,67.2683640912552],[23.546260358293,67.2251879321749],[23.595865390087,67.207818289415],[23.5544754004677,67.1674657992215],[23.7843836068018,66.996929396033],[23.9953484035872,66.8212000985846],[23.8795749787353,66.7632435724979],[23.8989576765259,66.7151111438749],[23.8782707216572,66.5829691847538],[23.7970800987117,66.5211168501924],[23.6501196802631,66.4548309473157],[23.6714181894011,66.3750133501287],[23.6457902995432,66.3015587596059],[23.7276060466661,66.1953798388378],[23.8918620311265,66.1676701925873],[23.9451880659081,66.0858529996431],[24.0373585081278,65.9922813495124],[24.1531711620704,65.8625786209432],[24.1377965691221,65.7793894820858],[24.1725594671771,65.699823770652],[24.159751002144,65.6128100204238],[24.1355167268353,65.5070780853278],[24.1501646966022,65.337287903793],[24.1545076708539,65.2924805347547],[24.1374948169974,65.2416484128856],[24.1149334366251,65.1739425977789],[24.0838254755623,65.081763181392],[24.0385990841975,65.0079488217685],[23.9434097538695,64.8547784586763],[23.8788206723745,64.7497128126739],[23.8358002286007,64.6654742396781],[23.6907086475414,64.6287395624253],[23.2351850475829,64.5110709517687],[23.1400539337433,64.483466464689],[23.0553807107393,64.4408818617709],[23.0031813963994,64.3916375825792],[22.9846297290188,64.3432888534135],[22.9611529304937,64.2200973458136],[22.7789004927065,64.1789731326456],[22.5729578340592,64.1319925796203],[22.455042390262,64.0937936569457],[22.3678215816198,64.0582688602895],[22.287878839137,64.0093855601079],[22.2125853104266,63.9509399715495],[22.0965039341615,63.8329942466167],[21.9787401367701,63.7599495846743],[21.8845873650511,63.7012124784773],[21.5994752111309,63.6702367832752],[21.5065683402704,63.6661126189112],[21.3605875508658,63.6289853324518],[20.9415672965784,63.5194251476728],[20.696319314382,63.4828669865965],[20.3987210815395,63.3308724915391],[20.3101785393382,63.267646647997],[20.1658189049327,63.1648513731483],[20.3001782244374,62.9300166464754],[20.4046129067101,62.7430915949995],[20.4660316785625,62.6561886573143],[20.6618640183249,62.373120195485],[20.6917128170462,62.2974971043024],[20.7110451805701,62.247805954535],[20.728112682294,62.2037869635282],[20.8291621122992,61.9216718820088],[20.8888853268441,61.6999278123364],[20.9036963630165,61.6465239705554],[20.8745591062254,61.5301831719775],[20.8296168994472,61.3526539486712],[20.8120723831696,61.2848757170443],[20.7731306640216,61.1334820093468],[20.7714473222996,61.1269082829326],[20.4375585336477,60.9018089858616],[20.377530566665,60.8766383898234],[20.2017917127625,60.802570912604],[20.1061024534451,60.7620036691538],[20.0251620072178,60.7275577553442],[19.7978434922093,60.7083454501912],[19.5984516453758,60.6895179641144],[19.4732340569849,60.6657890640015],[19.2201999080555,60.61151374359],[19.1611665609226,60.3749195656841],[19.0832038920896,60.1916933464304]]]]}}

window.onload = () => {
    initMap();
    map.on("click", addPopUp);

    // Finland's borders
    let finlandLayer = L.geoJSON(geoFinland).addTo(map);
    function onMapClick(e) {
        insideFinland = true;
    }
    finlandLayer.on('click', onMapClick);
    
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

    // Only locations inside Finland's borders are allowed
    if (insideFinland == false) {
        let popup = L.popup()
        .setLatLng(location)
        .setContent('<p>Outside Finland!.</p>') // TODO: Add translation
        .openOn(map);
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