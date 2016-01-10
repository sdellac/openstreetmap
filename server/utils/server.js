"use strict"

var request = require('request'),
    chalk = require('chalk');

var findServersFor = function(client, servers) {
    var handling_servers = [];
    for (let server of servers) {
        if (client.in(server.zone)) {
            handling_servers.push(server);
        }
    }

    return handling_servers;
}

var dispatch = function(client, servers, me) {
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
            request
                .post(options)
                .on('error', function(err) {
                    console.error(chalk.yellow('WARN'), err.message);
                });
        }
    }
}

module.exports = {
    findServersFor: findServersFor,
    dispatch: dispatch
}
