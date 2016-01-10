var _ = require('lodash');

function Map(io) {
    this._dict = {};
    this.io = io;
}

Map.prototype.update = function(client) {
    if (this._dict[client.id] === undefined || !_.isEqual(client, this._dict[client.id])) {
        this._dict[client.id] = client;
        this.io.emit('update', client);
    }
}

Map.prototype.remove = function(client) {
    this.io.emit('remove', this._dict[client.id]);
    delete this._dict[client.id];
}

module.exports = Map;
