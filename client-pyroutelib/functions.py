from uuid import getnode as get_mac
from math import *
from point import *
import json

class Car(Point):


    def __init__(self,x,y,id, v):
        Point.__init__(self,x,y)
        self.id=id
        self.v=v
        self.arrived=False
        self.l = []
	self.cpt = 0

    def print_position(self):
        return '('+str(self.x)+';'+str(self.y)+';'+str(self.id)+')'

    def refresh_position(self,x,y):
        self.x=x
	self.y=y

    #Deplace la voiture de v*time selon la liste de point l
    def move(self, time):
        
        destX = self.l[0].x
        destY = self.l[0].y

        distX = destX-self.x
        distY = destY-self.y

        if distX == 0:
            vx = 0
        else:
            vx = self.v/sqrt((distY/distX)*(distY/distX) + 1)
            
        if distY == 0:
            vy = 0
        else:
            vy = self.v/sqrt((distX/distY)*(distX/distY) + 1)
        
        if distX > vx*time:
            self.x += vx*time
        elif abs(distX) < vx*time:
            self.x = destX  
        elif abs(distX) == vx*time:
            self.x = destX 
        else:
            self.x -= vx*time


        if distY > vy*time:
            self.y += vy*time
        elif abs(distY) < vy*time:
            self.y = destY
        elif abs(distY) == vy*time:
            self.y = destY
        else:
            self.y -= vy*time


        if self.x == destX and self.y == destY:
            del self.l[0]
            if len(self.l) == 0:
                self.arrived = True
            elif abs(distX) < vx*time and abs(distY) < vy*time:
                timeleft = time - sqrt(distX*distX + distY*distY)/self.v
                self.move(timeleft)


        
     #Deplace la voiture de v*time selon la liste de point l et affiche la progression
    def move_progress(self, time, dtot, travel):

        destX = self.l[0].x
        destY = self.l[0].y

        distX = destX-self.x
        distY = destY-self.y

        if distX == 0:
            vx = 0
        else:
            vx = self.v/sqrt((distY/distX)*(distY/distX) + 1)
            
        if distY == 0:
            vy = 0
        else:
            vy = self.v/sqrt((distX/distY)*(distX/distY) + 1)
        
        if distX > vx*time:
            self.x += vx*time
        elif abs(distX) < vx*time:
            self.x = destX  
        elif abs(distX) == vx*time:
            self.x = destX 
        else:
            self.x -= vx*time


        if distY > vy*time:
            self.y += vy*time
        elif abs(distY) < vy*time:
            self.y = destY
        elif abs(distY) == vy*time:
            self.y = destY
        else:
            self.y -= vy*time


        if self.x == destX and self.y == destY:
	    if self.cpt > 0:
            	pourcentage = travel[self.cpt-1] / dtot *100
		print('\nCOMPLETION DU PARCOURS : '+ str(int(pourcentage)) + ' %\n')
	    self.cpt = self.cpt+1
            del self.l[0]
            if len(self.l) == 0:
                self.arrived = True
            elif abs(distX) < vx*time and abs(distY) < vy*time:
                timeleft = time - sqrt(distX*distX + distY*distY)/self.v
                self.move_progress(timeleft, dtot, travel)




class Object:
    def to_JSON(self, car):
        return json.dumps(self, default=lambda o: o.__dict__, 
                          sort_keys=True, indent=4)

def get_payload(car):

    payload = Object()
    payload.client = Object()
    payload.client.ID = str(car.id)
    payload.client.Position = Object()
    payload.client.Position.lat = car.x
    payload.client.Position.lon = car.y
    payload.isServer = False	
    return payload.to_JSON(car)

#car=Car(52.55,-1.8,54,0.0001)
#print get_payload(car)
    
#commande correcte
#curl -i -H "Content-Type: application/json" -X POST -d '{"client": {"id" : "5", "position" :{"lat" : 44.837442, "lon": -0.574733}}}' http://37.187.116.52:60000



