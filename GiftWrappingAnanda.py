
#Calculates Convex Hull using GiftWrap Algorythm
#By Ananda Leon, Nov 1, 2018
#At Run time, the code will paint two graphs:
    #Graph 1: contains original polygon
    #Graph 2: contains calculated Convex hull
    #Coordinates of both graphs adjust to fit the screen.
    #You can use positive and negative X,Y

from math import sqrt
from math import atan2
from math import pi
import pygame

#set up the screen
WIDTH = 800
HEIGHT = 300
screen_size = [WIDTH, int(2.5*HEIGHT)]
secondGraphPos = 2.4
pygame.init()
screen = pygame.display.set_mode(screen_size)
font = pygame.font.SysFont('Arial',20)
GREEN = (  0, 255,   0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init
        self.angulo = 0

    def shiftForScreen(self,shiftpoint):
        p = Point(0,0)
        p.x = self.x + shiftpoint.x
        p.y = -self.y + shiftpoint.y
        return p

    def __repr__(self):
        return "".join(["Point(",str(self.x),",",str(self.y),") ->",str(self.angulo)])

def angulo (p):
    return p.angulo


class Poligono:
    def __init__(self):
        self.lista=[]
        self._puntoInicial = Point(0,0)
        self._shiftX = 0 #for printing to screen
        self._shiftY = 0 #for printing to screen


    def anadir(self,p):
        self.lista.append(p)

    def __repr__(self):
        l=""
        for i in self.lista:
            l+=str(i)+"\n"
        return l

    def ConvexHullGiftWrap (self,screen_pos):
        finalPoints = Poligono() #Polygon that will contain convex hull
        #find the Initial Point for GiftWrap algorithm (lowest to the right)
        self._puntoInicial = self.puntoInicial()
        currentPoint = self._puntoInicial
        nextPoint = (self._puntoInicial.x-1,self._puntoInicial.y-1) #Initialized point outside the polygon

        while (nextPoint!=self._puntoInicial ):
            #go through all Points in Polygon and obtain smalest angle from currentPoint
            for i in self.lista:
                i.angulo = atan2(i.y-currentPoint.y,i.x-currentPoint.x) - currentPoint.angulo
                #convert negative angles from atan2 into positives
                #if ((i.angulo <= 0) and (i != currentPoint)) :
                if (i.angulo <= 0) :
                    i.angulo = i.angulo + 2*pi
            #sort polygon with smallest angle first
            self.lista.sort(key=angulo)
            #update pointer
            nextPoint = self.lista[0]
            #Start painting the outline of the ConvexHull
            p = currentPoint.shiftForScreen(Point(self._shiftX,int(screen_pos*HEIGHT)+self._shiftY))
            p_next = nextPoint.shiftForScreen(Point(self._shiftX,int(screen_pos*HEIGHT)+self._shiftY))
            pygame.draw.line(screen, GREEN, [p.x,p.y], [p_next.x,p_next.y], 1)
            #update pointer
            currentPoint = nextPoint
            self.lista.remove(nextPoint)
            #add to Convex hull polygon
            finalPoints.lista.append(currentPoint)

        #return final polygon with only points in ConvexHull
        return finalPoints

    def puntoInicial(self): #finds the lowest, most right Point in Polygon
        miny= 100000 #assumes highest Point in Polygon < 100000 Y axis
        maxx = -100000 #assumes left most Point in Polygon > -100000 in X axis
        menor = Point(maxx,miny)
        for j in self.lista:
            if j.y<=miny:
                if j.x>menor.x:
                    menor = j
                    miny = menor.y
                    maxx = menor.x
                else:
                    if j.y != miny:
                        menor = j
                        miny = menor.y
        print("Initial Point GiftWrap:",menor)
        return menor

    def findShiftValues(self):#Offset in X and Y to fit the screen
        minx = 100000
        miny = 100000

        #lets find the smallest values for x and y
        for i in self.lista:
            if i.x < minx:
                minx = i.x
            if i.y < miny:
                miny = i.y
        #use this values to shift and fit you polygon in the screen
        if (minx<0):
            self._shiftX = -minx + 10
        else:
            self._shiftX = 10

        if (miny<0):
            self._shiftY = miny
        else:
            self._shiftY = 0

    def printPaint (self,paint_color,screen_pos):

        print(self)
        self.findShiftValues()
        for i in self.lista:
            p = i.shiftForScreen(Point(self._shiftX,int(screen_pos*HEIGHT)+self._shiftY))
            pygame.draw.circle(screen, paint_color, [p.x,p.y], 5)


#create random points
#READ ME!!!!!
#Maximum distance from Points cannot exceed screen Height = 300, for printing purposes
p = Poligono()
p.anadir(Point(50,40))
p.anadir(Point(25,-20))
p.anadir(Point(90,140))
p.anadir(Point(-80,60))
p.anadir(Point(310,60))
p.anadir(Point(60,60))
p.anadir(Point(210,-70))
p.anadir(Point(410,90))
p.anadir(Point(140,-120))
p.anadir(Point(190,-1))
p.anadir(Point(27,37))
p.anadir(Point(100,0))
p.anadir(Point(31,69))


#lets paint and print our Polygon
print("These are the points in your original Polygon")
p.printPaint(BLUE,1)
text = font.render("ORIGINAL POLYGON",True,GREEN)
screen.blit(text,(WIDTH/2,10))

#start finding convex hull
giftwrap = p.ConvexHullGiftWrap(secondGraphPos)
print("Convex Hull result:\n")
giftwrap.printPaint(RED,secondGraphPos)
text = font.render("CONVEX HULL",True,GREEN)
screen.blit(text,(WIDTH/2,HEIGHT+10))

#lets create our axis
shiftinX = p._shiftX
shiftinY = p._shiftY
pygame.draw.line(screen, GREEN, [0,HEIGHT+shiftinY], [WIDTH-10,HEIGHT+shiftinY], 1)#X axis 1st graph
pygame.draw.line(screen, GREEN, [shiftinX,0], [shiftinX,HEIGHT+10], 1)#Y axis 1st graph
#lets create our axis for convexhull
pygame.draw.line(screen, GREEN, [0,secondGraphPos*HEIGHT+shiftinY], [WIDTH-10,secondGraphPos*HEIGHT+shiftinY], 1)#X axis 2nd graph
pygame.draw.line(screen, GREEN, [shiftinX,2.5*HEIGHT-HEIGHT], [shiftinX,2.5*HEIGHT+10], 1)#Y axis 2nd graph

#show screen
pygame.display.flip()
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
#time.sleep(5.5) #necesario para no cerrar la pantalla inmediatamente
pygame.quit()
