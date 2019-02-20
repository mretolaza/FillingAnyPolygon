import libs 
import struct
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

def glLoadOb(filename, get_coords): 
    img.loadObj(filename, get_coords)

#Show new image 
def glFinish():
    img.writeFile("polygon.bmp")



glCreateWindow(1000,800)
glViewPort(0,0,1000,800)
glClear()
glColor(1, 1, 1)
glVertex(0,0)
glLoadOb('pol1.pol', True)
glLoadOb('pol2.pol', True)
glLoadOb('pol3.pol', True)
glLoadOb('pol4.pol', True)
glColor(0, 0, 0)
glLoadOb('pol5.pol', True)
print('Se ha generado el objeto')
glFinish()