var http = require("http");
var url = require("url");

var client_str = '{\"client\":{\"ID\" : \"125469\",\"Position\" : {\"lat\" : \"5\", \"lon\" : \"10\"}}, \"isServer\" : \"false\"}';

var servers_str = '{\"servers\":[{\"zone\":{\"maxlat\": 10,\"minlat\": 5,\"maxlon\": 11,\"minlon\": 5},\"host\":\"1.2.3.4\"},{\"zone\":{\"maxlat\": 10,\"minlat\": 3,\"maxlon\": 15,\"minlon\": 1},\"host\":\"1.2.3.5\"}]}';


/* Envoi une réponse au client ou aux autres serveurs, à partir du message du client, de la liste serveurs-zone et de l'adresse ip de notre serveur */
function redirect (client_msg, servers_list, my_ip) {

    var servers_obj = JSON.parse(servers_list);
    var client_obj = JSON.parse(client_msg);

    var zones = new Array(); // zones contenant la position du client excepté celle de notre serveur
    var isDefaultServer = false;
    var i = 0;
    
    var maxLat, minLat, maxLon, minLon;
    var idClient = client_obj.client.ID;
    var lat =  client_obj.client.Position.lat;
    var lon =  client_obj.client.Position.lon;

    while (i < servers_obj.servers.length) {
	maxLat = servers_obj.servers[i].zone.maxlat;
	minLat = servers_obj.servers[i].zone.minlat;
	maxLon = servers_obj.servers[i].zone.maxlon;
	minLon = servers_obj.servers[i].zone.minlon;
	
	if (lat <= maxLat && lat >= minLat && lon <= maxLon && lon >= minLon) {
	    
	    if(servers_obj.servers[i].host == my_ip) {
		isDefaultServer = true;
	    } else {
		zones.push(servers_obj.servers[i].host);
	    }
	} 
	i++;
    }

    if(isDefaultServer) {

	if(zones.length != 0){
	    var clientPos = '{\"client\":{\"ID\" : \"' +idClient+ '\",\"Position\" : {\"lat\" : \"' +lat+ '\", \"lon\" : \"' +lon+ '\"}}, \"isServer\" : \"true\"}';
	    //envoyer l'info aux autres servers
	}

    } else {
	if(zones.length == 0){
	    //ERREUR, Zone inconnu ?
	} else {
	    var serversToContact = '{ "servers" : [';

	    for (var i = 0; i < zones.length; i++) {
		serversToContact += '{\"IP\" : \"' + zones[i] +'\"},';
	    }
	    serversToContact = serversToContact.substring(0, serversToContact.length - 1);
	    serversToContact += ']}';
	    //envoyer au client la liste des serveurs a contacter
	} 	
    }
}


/* Fonction appelé a chaque fois que l'on fait une requete*/
function onRequest(request, response) {
  console.log("Requête reçue.");
  response.writeHead(200, {"Content-Type": "text/plain"});
  var my_path = url.parse(request.url).pathname;

  /*if (my_path == '/yolo') {
      console.log('je rentre');
      redirect (client_str, servers_str, '1.2.3.8');
  }*/

  response.write("Hello World " + my_path);

  response.end();
}

http.createServer(onRequest).listen(8888);
console.log("Démarrage du serveur.");
