var map;

function initialize() {
    var centerLatLon = new google.maps.LatLng(59.332598, 18.065236);
    var myOptions = {
        zoom: 10,
        center: centerLatLon,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    };

    map = new google.maps.Map(document.getElementById("map"), myOptions);

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
            if (lines.length % 6 == 1) {
                for(var i = 0; i < lines.length-1; i=i+6){
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
                        new google.maps.LatLng(nw_lat, nw_lon),
                        new google.maps.LatLng(sw_lat, sw_lon),
                        new google.maps.LatLng(se_lat, se_lon),
                        new google.maps.LatLng(ne_lat, ne_lon)
                    ];

                    var min = lines[i+5] + ' min';

                    makePolygon(boxCoords, min, color);
                }
            }
        }
    });
};

function makePolygon(polyCoords, polyLabel, color) {
    var marker = new MarkerWithLabel({
        position: new google.maps.LatLng(0,0),
        draggable: false,
        raiseOnDrag: false,
        map: map,
        labelContent: polyLabel,
        labelAnchor: new google.maps.Point(30, 20),
        labelClass: "labels", // the CSS class for the label
        labelStyle: {opacity: 1.0},
        icon: "http://placehold.it/1x1",
        visible: false
     });

    var poly = new google.maps.Polygon({
        paths: polyCoords,
        strokeColor: color,
        strokeOpacity: 0.8,
        strokeWeight: 0,
        fillColor: color,
        fillOpacity: 0.7,
        map: map
    });

    google.maps.event.addListener(poly, "mousemove", function(event) {
        marker.setPosition(event.latLng);
        marker.setVisible(true);
    });
    google.maps.event.addListener(poly, "mouseout", function(event) {
        marker.setVisible(false);
    });
}

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
}

function splitLine(line) {
    return line.split(',')
}

function getLatFromLine(line) {
    return parseFloat(splitLine(line)[0])
}

function getLonFromLine(line) {
    return parseFloat(splitLine(line)[1])
}

google.maps.event.addDomListener(window, 'load', initialize);