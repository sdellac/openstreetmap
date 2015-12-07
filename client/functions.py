from uuid import getnode as get_mac
from math import *
from point import *

class Car(Point):
    def __init__(self,x,y,id):
        Point.__init__(self,x,y)
        self.id=id

    def affichage(self):
        return '('+str(self.x)+';'+str(self.y)+';'+str(self.id)+')'

    def refresh(self,x,y):
        self.x=x
	self.y=y


def print_mac():
    mac = get_mac()
    print(mac)

def payloadtest():
   return '{ \"client\":'+'\n'+'{\"ID\" : \"value\",'+'\n'+'\"Position\" :'+'\n'+'{\"lat\" : x'+'\n'+'\"lon\" : y}'+'\n'+'}'+'\n'+'\"isServer\" : bool'+'\n'+'}'

def get_payload(car):
    return'{ \"client\":{\"id\":'+str(car.id)+',\"position\":{\"lat\":'+str(car.x)+',\"lon\":'+str(car.y)+'}}}' 







