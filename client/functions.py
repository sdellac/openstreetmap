from uuid import getnode as get_mac
from math import *
from point import *

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
        
        if distX > self.v*time:
            self.x += self.v*time
        elif abs(distX) <= self.v*time:
            self.x = destX
        else:
            self.x -= self.v*time


        if distY > self.v*time:
            self.y += self.v*time
        elif abs(distY) <= self.v*time:
            self.y = destY
        else:
            self.y -= self.v*time
        
        if self.x == destX and self.y == destY:
            self.arrived = True
        


def print_mac():
    mac = get_mac()
    print(mac)

def payloadtest():
   return '{ \"client\":'+'\n'+'{\"ID\" : \"value\",'+'\n'+'\"Position\" :'+'\n'+'{\"lat\" : x'+'\n'+'\"lon\" : y}'+'\n'+'}'+'\n'+'\"isServer\" : bool'+'\n'+'}'

def get_payload(car):
    return'{ \"client\":{\"id\":'+str(car.id)+',\"position\":{\"lat\":'+str(car.x)+',\"lon\":'+str(car.y)+'}}}' 






