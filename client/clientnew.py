from functions import *
from distance import *
from pyroutelib2.route import *
import json
import requests
import linecache
import time
import random

defaultPort = 60000

#Envoi la position de car a l'url indiquee
def postPosition(url, car):
	payload = json.loads(get_payload(car))
	headers = {'content-type': 'application/json'}
	#print ("PAYLOAD" + json.dumps(payload))
	try:
		r = requests.post(url, data = json.dumps(payload), headers = headers, allow_redirects=False)
                print('Server response: '+ r.text)
                if r.status_code == 303:
                        newUrl = 'http://'+r.headers['location']+':'+str(defaultPort)
                        #postPostion(newUrl, car)
	except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
		print e


#Simule un deplacement vers (dest_x, dest_y). Envoi la position au serveur tous les timeToPost.
def move_to(url, car, dest_x, dest_y, timeToPost):
        while car.arrived is False:
                time.sleep(timeToPost)
                car.move(dest_x, dest_y, timeToPost)
                print ('Send position ' +str(car.x)+' '+str(car.y))
                postPosition(url, car)
        print (str(dest_x)+' '+str(dest_y)+' <------------------- REACHED\n\n')


def move_car (car, start_x, start_y, end_x, end_y, option):
        car.x = start_x
        car.y = start_y
        if (option is True):
                coords = listpos(start_x, start_y, end_x, end_y)
                dtot = getdtot(coords)
                travel = gettravel(coords)
                j = 0
        
        #print dtot
        data = LoadOsm("car")
        node1 = data.findNode(start_x,start_y)
        node2 = data.findNode(end_x,end_y)

        router = Router(data)
        result, route = router.doRoute(node1, node2)
        
        if result == 'success':
                for i in route:
                        node = data.rnodes[i]
                        #print ('Current position: ' + str(car.x)+' '+str(car.y))
                        #print('Next destination: '+ str(node[0])+' '+str(node[1]))
                        #print('MOVE')
                        move_to(serverToContact, car, node[0], node[1], 0.2)
			if (option is True):
                                pourcentage = travel[j-1] / dtot *100
                                if (j > 0):
                                        print('COMPLETION DU PARCOURS : '+ str(int(pourcentage)) + ' %')
                                j = j+1
                        car.arrived = False
        else:
                print("Failed (%s)" % result)
                        
        print('\nFinal position: '+str(car.x)+' '+str(car.y))



#Main
defaultServer = linecache.getline('./client.conf', 1).strip()
backupServer = linecache.getline('./client.conf', 2).strip()

serverToContact = defaultServer

restart = True

print ('----------Bienvenue dans le client python----------')


while restart is True:
    ch =input("\nChoisissez votre option: \n\n1: Faire un nouveau trajet \n2: Trajet par defaut\n3: Quitter  \n> ")
    n =int(ch)
    
    if n == 1:
        ch =input("\nVeuillez entrer l'ID de la voiture  : ")
        identifiant = int(ch)
        
	print ("\nVeuillez entrer un point de depart  : ")
        ch =input("Latitude de depart  : ")
        latStartPoint = float(ch)
	ch =input("Longitude de depart  : ")
        lonStartPoint = float(ch)
        
	print ("\nVeuillez entrer un point d arrivee  : ")
        ch =input("Latitude d arrivee  : ")
        latEndPoint = float(ch)
	ch =input("Longitude d arrivee  : ")
        lonEndPoint = float(ch)

        ch =raw_input("\nAfficher la progression du trajet (oui ou non)  : ")

        if ch == 'oui':	
            percent = True
        else:
            percent = False
    
        print ('C est parti !')

	voiture = Car(latStartPoint, lonStartPoint,identifiant,0.0003)
	#move_car(voiture, latStartPoint, lonStartPoint, latEndPoint, lonEndPoint)

	move_car(voiture, 44.837442, -0.574733, 44.832543, -0.575012, percent)
        #move_to(serverToContact, voiture, latEndPoint, lonEndPoint, 1):

    if n == 2:
        ch =raw_input("\nAfficher la progression du trajet (oui ou non)  : ")
        if ch == 'oui':	
            percent = True
        else:
            percent = False
    
        print ('\nC est parti !')

        voiture = Car(0, 0, get_mac(), 0.0003)
        move_car(voiture, 44.837442, -0.574733, 44.832543, -0.575012, percent)
        
    if n == 3:
        restart = False
        break



print ('Fin du programme')







