'use strict'

var winston = require('winston'),
    fs = require('fs'),
    bodyParser = require('body-parser'),
    express = require('express');

var app = express();
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

var argv = require('yargs')
	.usage('Usage: $0 -i [num]')
    	.demand(['i'])
	.argv;

class Zone {
	constructor(config) {
		this.minlat = config['minlat'];
		this.maxlat = config['maxlat'];
		this.minlon = config['minlon'];
		this.maxlon = config['maxlon'];
	}
}

class Server {
	constructor(config) {
		this.zone = new Zone(config['zone']);
		this.host = config['host'];
	}
}

class Client {
	constructor(config) {
		this.id = config['id'];
		this.lat = config['position']['lat'];
		this.lon = config['position']['lon'];
	}

	in(zone) {
		return this.lat >= zone.minlat &&
			this.lat < zone.maxlat &&
			this.lon >= zone.minlon &&
			this.lon < zone.maxlon;
	}

	static equals(c1, c2) {
		return c1.id === c2.id &&
			c1.lon === c2.lon &&
			c1.lat === c2.lat;
	}
}

class ClientMap {
	constructor() {
		this._dict = {};
	}

	update(client) {
		if (this._dict[client.id] === undefined || !Client.equals(client, this._dict[client.id])) {
			this._dict[client.id] = client; // TODO: dispatch updates through socket.io
		}
	}

	remove(client) {
		delete this._dict[client.id];
	}
}

var servers = JSON.parse(fs.readFileSync('server.conf', 'utf8'))['servers'].map(function (obj) {
	return new Server(obj);
});
//console.log(servers);

var me = servers[argv.i];
var port = 8080; // TODO: extract from config, default to 8080

var clients = new ClientMap();

function findServerFor(client) {
	for (let server of servers) {
		if (client.in(server.zone)) {
			return server;
		}
	}

	return undefined;
}

app.post('/', function (req, res) {
	let client, next_hop;
	try {
		client = new Client(req.body['client']);
		next_hop = findServerFor(client);
	} catch(err) {
		res.sendStatus(400); // Bad Request
		return;
	}

	if (next_hop === me) {
		clients.update(client);
		res.sendStatus(200); // OK
		return;
	} else if (next_hop === undefined) {
		clients.remove(client);
		res.sendStatus(404); // Not Found
		return;
	} else {
		clients.remove(client);
		res.redirect(303, next_hop.host); // See Other
	}
});

var server = app.listen(port, function () {
	var port = server.address().port;

	winston.info('server %s listening on port %s', me.host, port);
});
