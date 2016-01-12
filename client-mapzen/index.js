var map = L.map('map');

// Using Tangram 
//var layer = Tangram.leafletLayer({
  //scene: 'scene.yaml',
  //attribution: '<a href="https://mapzen.com/tangram" target="_blank">Tangram</a> | &copy; OSM contributors | <a href="https://mapzen.com/" target="_blank">Mapzen</a>'
//});
//layer.addTo(map);


// You can also use normal OSM tiles instead of Tangram
 L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
   attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
 }).addTo(map);

var controls = L.Routing.control({
  waypoints: [
    L.latLng(44.806, -0.605),
    L.latLng(44.841, -0.581)
  ],
  // You can get your own Valhalla API key from the Mapzen developer portal (https://mapzen.com/developers/)
  router: L.Routing.mapzen('valhalla-oJAv9do', 'auto'),
  geocoder: L.Control.Geocoder.nominatim(),
  formatter: new L.Routing.Mapzen.Formatter(),
  summaryTemplate:'<div class="start">{name}</div><div class="info {transitmode}">{distance}, {time}</div>'
});

controls.addTo(map);

/* Haversine formula */
function getDistanceFromLatLonInM(lat1, lon1, lat2, lon2) {
  var R = 6371000; // Radius of the earth in m
  var dLat = deg2rad(lat2-lat1);  // deg2rad below
  var dLon = deg2rad(lon2-lon1); 
  var a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
    Math.sin(dLon/2) * Math.sin(dLon/2)
    ; 
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  var d = R * c; // Distance in m
  return d;
}

function deg2rad(deg) {
  return deg * (Math.PI/180)
}

var route;
var loop = MainLoop.stop();
var coords;

var server = "37.187.116.52:60000";

var sync = function() {
    superagent
        .post('http://127.0.0.1:1337/' + server + '/')
        .send({
            client: {
                ID: "mapzen-78az5ez",
                Position: {
                    lat: coords[0],
                    lon: coords[1]
                }
            }
        })
        .end(function(err, res){
            if (res.req.url !== res.xhr.responseURL) {
                server = res.xhr.responseURL.substring(res.req.url.length, res.xhr.responseURL.length);
            }
        });
};

var syncInt;
var circle = L.circle(coords, 5, {
    color: 'blue',
    fillColor: '#03f',
    fillOpacity: 0.5
});

controls.on('routeselected', function(e) {
    clearInterval(syncInt);
    map.removeLayer(circle);
    loop.stop();
    route = e.route;

    // Instructions data
    var i = 0;
    var speed = route.instructions[i].distance*1000 / route.instructions[i].time;

    // Shape data
    var j = route.instructions[i].begin_shape_index;
    var distance = getDistanceFromLatLonInM(
        route.coordinates[j][0],
        route.coordinates[j][1],
        route.coordinates[j+1][0],
        route.coordinates[j+1][1]
    );
    var remaining_distance = distance;
    // Beware of references in Javascript !
    var start = route.coordinates[j].slice(0);
    coords = route.coordinates[j].slice(0);
    var vect = [
        route.coordinates[j+1][0]-route.coordinates[j][0],
        route.coordinates[j+1][1]-route.coordinates[j][1]
    ];
    circle = L.circle(coords, 5, {
        color: 'blue',
        fillColor: '#03f',
        fillOpacity: 0.5
    }).addTo(map);

    var begin = function() {
        if (remaining_distance <= 0) {
            j++;
            for (; j >= route.instructions[i].end_shape_index || j >= route.coordinates.length;) {
                i++;
                if (i >= route.instructions.length) {
                    clearInterval(syncInt);
                    loop.stop();
                    return;
                }
                speed = route.instructions[i].distance*1000 / route.instructions[i].time;
                j = route.instructions[i].begin_shape_index;
                continue;
            }
            distance = getDistanceFromLatLonInM(
                route.coordinates[j][0],
                route.coordinates[j][1],
                route.coordinates[j+1][0],
                route.coordinates[j+1][1]
            );
            remaining_distance = distance;
            start = route.coordinates[j].slice(0);
            coords = route.coordinates[j].slice(0);
            vect = [
                route.coordinates[j+1][0]-route.coordinates[j][0],
                route.coordinates[j+1][1]-route.coordinates[j][1]
            ];
        }
    }

    var update = function(delta) {
        remaining_distance -= (delta/1000)*speed;
        coords[0] = start[0] + (distance - remaining_distance) * vect[0] / distance;
        coords[1] = start[1] + (distance - remaining_distance) * vect[1] / distance;
        if (isNaN(coords[0])) {
            clearInterval(syncInt);
            loop.stop();
        }
    }

    var draw = function() {
        if (isNaN(coords[0])) {
            clearInterval(syncInt);
            loop.stop();
        }
        circle.setLatLng(coords, coords);
    }

    loop = MainLoop.setBegin(begin).setUpdate(update).setDraw(draw).start();
    syncInt = setInterval(sync, 10000);
});
