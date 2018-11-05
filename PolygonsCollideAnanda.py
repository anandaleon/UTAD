
#Determines if Polygons A and B are colliding using AABB
#By Ananda Leon, Nov 3, 2018
#At Run time, the code will paint two graphs:
    #Graph 1: contains original polygons
    #Graph 2: contains AABB
    #Coordinates of both graphs adjust to fit the screenself.
    #You can use positive and negative X,Y
import math
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
font = pygame.font.SysFont('Arial',50)
GREEN = (  0, 255,   0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CUSTOMBLUE = (100, 255, 255)
CUSTOMRED = (255, 100, 50)
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
    def shift(self, other):
        self.x += other.x
        self.y += other.y
    def __add__(self, other):
        return Point((self.x + other.x, self.y + other.y))
    def __sub__(self, other):
        return Point((self.x - other.x, self.y - other.y))
    def __mul__(self, scalar):
        return Point((self.x*scalar, self.y*scalar))
    def divide(self, scalar):
        return Point((self.x/scalar, self.y/scalar))
    def __len__(self):
        return int(math.sqrt(self.x**2 + self.y**2))
    # get back values in original tuple format
    def get(self):
        return (self.x, self.y)
    def __repr__(self):
        return "".join(["Point(",str(self.x),",",str(self.y),") ->",str(self.angulo)])

def angulo (p):
    return p.angulo


class Poligono:
    def __init__(self):
        self.lista=[]
        self._puntoInicial = Point([0,0])
        self._minX = 0
        self._minY = 0
        self._maxX = WIDTH
        self._maxY = HEIGHT
        self._shiftX = 0 #for printing to screen
        self._shiftY = 0 #for printing to screen


    def anadir(self,p):
        self.lista.append(p)

    def __repr__(self):
        l=""
        for i in self.lista:
            l+=str(i)+"\n"
        return l

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
        #print("Initial Point GiftWrap:",menor)
        return menor

    def ConvexHullGiftWrap (self, color, screen_pos):
        finalPoints = Poligono() #Polygon that contains convex hull
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
            p = currentPoint.shiftForScreen(Point([shiftX,int(screen_pos*HEIGHT)+shiftY]))
            p_next = nextPoint.shiftForScreen(Point([shiftX,int(screen_pos*HEIGHT)+shiftY]))
            pygame.draw.line(screen, color, [p.x,p.y], [p_next.x,p_next.y], 1)
            #pygame.draw.line(screen, color, [currentPoint.x+shiftX,-currentPoint.y+screen_pos*HEIGHT+shiftY], [nextPoint.x+shiftX,-nextPoint.y+screen_pos*HEIGHT+shiftY], 1)
            currentPoint = nextPoint
            self.lista.remove(nextPoint)
            #add to Convex hull polygon
            finalPoints.lista.append(currentPoint)

        #return final polygon with only points in ConvexHull
        return finalPoints

    def findBoundaries(self):#find min and max X & Y
        minx = 100000
        miny = 100000
        maxy = -10000
        maxx = -10000

        #lets find the smallest values for x and y
        for i in self.lista:
            if i.x < minx:
                minx = i.x
            if i.y < miny:
                miny = i.y
            if i.x > maxx:
                maxx = i.x
            if i.y > maxy:
                maxy = i.y

        #use this values to shift and fit you polygon in the screen
        if (minx<0):
            self._shiftX = -minx + 10
        else:
            self._shiftX = 10

        if (miny<0):
            self._shiftY = miny-10
        else:
            self._shiftY = -10

        self._minX = minx
        self._minY = miny
        self._maxX = maxx
        self._maxY = maxy

    def printPaint (self,paint_color,screen_pos):

        print(self)
        for i in self.lista:
            p = i.shiftForScreen(Point([shiftX,int(screen_pos*HEIGHT)+shiftY]))
            pygame.draw.circle(screen, paint_color, [i.x+shiftX,-i.y+shiftY+int(screen_pos*HEIGHT)], 5)

def isCollision(PolygonA, PolygonB):
    #print AABB Boundaries for Polygon A
    draw_dashed_line(screen, CUSTOMBLUE,(shiftX,-PolygonA._maxY+secondGraphPos*HEIGHT+shiftY), (PolygonA._maxX+shiftX,-PolygonA._maxY+secondGraphPos*HEIGHT+shiftY), 1,10)
    draw_dashed_line(screen, CUSTOMBLUE,(shiftX,-PolygonA._minY+secondGraphPos*HEIGHT+shiftY), (PolygonA._maxX+shiftX,-PolygonA._minY+secondGraphPos*HEIGHT+shiftY), 1,10)
    draw_dashed_line(screen, CUSTOMBLUE,(PolygonA._minX+shiftX,secondGraphPos*HEIGHT+shiftY), (PolygonA._minX+shiftX,-PolygonA._maxY+secondGraphPos*HEIGHT+shiftY), 1,10)
    draw_dashed_line(screen, CUSTOMBLUE,(PolygonA._maxX+shiftX,secondGraphPos*HEIGHT+shiftY), (PolygonA._maxX+shiftX,-PolygonA._maxY+secondGraphPos*HEIGHT+shiftY), 1,10)
    #print AABB Boundaries for Polygon B
    draw_dashed_line(screen, CUSTOMRED,(shiftX,-PolygonB._maxY+secondGraphPos*HEIGHT+shiftY), (PolygonB._maxX+shiftX,-PolygonB._maxY+secondGraphPos*HEIGHT+shiftY), 1,10)
    draw_dashed_line(screen, CUSTOMRED,(shiftX,-PolygonB._minY+secondGraphPos*HEIGHT+shiftY), (PolygonB._maxX+shiftX,-PolygonB._minY+secondGraphPos*HEIGHT+shiftY), 1,10)
    draw_dashed_line(screen, CUSTOMRED,(PolygonB._minX+shiftX,secondGraphPos*HEIGHT+shiftY), (PolygonB._minX+shiftX,-PolygonB._maxY+secondGraphPos*HEIGHT+shiftY), 1,10)
    draw_dashed_line(screen, CUSTOMRED,(PolygonB._maxX+shiftX,secondGraphPos*HEIGHT+shiftY), (PolygonB._maxX+shiftX,-PolygonB._maxY+secondGraphPos*HEIGHT+shiftY), 1,10)

    #if boundaries on X axis don't collide, return NO
    if not (((PolygonB._minX > PolygonA._minX) and (PolygonB._minX < PolygonA._maxX))
        or ((PolygonB._maxX > PolygonA._minX) and (PolygonB._maxX < PolygonA._maxX))):
        return False
    #if Boundaries on Y axis don't collide, return NO
    if not (((PolygonB._minY > PolygonA._minY) and (PolygonB._minY < PolygonA._maxY))
    or ((PolygonB._maxY > PolygonA._minY) and (PolygonB._maxY < PolygonA._maxY))):
        return False

    return True

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    origin = Point(start_pos)
    target = Point(end_pos)
    displacement = target - origin
    length = len(displacement)
    slope = displacement.divide(length)

    for index in range(0, int(length/dash_length), 2):
        start = origin + (slope *    index    * dash_length)
        end   = origin + (slope * (index + 1) * dash_length)
        pygame.draw.line(surf, color, start.get(), end.get(), width)

#READ ME!!!!!
#Maximum distance from Points cannot exceed screen Width = 400, for printing purposes
#Lets construct Polygon A
A = Poligono()
A.anadir( Point([400,100]))
A.anadir( Point([600,-50]))
A.anadir( Point([450,50]))
A.anadir( Point([350,100]))
A.anadir( Point([430,20]))
A.anadir( Point([600,20]))

#Lets construct Polygon B
B = Poligono()
B.anadir( Point([10,180]))
B.anadir( Point([200,130]))
B.anadir( Point([50,70]))


#find the boundaries for AABB method
A.findBoundaries()
B.findBoundaries()

#lets create our axis
#find the shift X and Y for printing purposes, when using negative numbers
if (A._shiftX<B._shiftY):
        shiftX = B._shiftX
else:
    shiftX = A._shiftX

if (A._shiftY<B._shiftY):
    shiftY = A._shiftY
else:
    shiftY = B._shiftY


pygame.draw.line(screen, GREEN, [0,HEIGHT+shiftY], [WIDTH-10,HEIGHT+shiftY], 1) #X axis 1st graph
pygame.draw.line(screen, GREEN, [shiftX,0], [shiftX,HEIGHT+10], 1)#Y axis 1st graph
pygame.draw.line(screen, GREEN, [0,secondGraphPos*HEIGHT+shiftY], [WIDTH-10,secondGraphPos*HEIGHT+shiftY], 1)#X axis 2nd graph
pygame.draw.line(screen, GREEN, [shiftX,2.5*HEIGHT-HEIGHT], [shiftX,2.5*HEIGHT+10], 1)#Y axis 2nd graph


#lets paint and print our Polygon A
A.printPaint(BLUE,1)
ConvexA = A.ConvexHullGiftWrap(BLUE,secondGraphPos)
print("Convex Hull of Polygon A:\n")
ConvexA.printPaint(BLUE,secondGraphPos)

#lets paint and print our Polygon B
B.printPaint(RED,1)
ConvexB = B.ConvexHullGiftWrap(RED,secondGraphPos)
print("Convex Hull of Polygon B:\n")
ConvexB.printPaint(RED,secondGraphPos)

#Is there a collision?
if  isCollision(A,B):
    print("\nYES, THE BOUNDARIES OF THE POLYGONS ARE COLLIDING \n")
    text = font.render("COLLIDING",True,RED)
    screen.blit(text,(WIDTH/2,HEIGHT/2))
else:
    print("\nNO,  THE BOUNDARIES OF THE POLYGONS ARE NOT COLLIDING\n")
    text = font.render("NOT COLLIDING",True,GREEN)
    screen.blit(text,(WIDTH/2,HEIGHT/2))

#show screen
pygame.display.flip()
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
#time.sleep(5.5) #necesario para no cerrar la pantalla inmediatamente
pygame.quit()
