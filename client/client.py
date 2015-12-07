from functions import *
import json
import requests
import linecache


def postPosition(url, car):
	payload = json.loads(get_payload(car))
	headers = {'content-type': 'application/json'}
	s=requests.Session()
	r = None
	try:
		r = s.post(url, data = json.dumps(payload), headers = headers)
	except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
		print ("Failed to connect to "+url)
		print e
	return r


#Main
defaultServer = linecache.getline('./client.conf', 1).strip()
backupServer = linecache.getline('./client.conf', 2).strip()
defaultPort = '8080'

serverToContact = defaultServer
c=Car(1,1,get_mac())

#Premiere connection determinant l'utilisation du serveur de secours
res = postPosition(serverToContact, c)
if res is None:
		serverToContact = backupServer
		print('BACKUP SERVER '+serverToContact)
		res = postPosition(serverToContact, c)

#"Deplacement de la voiture"
for i in range(5,15) :
	c.refresh(1, i)
	res = postPosition(serverToContact, c)

	if res is None:
		break

	print ('pour i = '+str(i))
	if "OK" in res.text: 
    		print('OK')
	elif "Not Found" in res.text:
    		print('Not Found')
	else:
    		serverToContact = 'http://'+res.text.replace("Cannot GET /","").strip()+':'+defaultPort+'/'
		print ('New server to contact: '+serverToContact)


print ('fin du programme')







