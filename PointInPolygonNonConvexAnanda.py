
#Determines if a Point P2 or P2 is inside Polygon A that is NOT convexhull
#This method uses the sum of angles, and checks if point is to the LEFT of all the
#sides of the Polygon A or intersecting the polygon
#By Ananda Leon, Nov 3, 2018
#At Run time, the code will paint Polygon A, P1 and P2
    #If p is inside A, the grapgh will say "P is inside the polygon"
    #If p is Intersecting the Polygon, the grapgh will say "P is INTERSECTING the polygon"
    #If p is not part of the Polygon, the graph will say "P is not inside the Polygon"
    #You can use positive and negative numbers for polygon and P1, P2

from math import sqrt
from math import atan2
from math import acos
from math import pi
import pygame

#set up the screen
WIDTH = 800
HEIGHT = 400
screen_size = [WIDTH, HEIGHT]
pygame.init()
screen = pygame.display.set_mode(screen_size)
font = pygame.font.SysFont('Arial',20)
GREEN = (  0, 255,   0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Point:
    def __init__(self, point_t = (0,0)):
        self.x = (point_t[0])
        self.y = (point_t[1])
        self.angulo = 0
    def shiftForScreen(self,shiftpoint):
        p = Point([0,0])
        p.x = self.x + shiftpoint.x
        p.y = -self.y + shiftpoint.y
        return p
    def __repr__(self):
        return "".join(["Point(",str(self.x),",",str(self.y),") ->",str(self.angulo)])

    def paintPoint(self,name,color,screen_pos):
        p = self.shiftForScreen(Point([shiftinX,int(screen_pos*HEIGHT+shiftinY)]))
        pygame.draw.circle(screen, color,[p.x,p.y],5)
        text = font.render(name,True,color)
        screen.blit(text,(p.x,p.y))


def angulo (p):
    return p.angulo


class Poligono:
    def __init__(self):
        self.lista=[]
        self._puntoInicial = Point([0,0])
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
        finalPoints._puntoInicial = self._puntoInicial
        currentPoint = self._puntoInicial
        nextPoint = (self._puntoInicial.x-1,self._puntoInicial.y-1) #Initialized point outside the polygon

        while (nextPoint!=self._puntoInicial ):
            #go through all Points in Polygon and obtain smalest angle from currentPoint
            for i in self.lista:
                i.angulo = atan2(i.y-currentPoint.y,i.x-currentPoint.x) - currentPoint.angulo
                #convert negative angles from atan2 into positives
                #if ((i.angulo <= 0) and (i != currentPoint)) :
                if (i.angulo <= 0) :
                    i.angulo = i.angulo + 2*3.1416
            #sort polygon with smallest angle first
            self.lista.sort(key=angulo)
            #update pointer
            nextPoint = self.lista[0]
            #Start painting the outline of the ConvexHull
            p = currentPoint.shiftForScreen(Point([self._shiftX,int(screen_pos*HEIGHT)+self._shiftY]))
            p_next = nextPoint.shiftForScreen(Point([self._shiftX,int(screen_pos*HEIGHT)+self._shiftY]))
            pygame.draw.line(screen, GREEN, [p.x,p.y], [p_next.x,p_next.y], 1)
            currentPoint = nextPoint
            self.lista.remove(nextPoint)
            #add to Convex hull polygon
            finalPoints.lista.append(currentPoint)

        #return final polygon with only points in ConvexHull
        return finalPoints

    def puntoInicial(self): #finds the lowest, most right Point in Polygon
        miny= 100000 #assumes highest Point in Polygon < 100000 Y axis
        maxx = -100000 #assumes left most Point in Polygon > -100000 in X axis
        menor = Point([maxx,miny])
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
            self._shiftY = miny - 10
        else:
            self._shiftY = -10

    def printPaint (self,paint_color,screen_pos):

        print(self)
        self.findShiftValues()
        for i in self.lista:
            p = i.shiftForScreen(Point([self._shiftX,int(screen_pos*HEIGHT)+self._shiftY]))
            pygame.draw.circle(screen, paint_color, [p.x,p.y], 5)

    def outline (self,paint_color,screen_pos):
        index = len(self.lista)
        currentPoint = self.lista[index-1]
        for i in self.lista:
            p = currentPoint.shiftForScreen(Point([self._shiftX,int(screen_pos*HEIGHT)+self._shiftY]))
            p_next = i.shiftForScreen(Point([self._shiftX,int(screen_pos*HEIGHT)+self._shiftY]))
            pygame.draw.line(screen, paint_color, [p.x,p.y], [p_next.x,p_next.y], 1)
            currentPoint = i

    def isPointInsideConvex(self,punto):#checks if a point (punto) is inside polygon
        currentPoint = self._puntoInicial
        #check if punto is always to the left of the aristas
        for i in self.lista:
            if not isleft(currentPoint,i,punto):
                return False
            currentPoint = i

        return True

    def isPointInsidePolygon(self,punto):#checks if a point (punto) is inside polygon using sum of angles
        sum = 0.0
        index = len(self.lista)
        currentPoint = self.lista[index-1]
        pointer = 0
        #check the sum of the angles is== 2PI
        for i in range(0,index):
            if  ((currentPoint.x == punto.x) and (currentPoint.y == punto.y) ):
                angle = getAngle(punto,self.lista[i-2],self.lista[i])
                sum += 2*pi +angle
            else:
                sum += getAngle(punto,currentPoint,self.lista[i])
            currentPoint = self.lista[i]
        print("The sum of all the angles:",sum)
        return bool((sum<(2*pi+0.0001)) and (sum>(2*pi-0.0001)))

    def isPointCollinear(self,punto):#checks if a point (punto) is on the border
        currentPoint = self._puntoInicial
        #check if punto is always to the left of the aristas
        for i in self.lista:
            if isCollinear(currentPoint,i,punto):
                return True
            currentPoint = i

        return False

def isleft(a,b,c): #returns true if point c, is Left of the segment a -> b
    return bool(((b.x-a.x)*(c.y-a.y))-((c.x-a.x)*(b.y-a.y))>=0)

def isCollinear(a,b,c): #returns true if point c, is collinear with a->b
    return bool(((b.x-a.x)*(c.y-a.y))-((c.x-a.x)*(b.y-a.y))==0)

def getAngle(a,b,c): #gets angle of vertice a
    vectorAB = Point([b.x-a.x,b.y-a.y])
    vectorAC = Point([c.x-a.x,c.y-a.y])
    dotProduct = vectorAB.x*vectorAC.x+vectorAB.y*vectorAC.y
    magAB = sqrt(vectorAB.x*vectorAB.x + vectorAB.y*vectorAB.y)
    magAC = sqrt(vectorAC.x*vectorAC.x + vectorAC.y*vectorAC.y)
    if (magAB*magAC == 0):
        return 0
    result = acos(dotProduct/(magAB*magAC))
    if not isleft(b,c,a):
        result = result*-1
    return result



#READ ME!!!!!
#Maximum distance from Points cannot exceed screen Height = 300, for printing purposes
#lets create our Polygon
A = Poligono()
A.anadir(Point([70,20]))
A.anadir(Point([300,10]))
A.anadir(Point([250,110]))
A.anadir(Point([440,50]))
A.anadir(Point([660,50]))
A.anadir(Point([540,270]))
A.anadir(Point([200,170]))
A.anadir(Point([70,290]))
A.anadir(Point([30,50]))

#lets choose two random points
P1 = Point([80,80]) #one inside the polygon
P2 = Point([170,250]) #one outside the polygon

A.findShiftValues()
#lets create our axis
shiftinX = A._shiftX
shiftinY = A._shiftY
pygame.draw.line(screen, GREEN, [0,HEIGHT+shiftinY], [WIDTH-10,HEIGHT+shiftinY], 1)#X axis 1st graph
pygame.draw.line(screen, GREEN, [shiftinX,0], [shiftinX,HEIGHT+10], 1)#Y axis 1st graph

#lets paint and print our Polygon and our Point
print("These are the points in your original Polygon")
A.printPaint(BLUE,1)
A.outline(GREEN,1)

#Find if Point P1 is inside the Polygon
print("Calculating P1\n")
if A.isPointInsidePolygon(P1):
    if A.isPointCollinear(P1):
        print("P1 is INTERSECTING the Convex Hull\n")
        P1.paintPoint("P1 is INTERSECTING the Polygon",GREEN,1)
    else:    #Lets paint our Point P1
        print("P1 is inside the Polygon A\n")
        P1.paintPoint("P1 is Inside the Polygon",GREEN,1)
else:
    print("P1 is NOT inside the Polygon A\n")
    P1.paintPoint("P1 is NOT inside Polygon",RED,1)

#Find if Point P2 is inside the Polygon
print("Calculating P2\n")
if A.isPointInsidePolygon(P2):
    if A.isPointCollinear(P2):
        print("P2 is INTERSECTING the Convex Hull\n")
        P2.paintPoint("P2 is INTERSECTING the Polygon",GREEN,1)
    else:
        print("P2 is inside the Polygon A\n")
        P2.paintPoint("P2 is Inside the Polygon",GREEN,1)
else:
    print("P2 is NOT inside the Polygon A\n")
    P2.paintPoint("P2 is NOT inside Polygon",RED,1)


#show screen
pygame.display.flip()
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
#time.sleep(5.5) #necesario para no cerrar la pantalla inmediatamente
pygame.quit()
