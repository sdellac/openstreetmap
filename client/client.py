from functions import *
import json
import requests
import linecache
import time
import random


defaultPort = 8080

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


def straight_move(url, car, dest_y, timeToPost):
        for i in range(car.y,dest_y): 
              car.move(car.x, i, timeToPost)
              print (str(car.x)+' '+str(car.y))
              postPosition(url, car)
              time.sleep(timeToPost)
              
        
def random_move (url, car, cpt, timeToPost):
        while cpt != 0:
                dest_x = random.randrange(20)
                dest_y = random.randrange(20)
                print ('------------- FROM '+str(car.x)+' '+str(car.y)+' Going to '+str(dest_x)+' '+str(dest_y)+'---------------')

                while car.arrived is False:
                        car.move(dest_x, dest_y, timeToPost)
                        print (str(car.x)+' '+str(car.y))
                        postPosition(url, car)
                        time.sleep(timeToPost)

                print (str(dest_x)+' '+str(dest_y)+' <------------------- REACHED\n')
                car.arrived = False
                cpt -= 1

#Main
defaultServer = linecache.getline('./client.conf', 1).strip()
backupServer = linecache.getline('./client.conf', 2).strip()

serverToContact = defaultServer
c=Car(1,10,get_mac(),2.5)

#straight_move(serverToContact, c, 20, 1)
random_move(serverToContact, c, 2, 1)


print ('fin du programme')







