import libs 
import struct
import math
import os 
from libs import Bitmap
from libs import word

#Objet to draw 
img = None

#Constructor 
def glInit():
    return None

#Init FrameBuffer
def glCreateWindow(width, height):
    global img 
    img = Bitmap(width,height) 

#Delete actual image 
def glClear(): 
    img.clear()
#Image area can draw
def glViewPort(x,y,widht, height):
    img.viewPort(x,y,widht, height)

#Get Color 
def glColor(r,g,b):
    img.color(r,g,b)

#Init canvas with new color 
def glClearColor(r,g,b):
    img.clearColor(0,0,0) 

#Get new x,y points 
def glVertex(x,y):
    img.vertex(x,y)

def getNewX(x): 
    return img.getNormXCoord(x)

def getNewY(y): 
    return img.getNormYCoord(y)

def glLine (x1,y1, x2,y2):
    img.line(x1, y1, x2, y2)

#Show new image 
def glFinish():
    img.writeFile("img.bmp")



glCreateWindow(800,600)
glViewPort(0,0,799,599)
glClear()
glColor(1, 0, 0)
glVertex(0,0)
glLine(getNewX(10),getNewY(10),getNewX(510),getNewY(10))
glLine(getNewX(10),getNewY(10),getNewX(462),getNewY(191))
glLine(getNewX(10),getNewY(10),getNewX(354),getNewY(354))
glLine(getNewX(10),getNewY(10),getNewX(191),getNewY(462))
glLine(getNewX(10),getNewY(10),getNewX(10),getNewY(510))
glFinish()