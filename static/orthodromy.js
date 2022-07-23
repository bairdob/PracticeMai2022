let TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
let map = L.map('llmap').fitWorld();
L.tileLayer(TILE_URL).addTo(map);

let markers = {};
function makePoint(inputId, markerId) {

    let wkt;
    map.off('click');
    map.on('click', function(event) {
        if (markers[markerId]) {
            map.removeLayer(markers[markerId]);
            map.invalidateSize();
            output_linestring.innerHTML = '';
        }
        if (polyline){
            map.removeLayer(polyline);
        }
        markers[markerId] = L.marker(event.latlng);
        markers[markerId].addTo(map);
        wkt = "POINT("+event.latlng.lng.toString()+" "+event.latlng.lat.toString()+")"
        // console.log(markers, wkt)
        document.getElementById(inputId).value = wkt;
        document.getElementById(inputId).style.backgroundColor = null;
    });

}


function calculate_orthodrome_line(event){
    
    let point1 = document.getElementById('input_point1').value;
    let point2 = document.getElementById('input_point2').value;
    let cs = document.getElementById('input_coordinate_system').value;
    let count = document.getElementById('input_count').value;
    let url = 'http://' + window.location.host + '/api/calculate_orthodrome_line?point1='+ point1 + '&point2=' + point2 +'&cs='+ cs +'&count='+ count;
    
    let xhr = new XMLHttpRequest();
    xhr.open("GET", encodeURI(url));
    xhr.send();
    xhr.onreadystatechange = function() {

        if (this.readyState == 4 && this.status == 200) {
            $("#output_linestring").html(this.responseText);
            // console.log(this.responseText);
            addPolyline();
        }
        else {   
            if (this.readyState == 3) { // demostration only: freezing page
                $("#output_linestring").html('calculating... please wait');
            }
                else {
                    $("#output_linestring").html(this.statusText);
                }
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

function changeInputBackground(element, pattern){
    if (element.value === '' || !pattern.test(element.value)) {
        element.style.backgroundColor = '#FFCDD2';
    } else {
        element.style.backgroundColor = null;
    };
};

let patternDigit = new RegExp(/^[0-9]+$/);
let patternPoint = new RegExp(/^POINT\([-]?[0-9]*\.[0-9]* [-]?[0-9]*\.[0-9]*\)$/);

let point1 = document.getElementById('input_point1');
let point2 = document.getElementById('input_point2');
let count = document.getElementById('input_count');

point1.addEventListener('change', function(){
    changeInputBackground(point1, patternPoint)
});

point2.addEventListener('change', function(){
    changeInputBackground(point2, patternPoint)
});

count.addEventListener('change', function(){
    changeInputBackground(count, patternDigit)
});

$(document).ready(function($) {
  $(document).on('submit', '#submit-form', function(event) {
    event.preventDefault();
  
    alert('page did not reload');
  });
});




