#!/bin/env node

'use strict'

var winston = require('winston'),
    fs = require('fs'),
    bodyParser = require('body-parser'),
    express = require('express');

var app = express(),
    server = require('http').Server(app),
    io = require('socket.io')(server);

app.use(bodyParser.json());

// Handle middlewares errors like JSON parsing
app.use(function(err, req, res, next) {
	if (res.headersSent) {
		return next(err);
	} else if (err.status) {
		return res.sendStatus(err.status);
	} else {
		res.status(500);
	}
});

app.set('view engine', 'ejs');

var argv = require('yargs')
	.usage('Usage: $0 -i [num]')
    	.demand(['i'])
	.argv;

// Classes definitions
class Zone {
	constructor() {
		this.minlat = 0;
		this.maxlat = 0;
		this.minlon = 0;
		this.maxlon = 0;
	}
}

class Server {
	constructor() {
		this.host = "";
		this.zone = new Zone();
	}
}

class Client {
	constructor(config) {
		this.id = "";
        this.position = {
            lat: 0,
            lon: 0
        };
	}

	in(zone) {
		return this.position.lat >= zone.minlat &&
			this.position.lat < zone.maxlat &&
			this.position.lon >= zone.minlon &&
			this.position.lon < zone.maxlon;
	}

	static equals(c1, c2) {
		return c1.id === c2.id &&
			c1.position.lon === c2.position.lon &&
			c1.position.lat === c2.position.lat;
	}
}

class ClientMap {
	constructor() {
		this._dict = {};
	}

	update(client) {
		if (this._dict[client.id] === undefined || !Client.equals(client, this._dict[client.id])) {
			this._dict[client.id] = client;
            io.emit('update', client);
		}
	}

	remove(client) {
        io.emit('remove', this._dict[client.id]);
		delete this._dict[client.id];
	}
}

var colors = ['#ee4035', '#0392cf', '#f37736', '#fdf498', '#7bc043'];

var i = 0;
var servers = JSON.parse(fs.readFileSync('server.conf', 'utf8'))['servers'].map(function (obj) {
	return new Server(obj, colors[i++]);
});
//console.log(servers);

var url = require('url');
var util = require('util');

var me = servers[argv.i];
var port = parseInt(url.parse('http://' + me.host).port) || 8080;

var clients = new ClientMap();

function findServersFor(client) {
    var handling_servers = [];
	for (let server of servers) {
		if (client.in(server.zone)) {
			handling_servers.push(server);
		}
	}

	return handling_servers;
}

var request = require('request');

function dispatch(client, servers) {
    client.isServer = true;
    for (let server of servers) {
        if (server !== me) {
            console.log(util.inspect(client));
            let options = {
              uri: 'http://' + server.host + '/',
              method: 'POST',
              json: client.toJSON()
            }
            request.post(options);
        }
    }
}

app.get('/', function (req, res) {
    res.render('index', { me: argv.i, port: port, servers: servers });
});

app.post('/', function (req, res) {
    console.log(util.inspect(req.body));
	let client, hservers;
	try {
		client = new Client(req.body['client']);
        hservers = findServersFor(client);
	} catch(err) {
		res.sendStatus(400); // Bad Request
		return;
	}

    console.log(hservers);

    if (client['isServer'] === true) {
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

server.listen(port+100);
winston.info('websockets listening on 127.0.0.1:%d', port+100);

var server = app.listen(port, function () {
	var port = server.address().port;

	winston.info('express listening on %s', me.host);
});
