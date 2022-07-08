var TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
map = L.map('llmap').fitWorld();
L.tileLayer(TILE_URL).addTo(map);

let markers = {};
function makePoint(inputId, markerId) {

    let wkt;
    map.off('click');
    map.on('click', function(event) {
        if (markers[markerId]) {
            map.removeLayer(markers[markerId]);
            map.invalidateSize();
        }
        if (polyline){
            map.removeLayer(polyline);
        }
        markers[markerId] = L.marker(event.latlng);
        markers[markerId].addTo(map);
        wkt = "POINT("+event.latlng.lng.toString()+" "+event.latlng.lat.toString()+")"
        // console.log(markers, wkt)
        document.getElementById(inputId).value = wkt;
    });

}


function calculate_orthodrome_line(){
    point1 = document.getElementById('input_point1').value;
    point2 = document.getElementById('input_point2').value;
    cs = document.getElementById('input_coordinate_system').value;
    count = document.getElementById('input_count').value;
    url = 'http://' + window.location.host + '/api/calculate_orthodrome_line?point1='+ point1 + '&point2=' + point2 +'&cs='+ cs +'&count='+ count;
    
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

function parseLinestring(t) {
    let items = t.replace(/^LINESTRING\(|\)$/g, "").split(",\ ");
    items.forEach(function(val, index, array) {
       array[index] = val.split("\ ").map(Number);
    });
    return items;
}


var polyline;
function addPolyline(){

    if (polyline){
        map.removeLayer(polyline);
    }

    let linestring = document.getElementById('output_linestring').value;
    let result = parseLinestring(linestring);

    let latlngs = []
    result.forEach((element) => {
        latlngs.push(new L.LatLng(element[1], element[0]))
    });

    polyline = new L.Polyline(latlngs, { color: '#2A81CB', opacity: 0.5 });
    polyline.addTo(map);

}