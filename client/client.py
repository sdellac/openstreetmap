from functions import *
from pyroutelib2.route import *
import json
import requests
import linecache
import time
import random

defaultPort = 8080

#Envoi la position de car a l'url indiquee
def postPosition(url, car):
	payload = json.loads(get_payload(car))
	headers = {'content-type': 'application/json'}
	try:
		r = requests.post(url, data = json.dumps(payload), headers = headers, allow_redirects=False)
                print('Server response: '+ r.text)
                if r.status_code == 303:
                        newUrl = 'http://'+r.headers['location']+':'+str(defaultPort)
                        #postPosition(newUrl, car)
	except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
		print e


#Simule un deplacement selon la longitude vers dest_y. Envoi la position au serveur tous les timeToPost.
def straight_move(url, car, dest_y, timeToPost):
        move_to(url, car, car.x, dest_y, timeToPost)
              

#Simule cpt deplacements aleatoire. Envoi la position au serveur tous les timeToPost.     
def random_move (url, car, cpt, timeToPost):
        while cpt != 0:
                dest_x = random.randrange(20)
                dest_y = random.randrange(20)
                print ('------------- FROM '+str(car.x)+' '+str(car.y)+' Going to '+str(dest_x)+' '+str(dest_y)+'---------------')
                move_to(url, car, dest_x, dest_y, timeToPost)
                car.arrived = False
                cpt -= 1


#Simule un deplacement vers (dest_x, dest_y). Envoi la position au serveur tous les timeToPost.
def move_to(url, car, dest_x, dest_y, timeToPost):
        while car.arrived is False:
                time.sleep(timeToPost)
                car.move(dest_x, dest_y, timeToPost)
                print ('Send position ' +str(car.x)+' '+str(car.y))
                postPosition(url, car)
        print (str(dest_x)+' '+str(dest_y)+' <------------------- REACHED\n')


def move_car (car, start_x, start_y, end_x, end_y):
        car.x = start_x
        car.y = start_y

        data = LoadOsm("car")
        node1 = data.findNode(start_x,start_y)
        node2 = data.findNode(end_x,end_y)

        router = Router(data)
        result, route = router.doRoute(node1, node2)

        if result == 'success':
                for i in route:
                        node = data.rnodes[i]
                        print ('Current position: ' + str(car.x)+' '+str(car.y))
                        print('Next destination: '+ str(node[0])+' '+str(node[1]))
                        print('MOVE')
                        move_to(serverToContact, car, node[0], node[1], 0.1)
                        car.arrived = False
        else:
                print("Failed (%s)" % result)
                        
        print('\nFinal position: '+str(car.x)+' '+str(car.y))

def move_to2(url,car,dest_x,dest_y,timeToPost):
        car.move(dest_x,dest_y,timeToPost)
        print ('Send position ' +str(car.x)+' '+str(car.y))
        postPosition(url, car)
        print (str(dest_x)+' '+str(dest_y)+' <------------------- REACHED\n')

def listpos (car, start_x, start_y, end_x, end_y):
        car.x = start_x
        car.y = start_y

        data = LoadOsm("car")
        node1 = data.findNode(start_x,start_y)
        node2 = data.findNode(end_x,end_y)

        router = Router(data)
        result, route = router.doRoute(node1, node2)
        if result == 'success':
                for i in route:
                        print('node'+ i +':'+ data.rnodes[i])

#Main
defaultServer = linecache.getline('./client.conf', 1).strip()
backupServer = linecache.getline('./client.conf', 2).strip()

serverToContact = defaultServer
voiture = Car(52.55,-1.8,54,0.0001)

move_car(voiture, 52.552394, -1.818763, 52.563368, -1.818291)

print ('fin du programme')







