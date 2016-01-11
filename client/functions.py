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

    def print_position(self):
        return '('+str(self.x)+';'+str(self.y)+';'+str(self.id)+')'

    def refresh_position(self,x,y):
        self.x=x
	self.y=y

    #Deplace la voiture de v*time lorsque celle ci a pour destination le point (destX, destY)
    def move(self, destX, destY, time):
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
        elif abs(distX) <= vx*time:
            self.x = destX
        else:
            self.x -= vx*time


        if distY > vy*time:
            self.y += vy*time
        elif abs(distY) <= vy*time:
            self.y = destY
        else:
            self.y -= vy*time
        
        if self.x == destX and self.y == destY:
            self.arrived = True
        


def print_mac():
    mac = get_mac()
    print(mac)

def payloadtest():
    return '{ \"client\":'+'\n'+'{\"ID\" : \"value\",'+'\n'+'\"Position\" :'+'\n'+'{\"lat\" : x'+'\n'+'\"lon\" : y}'+'\n'+'}'+'\n'+'\"isServer\" : bool'+'\n'+'}'

def get_payload(car):
    return'{\"client\":{\"id\":'+str(car.id)+',\"position\":{\"lat\":'+str(car.x)+',\"lon\":'+str(car.y)+'}}}' 


class Object:
    def to_JSON(self, car):
        return json.dumps(self, default=lambda o: o.__dict__, 
                          sort_keys=True, indent=4)

def get_payload2(car):

    payload = Object()
    payload.client = Object()
    payload.client.id = str(car.id)
    payload.client.position = Object()
    payload.client.position.lat = car.x
    payload.client.position.lon = car.y
    return payload.to_JSON(car)

car=Car(52.55,-1.8,54,0.0001)
print get_payload2(car)
    
#commande correcte
#curl -i -H "Content-Type: application/json" -X POST -d '{"client": {"id" : "5", "position" :{"lat" : 44.837442, "lon": -0.574733}}}' http://37.187.116.52:60000



