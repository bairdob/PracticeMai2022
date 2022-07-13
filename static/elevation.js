//var1________
let TILE_URL = "https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}";
let map = L.map('llmap').setView([55, 160], 4);;
L.tileLayer(TILE_URL).addTo(map);


var imageUrl = '/static/srtm_N55E160.png';
var errorOverlayUrl = 'https://cdn-icons-png.flaticon.com/512/110/110686.png';
var altText = 'данные на вулканы Камчатки (55-56 с.ш. и 160-161 в.д.)';
var latLngBounds = L.latLngBounds([[55, 160], [56, 161]]);

var imageOverlay = L.imageOverlay(imageUrl, latLngBounds, {
    opacity: 0.8,
    errorOverlayUrl: errorOverlayUrl,
    alt: altText,
    interactive: true
}).addTo(map);

L.rectangle(latLngBounds, {opacity: 0.5}).addTo(map);
map.fitBounds(latLngBounds)

// var2__________
// var map = L.map('llmap', {
//     minZoom: 1,
//     maxZoom: 5.2,
//     center: [0, 0],
//     zoom: 1,
//     crs: L.CRS.Simple
// });
// var w = 3601;
// var h = 3601;
// var url = '/static/srtm_N55E160.png';
// var southWest = map.unproject([ 0, h], map.getMaxZoom()-1);
// var northEast = map.unproject([ w, 0], map.getMaxZoom()-1);
// var bounds = new L.LatLngBounds( southWest, northEast);

// L.imageOverlay( url, bounds).addTo(map);

// map.setMaxBounds(bounds);


function clean_map(){

    if (marker) {
        map.removeLayer(marker);
    }

    // if (polyline) {
    //     map.removeLayer(polyline);
    // }

}


let marker;
map.on('click', function (event) {
    clean_map();
    marker = L.marker(event.latlng);
    marker.addTo(map);
    wkt = "POINT("+event.latlng.lng.toString()+" "+event.latlng.lat.toString()+")"
    marker.bindPopup(wkt).openPopup();
 })


function calculate_elevation_select(){
    let sel = document.getElementById('select_wkt');
    let wkt = sel.options[sel.selectedIndex].text;
    let url = 'http://' + window.location.host + '/api/elevation?wkt='+ wkt;
    
    let xhr = new XMLHttpRequest();
    xhr.open("GET", encodeURI(url));
    xhr.send();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $("#output_linestring").html(this.responseText);
            // console.log(this.responseText);
        }
    };
    
}

document.getElementById("select_wkt").addEventListener("change", (ev) => {
    output_linestring.innerHTML = '';
});


function check_image() {

    var chbox;
    chbox=document.getElementById('checkbox_image');
        if (chbox.checked) {
            imageOverlay.addTo(map)
        }
        else {
            map.removeLayer(imageOverlay)
        }

}


document.getElementById("select_format").addEventListener("change", (ev) => {
    var buttonId = document.getElementById("select_format").value;
    var button = document.querySelector('[button="' + buttonId + '"]');
    var buttons = document.querySelectorAll(".hiden_button").forEach(el => {
        el.style.display = 'none';
        clean_map();
    });
    button.style.display = 'block';
    output_linestring.innerHTML = '';
});


function makePoint(inputId) {

    let wkt;
    map.off('click');
    map.on('click', function(event) {
        output_linestring.innerHTML = '';        
        clean_map();

        marker = L.marker(event.latlng);
        marker.addTo(map);
        wkt = "POINT(" + event.latlng.lng.toString() + " " + event.latlng.lat.toString() + ")";
        // console.log(marker, wkt)
        document.getElementById(inputId).value = wkt;
    });

}


function calculate_elevation_custom(){

    let wkt = document.getElementById('input_wkt').value;
    let url = 'http://' + window.location.host + '/api/elevation?wkt='+ wkt;
    
    let xhr = new XMLHttpRequest();
    xhr.open("GET", encodeURI(url));
    xhr.send();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $("#output_linestring").html(this.responseText);
            // console.log(this.responseText);
        }
    };
    
}


function get_wkt(polyline){

    let wkt = "LINESTRING(";
    latlongs = polyline.getLatLngs();

    latlongs.forEach((element) => {
        wkt += element.lng + " " + element.lat + ", ";
    })
    wkt = wkt.slice(0, -2); 
    wkt += ')';

    return wkt;

}


var polyline = new L.Polyline([]).addTo(map);

function makePolyline(inputId) {
    let wkt;

    map.off('click');
    map.on('click', function(event) {
        clean_map();

        new L.Marker(event.latlng).addTo(map);
        polyline.addLatLng(event.latlng);
        wkt = get_wkt(polyline);
        document.getElementById(inputId).value = wkt;

    });

}

