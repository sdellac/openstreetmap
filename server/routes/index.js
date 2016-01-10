var express = require('express'),
    fs = require('fs'),
    Joi = require('joi'),
    _ = require('lodash'),
    url = require('url');

/* Models */
var Server = require('../models/server.js'),
    Client = require('../models/client.js'),
    Map = require('../models/map.js');

/* Validation schemas */
var configSchema = require('../models/config.schema.js'),
    clientSchema = require('../models/client.schema.js');

var utils = require('../utils/server.js');

/* Server configuration gathering */
var argv = require('yargs')
    .usage('Usage: $0 [options]')
    .help('h')
    .alias('h', 'help')
    .default('i', 0)
    .describe('i', 'Server id')
    .default('c', 'config.json')
    .describe('c', 'Server configuration file')
    .argv;

var config_file = fs.readFileSync(argv.c, 'utf8'),
    config = Joi.validate(config_file, configSchema);

var servers = config.value.servers.map(function (obj) {
    return new Server(obj);
});
var me = servers[argv.i];

/* Routes definition */
module.exports = function(io) {

    var router = express.Router();
    router.port = parseInt(url.parse('http://' + me.host).port) || process.env.PORT || 8080;

    var clients = new Map(io);

    // Send handled clients on connect
    io.on('connection', function (socket) {
        socket.emit('init', clients._dict);
    });

    /* Client coordinates submission */
    router.post('/', function(req, res) {
      /* Form validation */
      var form = Joi.validate(req.body, clientSchema);
      if (form.error) {
        res.sendStatus(400); // Bad Request
        return;
      }

      var client = new Client(form.value.client);
      var hservers = utils.findServersFor(client, servers); // Handling servers

      // TODO: Ensure the request comes from a registered server
      if (form.value.isServer === true) {
          clients.update(client);
          res.sendStatus(200); // OK
          return;
      }

      if (hservers.indexOf(me) !== -1) {
          clients.update(client);
          utils.dispatch(client, hservers, me);
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

    // Server state real-time interface
    router.get('/', function(req, res) {
        res.render('index', {servers: servers, me: argv.i});
    });

    return router;
}
