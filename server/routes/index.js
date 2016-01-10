"use strict"

module.exports = function(io) {
    var express = require('express');
    var router = express.Router();

    /* Get servers configurations */
    var argv = require('yargs')
        .usage('Usage: $0 [options]')
        .help('h')
        .alias('h', 'help')
        .default('i', 0)
        .describe('i', 'Server id')
        .default('c', 'config.json')
        .describe('c', 'Server configuration file')
        .argv;

    var fs = require('fs');
    var Joi = require('joi');
    var config = fs.readFileSync(argv.c, 'utf8');
    var configSchema = require('../models/config.schema.js');
    var config = Joi.validate(config, configSchema);

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

    var servers = config.value.servers.map(function (obj) {
        return new Server(obj);
    });
    var me = servers[argv.i];

    var clientSchema = require('../models/client.schema.js');

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

    function findServersFor(client) {
        var handling_servers = [];
        for (let server of servers) {
            if (client.in(server.zone)) {
                handling_servers.push(server);
            }
        }

        return handling_servers;
    }

    function Map() {
        this._dict = {};
    }

    Map.prototype.update = function(client) {
        if (this._dict[client.id] === undefined || !_.isEqual(client, this._dict[client.id])) {
            this._dict[client.id] = client;
            io.emit('update', client);
        }
    }

    Map.prototype.remove = function(client) {
        io.emit('remove', this._dict[client.id]);
        delete this._dict[client.id];
    }

    var request = require('request');

    function dispatch(client, servers) {
        var payload = {
            client: client,
            isServer: true
        }
        for (let server of servers) {
            if (server !== me) {
                let options = {
                  uri: 'http://' + server.host + '/',
                  method: 'POST',
                  json: payload
                }
                request.post(options);
            }
        }
    }

    var clients = new Map();

    var url = require('url');
    router.port = parseInt(url.parse('http://' + me.host).port) || 8080;

    router.post('/', function(req, res) {
      var form = Joi.validate(req.body, clientSchema);
      if (form.error) {
        res.sendStatus(400);
        return;
      }

      var client = new Client(form.value.client);
      var hservers = findServersFor(client);

      if (form.value.isServer === true) {
          clients.update(client);
          res.sendStatus(200); // OK
          return;
      }

      if (hservers.indexOf(me) !== -1) {
          clients.update(client);
          dispatch(client, hservers);
          res.sendStatus(200); // OK
          return;
      } else if (hservers.length === 0) {
          clients.remove(client);
          res.sendStatus(404); // Not Found
          return;
      } else {
          clients.remove(client);
          res.redirect(303, hservers[0].host); // See Other
      }
    });

    router.get('/', function(req, res) {
        res.render('index', {servers: servers, me: argv.i, port: router.port});
    });

    return router;
}
