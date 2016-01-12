class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def affichage(self):
        return '('+str(self.x)+';'+str(self.y)+')'

    def milieu(self,p):
        return Point((self.x+p.x)/2,(self.y+p.y)/2)

    def vecteur(self,p):
        return Vecteur(p.x-self.x,p.y-self.y)

    def distance(self,p):
        return self.vecteur(p).norme()
