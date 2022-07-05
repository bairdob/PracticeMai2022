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

function makePoint1() {
    var marker1;
    map.on('click', function(event){

        if (marker1 == undefined) {    
            marker1 = L.marker(event.latlng);

            marker1.addTo(map);

            text1 = "POINT("+event.latlng.lng.toString()+" "+event.latlng.lat.toString()+")"
            marker1.bindPopup(text1).openPopup();
            document.getElementById('input_point1').value = text1;

        }       
        else {
            map.removeLayer(marker1);
            // map.removeLayer(markers);
            marker1 = L.marker(event.latlng)
            point1 = marker1;
            marker1.addTo(map);
            map.invalidateSize()
            text1 = "POINT("+event.latlng.lng.toString()+" "+event.latlng.lat.toString()+")"
            marker1.bindPopup(text1).openPopup();
            document.getElementById('input_point1').value = text1;

        }
                        
    });
 
}

function makePoint2() {
    var marker;

    map.on('click', function(event){

        if (marker == undefined) {    
            marker = L.marker(event.latlng);
            marker.addTo(map);
            text2 = "POINT("+event.latlng.lng.toString()+" "+event.latlng.lat.toString()+")"
            marker.bindPopup(text2).openPopup();
            document.getElementById('input_point2').value = text;
        }       
        else {
            map.removeLayer(marker);
            marker = L.marker(event.latlng);
            marker.addTo(map);
            text2 = "POINT("+event.latlng.lng.toString()+" "+event.latlng.lat.toString()+")"
            marker.bindPopup(text2).openPopup();
            document.getElementById('input_point2').value = text2;
        }
                        
    });

}


function test(form){
    document.getElementById('input_point1').value = "point1";
    document.getElementById('input_point2').value = "point2";
}
