var _ = require('lodash');

function Client(obj) {
    this.id = "";
    this.position = {
        lat: 0,
        lon: 0
    }
    _.assign(this, obj);
}

Client.prototype.in = function(zone) {
    return this.position.lat >= zone.minlat &&
        this.position.lat < zone.maxlat &&
        this.position.lon >= zone.minlon &&
        this.position.lon < zone.maxlon;
}

module.exports = Client;
