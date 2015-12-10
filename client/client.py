from functions import *
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
                if r.status_code == 303:
                        print (r.text)
                        newUrl = 'http://'+r.headers['location']+':'+str(defaultPort)
                        #postPosition(newUrl, car)
                else:
                        print(r.text)
	except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
		print e


#Simule un deplacement vers (dest_x, dest_y). Envoi la position au serveur tous les timeToPost.
def move_to(url, car, dest_x, dest_y, timeToPost):
        while car.arrived is False:
                car.move(dest_x, dest_y, timeToPost)
                print (str(car.x)+' '+str(car.y))
                postPosition(url, car)
                time.sleep(timeToPost)
        print (str(dest_x)+' '+str(dest_y)+' <------------------- REACHED\n')

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

#Main
defaultServer = linecache.getline('./client.conf', 1).strip()
backupServer = linecache.getline('./client.conf', 2).strip()

serverToContact = defaultServer
c=Car(23,9,get_mac(),3)

#straight_move(serverToContact, c, 20, 1)
#random_move(serverToContact, c, 2, 1)
move_to(serverToContact, c, 2, 12, 1)

print ('fin du programme')







