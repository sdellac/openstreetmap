from functions import *
from distance import *
from pyroutelib2.route import *
import json
import requests
import linecache
import time
import random


#Envoi la position de car au serveur
def postPosition(car):
        global serverToContact
	payload = json.loads(get_payload(car))
	headers = {'content-type': 'application/json'}
	#print ("PAYLOAD" + json.dumps(payload))
	try:
		r = requests.post(serverToContact, data = json.dumps(payload), headers = headers, allow_redirects=False)
                print('Server response: '+ r.text)
                if r.status_code == 303:
                        serverToContact = 'http://'+r.headers['location']+'/'
                        postPosition(car)
	except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
		print e


#Simule un deplacement. Envoi la position au serveur tous les timeToPost.
def move_to(car, timeToPost):
        while car.arrived is False:
                time.sleep(timeToPost)
                car.move(timeToPost)
                print ('Send position ' +str(car.x)+' '+str(car.y))
                postPosition(car)
        print (str(car.x)+' '+str(car.y)+' <------------------- REACHED\n\n')


#Simule un deplacement. Envoi la position au serveur tous les timeToPost. Affiche la progression.
def move_to_progress(car, timeToPost, coords):
        dtot = getdtot(coords)
        travel = gettravel(coords)

        while car.arrived is False:
                time.sleep(timeToPost)
                car.move_progress(timeToPost, dtot, travel)
                print ('Send position ' +str(car.x)+' '+str(car.y))
                postPosition(car)
        print (str(car.x)+' '+str(car.y)+' <------------------- REACHED\n\n')


#Genere un chemin avec Pyroutelib2 puis appele move_to
def move_car (car, start_x, start_y, end_x, end_y, option):
        timeToPost = 1
        car.x = start_x
        car.y = start_y
        
        data = LoadOsm("car")
        node1 = data.findNode(start_x,start_y)
        node2 = data.findNode(end_x,end_y)

        router = Router(data)
        result, route = router.doRoute(node1, node2)

        if result == 'success':
                listo = []

                for i in route:
                        node = data.rnodes[i]
                        listo.append(Point(node[0], node[1]))
                car.l = listo

                if (option is True):
                        coords = listpos(start_x, start_y, end_x, end_y)
                        move_to_progress(car, timeToPost, coords)
                else:
                        move_to(car, timeToPost)
                print('\nFinal position: '+str(car.x)+' '+str(car.y))
        
        else:
                 print("Failed (%s)" % result)

                        
#Fonction principale
def main():

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
    
                                print ('\nC est parti !')

                        voiture = Car(latStartPoint, lonStartPoint,identifiant,0.0003)
                        move_car(voiture, latStartPoint, lonStartPoint, latEndPoint, lonEndPoint, percent)

                if n == 2:
                        ch =raw_input("\nAfficher la progression du trajet (oui ou non)  : ")
                        if ch == 'oui':	
                                percent = True
                        else:
                                percent = False
    
                        print ('\nC est parti !')

                        voiture = Car(0, 0, get_mac(), 0.0003)
                        move_car(voiture, 44.837442, -0.574733, 44.832543, -0.575012, percent)

                        #voiture = Car(44.871144, -0.613308, get_mac(), 0.003)
                        #move_to(voiture, 44.791809, -0.605515, 0.2)
        
                if n == 3:
                        restart = False
                        break



#Main

#Parse les fichiers de configurations
defaultServer = linecache.getline('./client.conf', 1).strip()
backupServer = linecache.getline('./client.conf', 2).strip()

defaultPort = 8080
serverToContact = defaultServer

main()

print ('Fin du programme')







