function initMap() {
    var centerLatLon = {lat: 59.332598, lng: 18.065236};

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 11,
      center: centerLatLon,
      mapTypeId: google.maps.MapTypeId.TERRAIN
    });

    var marker = new google.maps.Marker({
        position: centerLatLon,
        map: map
    });

    getFileFromServer('coordinates_colored.txt', function(text) {
        if (text === null) {
            // An error occurred
        }
        else {
            var lines = text.split('\n')
            if (lines.length % 5 == 1) {
                for(var i = 0; i < lines.length-1; i=i+5){
                    var nw_lat = getLatFromLine(lines[i])
                    var nw_lon = getLonFromLine(lines[i])

                    var sw_lat = getLatFromLine(lines[i+1])
                    var sw_lon = getLonFromLine(lines[i+1])

                    var se_lat = getLatFromLine(lines[i+2])
                    var se_lon = getLonFromLine(lines[i+2])

                    var ne_lat = getLatFromLine(lines[i+3])
                    var ne_lon = getLonFromLine(lines[i+3])

                    var color = lines[i+4]
                    var boxCoords = [
                      {lat: nw_lat, lng: nw_lon}, // NW
                      {lat: sw_lat, lng: sw_lon}, // SW
                      {lat: se_lat, lng: se_lon}, // SE
                      {lat: ne_lat, lng: ne_lon}  // NE
                    ];

                    // Construct the polygon.
                    var colorBox = new google.maps.Polygon({
                      paths: boxCoords,
                      strokeColor: color,
                      strokeOpacity: 0.8,
                      strokeWeight: 0,
                      fillColor: color,
                      fillOpacity: 0.7
                    });

                    colorBox.setMap(map);
                }
            }
        }
    });
};

function getFileFromServer(url, doneCallback) {
    var xhr;

    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = handleStateChange;
    xhr.open("GET", url, true);
    xhr.send();

    function handleStateChange() {
        if (xhr.readyState === 4) {
            doneCallback(xhr.status == 200 ? xhr.responseText : null);
        }
    }
};

function splitLine(line) {
    return line.split(',')
}

function getLatFromLine(line) {
    return parseFloat(splitLine(line)[0])
}

function getLonFromLine(line) {
    return parseFloat(splitLine(line)[1])
}