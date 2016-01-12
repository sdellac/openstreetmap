var _ = require('lodash');

function Map(io) {
    this._dict = {};
    this._int = {};
    this.io = io;
}

Map.prototype.update = function(client) {
    if (this._dict[client.ID] === undefined || !_.isEqual(client, this._dict[client.ID])) {
        this._dict[client.ID] = client;

        // Reset timer
        clearInterval(this._int[client.ID]);
        this._int[client.ID] = setInterval(function() {
            this.remove(client);
        }.bind(this), 30000);

        this.io.emit('update', client);
    }
}

Map.prototype.remove = function(client) {
    this.io.emit('remove', this._dict[client.ID]);
    delete this._dict[client.ID];
}

module.exports = Map;
