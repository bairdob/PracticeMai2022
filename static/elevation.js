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

L.rectangle(latLngBounds).addTo(map);
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

let marker;
map.on('click', function (event) {
		if (marker) {
        map.removeLayer(marker);
     }
     marker = L.marker(event.latlng);
     marker.addTo(map);
     marker.bindPopup(event.latlng.toString()).openPopup();
 })


function calculate_elevation(){

    // let point = document.getElementById('input_point').value;
    // let url = 'http://' + window.location.host + '/api/elevation?wkt='+ point;
    let url = 'http://127.0.0.1:5000/api/elevation?wkt=POINT(55.5 160.5)';
    
    let xhr = new XMLHttpRequest();
    xhr.open("GET", encodeURI(url));
    xhr.send();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $("#output_linestring").html(this.responseText);
            // console.log(this.responseText);
            addPolyline();
        }
    };
    
}


