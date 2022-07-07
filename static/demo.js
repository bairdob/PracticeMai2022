function makeMap() {
    // var point1 = L.marker([10, 10]).bindPopup('point1'),
    // point2 = L.marker([0, 0]).bindPopup('point2');
    // var markers = L.layerGroup([point1, point2]);

    var TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    var MB_ATTR = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    map = L.map('llmap').fitWorld();
    L.tileLayer(TILE_URL, {attribution: MB_ATTR}).addTo(map);

}



$(function() {
    makeMap();

})

let markers = {};
function makePoint(inputId, markerId) {

    let wkt;
    map.on('click', function(event) {
        if (markers[markerId]) {
            map.removeLayer(markers[markerId]);
            map.invalidateSize();
        }
        markers[markerId] = L.marker(event.latlng);
        markers[markerId].addTo(map);
        wkt = "POINT("+event.latlng.lng.toString()+" "+event.latlng.lat.toString()+")"
        console.log(markers, wkt)
        document.getElementById(inputId).value = wkt;
    });

}



function test(form){
    document.getElementById('input_point1').value = "point1";
    document.getElementById('input_point2').value = "point2";
}
