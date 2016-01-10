(function () {
    var zone = servers[me].zone;
    var bounds = L.latLngBounds([[zone.minlat, zone.minlon], [zone.maxlat, zone.maxlon]]);

    var map = L.map('map', {
        center: [(zone.maxlat-zone.minlat)/2+zone.minlat, (zone.maxlon-zone.minlon)/2+zone.minlon],
        maxBounds: bounds,
        dragging: true,
        touchZoom: false,
        scrollWheelZoom: true,
        doubleClickZoom: false,
        keyboard: false,
        tap: false,
        zoomControl: false
    });

    L.tileLayer('http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
        subdomains: 'abcd',
        maxZoom: 18
    }).addTo(map);

    for (server of servers) {
        L.rectangle(L.latLngBounds([[server.zone.minlat, server.zone.minlon], [server.zone.maxlat, server.zone.maxlon]]), {color: "#666", weight: 1}).addTo(map);
    }

    map.fitBounds(bounds);
    window.addEventListener('resize', function(event){
        map.fitBounds(bounds);
    });

    var markers = {};

    // Socket.io handlers
    var socket = io('http://' + location.host);
    socket.on('init', function (clients) {
        for (var prop in clients) {
            var data = clients[prop];
            markers[data.id] = L.marker([data.position.lat, data.position.lon], {title: data.id})
                .bindPopup(L.popup({closeButton: false, minWidth: 30})
                    .setContent(data.id))
                .addTo(map);
        }
    });

    socket.on('update', function (data) {
        if (markers[data.id] === undefined) {
            markers[data.id] = L.marker([data.position.lat, data.position.lon], {title: data.id})
                .bindPopup(L.popup({closeButton: false, minWidth: 30})
                    .setContent(data.id))
                .addTo(map);
        } else {
            markers[data.id].setLatLng([data.position.lat, data.position.lon]);
        }
    });

    socket.on('remove', function (data) {
        if (markers[data.id] !== undefined) {
            map.removeLayer(markers[data.id]);
            delete markers[data.id];
        }
    });
})()
