import struct
import math
from obj_loader import obj_loader

def char(c):
    return struct.pack("=c", c.encode('ascii'))

def word(c):
    return struct.pack("=h", c)

def dword(c):
    return struct.pack("=l", c)

def color(r, g, b):
    return bytes([b, g, r])

class Bitmap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = []
        self.newGlColor = color(255, 255, 255)
        self.clear()
       

    #structure image file 
    def writeFile(self, filename):
        f = open(filename, "wb")
        # estandar
        f.write(char('B'))
        f.write(char('M'))
        # file size
        f.write(dword(14 + 40 + self.width * self.height * 3))
        # reserved
        f.write(dword(0))
        # data offset
        f.write(dword(54))
        # header size
        f.write(dword(40))
        # width
        f.write(dword(self.width))
        # height
        f.write(dword(self.height))
        # planes
        f.write(word(1))
        # bits per pixel
        f.write(word(24))
        # compression
        f.write(dword(0))
        # image size
        f.write(dword(self.width * self.height * 3))
        # x pixels per meter
        f.write(dword(0))
        # y pixels per meter
        f.write(dword(0))
        # number of colors
        f.write(dword(0))
        # important colors
        f.write(dword(0))
        # image data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])
        # close file
        f.close()
    
    #clear the canvas with a new color 
    def clearColor(self, r, g, b): 
        newR = math.floor(r*255)
        newG = math.floor(g*255)
        newB = math.floor(b*255)

        self.framebuffer = [
            [color(newR, newG, newB) for x in range(self.width)]
            for y in range(self.height)
        ]
    
    # Clear image 
    def clear(self):
        self.framebuffer = [
            [
                #show background color 
                self.color(0,0,0) for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    # get dimension image (begin of glViewPort)
    def viewPort(self, x, y, width, height):
        self.viewPortWidth = width
        self.viewPortHeight = height
        self.xViewPort = x
        self.yViewPort = y
    
    def getNormXCoord(self, realX):
        realXVP = realX - self.xViewPort
        dx = realXVP - (self.viewPortWidth / 2)
        x = dx / (self.viewPortWidth / 2)
        return x

    def getNormYCoord(self, realY):
        realYVP = realY - self.yViewPort
        dy = realYVP - (self.viewPortHeight / 2)
        y = dy / (self.viewPortHeight / 2)
        return y

    def vertex(self, x, y):
        if ((x >= -1 and x <= 1) and (y >= -1 and y <= 1)):
            # x           
            dx = x * (self.viewPortWidth / 2)
            realXVP = (self.viewPortWidth / 2) + dx

            # y
            dy = y * (self.viewPortHeight / 2)
            realYVP = (self.viewPortHeight / 2) + dy

            # Add new viewports 
            realX = realXVP + self.xViewPort
            realY = realYVP + self.yViewPort       

            if ((realX <= self.width) and (realY <= self.height)):
                if (realX == self.width):
                    realX = self.width - 1
                if (realY == self.height): 
                    realY = self.height - 1
                self.framebuffer[math.floor(realY)][math.floor(realX)] = self.newGlColor

    def color(self, r, g, b):
        newR = math.floor(r*255)
        newG = math.floor(g*255)
        newB = math.floor(b*255)

        self.newGlColor = color(newR, newG, newB)
        return self.newGlColor

    def point(self, x, y):
        self.framebuffer[int(y)][int(x)] = self.newGlColor

    def lineBotton(self, x1, y1, x2, y2, cords):
        dx = x2 - x1
        dy = y2 - y1
        startOfY = 1

        if (dy < 0):
            startOfY = -1
            dy = -dy
        
        Directriz = 2*dy - dx
        y = y1

        for x in range(x1, x2):  
            vertex = [x, y]
            self.thisPolygon.append(vertex)
            normX = self.getNormXCoord(x)
            normY = self.getNormYCoord(y)
            self.vertex(normX, normY)
            if (Directriz > 0):
                y = y + startOfY
                Directriz = Directriz - (2*dx)
            
            Directriz = Directriz + (2*dy)

    def lineTop(self, x1, y1, x2, y2, coords):
        dx = x2 - x1
        dy = y2 - y1
        startOfX = 1

        if (dx < 0):
            startOfX = -1
            dx = -dx
        
        Directriz = (2*dx) - dy
        x = x1

        for y in range(y1, y2):  
            vertex = [x, y]
            self.thisPolygon.append(vertex)     
            normX = self.getNormXCoord(x)
            normY = self.getNormYCoord(y)    
            self.vertex(normX, normY )
            if (Directriz > 0):
                x = x + startOfX
                Directriz = Directriz - 2*dy
            
            Directriz = Directriz + 2*dx

    def line(self, x1, y1, x2, y2, coords):

        if abs(y2 - y1) < abs(x2 - x1):
            if (x1 > x2):
                self.lineBotton(x2, y2, x1, y1, coords)
            else:
                self.lineBotton(x1, y1, x2, y2, coords)
        else:
            if (y1 > y2):
                self.lineTop(x2, y2, x1, y1, coords)
            else:
                self.lineTop(x1, y1, x2, y2, coords)
 
    def loadObj(self, filename, coords):
        
        model = obj_loader(filename)
        countOfVertices = len(model.vertices)
        self.thisPolygon = []

        for j in range(1, countOfVertices):
            vertex1 = model.vertices[j - 1]
            vertex2 = model.vertices[j]

            x1 = vertex1[0]
            y1 = vertex1[1]
            x2 = vertex2[0]
            y2 = vertex2[1]

            self.line(x1, y1, x2, y2, coords)

        vertex1 = model.vertices[countOfVertices - 1]
        vertex2 = model.vertices[0]

        x1 = vertex1[0]
        y1 = vertex1[1]
        x2 = vertex2[0]
        y2 = vertex2[1]

        self.line(x1, y1, x2, y2, coords)
        
        xCoords = []

        for vertex in self.thisPolygon:         
            xCoords.append(vertex[0])                        

        xMax = max(xCoords)
        xMin = min(xCoords)

        for y in range (xMin, xMax):
            vertices = list(filter(lambda x: x[0] == y, self.thisPolygon))
            listV = len(vertices)

            for k in range(1, listV, 1):
                vertex1 = vertices[k - 1]
                vertex2 = vertices[k]

                x1 = vertex1[0]
                y1 = vertex1[1]
                x2 = vertex2[0]
                y2 = vertex2[1]

                self.line(x1, y1, x2, y2, False)