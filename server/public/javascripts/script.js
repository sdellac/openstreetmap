(function () {
    var zone = servers[me].zone;
    var bounds = L.latLngBounds([[zone.minlat, zone.minlon], [zone.maxlat, zone.maxlon]]);

    var map = L.map('map', {
        center: [(zone.maxlat-zone.minlat)/2+zone.minlat, (zone.maxlon-zone.minlon)/2+zone.minlon],
        maxBounds: bounds,
        dragging: false,
        touchZoom: false,
        scrollWheelZoom: false,
        doubleClickZoom: false,
        keyboard: false,
        tap: false,
        zoomControl: false
    });

    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
            maxZoom: 18
            }).addTo(map);

    for (server of servers) {
        L.rectangle(L.latLngBounds([[server.zone.minlat, server.zone.minlon], [server.zone.maxlat, server.zone.maxlon]]), {color: server.color, weight: 1}).addTo(map);
    }

    map.fitBounds(bounds);
    window.addEventListener('resize', function(event){
        map.fitBounds(bounds);
    });

    var markers = {};

    var socket = io('http://' + location.host);
    socket.on('update', function (data) {
        console.log(data);
        if (markers[data.id] === undefined) {
            markers[data.id] = L.marker([data.position.lat, data.position.lon]).addTo(map);
        } else {
            markers[data.id].setLatLng([data.position.lat, data.position.lon]);
        }
    });
})()
