var _ = require('lodash');

function Server(obj) {
    this.host = "";
    this.zone = {
        minlat: 0,
        maxlat: 0,
        minlon: 0,
        maxlon: 0
    };
    _.assign(this, obj);
}

module.exports = Server;
