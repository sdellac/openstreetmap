var _ = require('lodash');

function Client(obj) {
    this.ID = "";
    this.Position = {
        lat: 0,
        lon: 0
    }
    _.assign(this, obj);
}

Client.prototype.in = function(zone) {
    return this.Position.lat >= zone.minlat &&
        this.Position.lat < zone.maxlat &&
        this.Position.lon >= zone.minlon &&
        this.Position.lon < zone.maxlon;
}

module.exports = Client;
