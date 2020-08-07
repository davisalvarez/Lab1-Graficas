from utilidades import *
from ModeloOBJ import *
import random

def color(r, g, b):
    return bytes([round(b * 255), round(g * 255), round(r * 255)])

BLACK = color(0,0,0)
WHITE = color(1,1,1)
YELLOW = color(1,1,0)

class render(object):

    def __init__(self):
        self.width = 0
        self.height = 0
        self.default_color = BLACK
        self.vetex_color = WHITE
        self.pixels = []
        self.xVP=0
        self.yVP = 0
        self.widthVP = 0
        self.heightVP = 0

    def glInit(self):
        self.iniciarFramebuffer(BLACK)

    def glCreateWindow(self, w, h):
        self.width = w
        self.height = h
        self.iniciarFramebuffer(BLACK)


    def iniciarFramebuffer(self, c):
        self.pixels = []
        for y in range(self.height):
            linea=[]
            for x in range(self.width):
                linea.append(c)
            self.pixels.append(linea)

        #print(str(self.pixels))


        #self.pixels = [ [ BLACK for x in range(self.width)] for y in range(self.height) ]

    def glViewPort(self, x, y, width, height):
        self.xVP= x
        self.yVP = y
        self.widthVP = width
        self.heightVP = height

    def glClear(self):
        self.iniciarFramebuffer(self.default_color)

    def glClearColor(self, r, g, b):
        self.default_color=color(r, g, b)

    def glVertex(self, x, y):
        #pos X
        xIMG = self.xVP + (x+1)* (self.widthVP/2)
        #pos Y
        yIMG = self.yVP + (y+1)*(self.heightVP / 2)

        self.pintarPixelIMG(round(xIMG),round(yIMG))

        #print("x: "+str(xIMG))
        #print("y: " + str(yIMG))


    def pintarPixelIMG(self, x, y, color = None):
        try:

            self.pixels[y][x] = color or self.vetex_color
        except:
            print("pintarPixelIMG() error")

    def glColor(self, r, g, b):
        self.vetex_color=color(r, g, b)

    def glFinish(self):
        self.generar("gotham.bmp")

    def generar(self, filename):

        imagen = open(filename, 'wb')

        #BITMAPFILEHEADER
        #14 Bytes

        imagen.write(bytes('B'.encode('ascii')))
        imagen.write(bytes('M'.encode('ascii')))
        imagen.write(dword(14+40+ self.width * self.height * 3))  #4
        imagen.write(word(0)) #2
        imagen.write(word(0)) #2
        imagen.write(dword(14+40)) #4

        #BITMAPINFOHEADER
        #40 Bytes

        imagen.write(dword(40)) #4
        imagen.write(dword(self.width)) #4
        imagen.write(dword(self.height)) #4
        imagen.write(word(1)) #2
        imagen.write(word(24)) # 2
        imagen.write(dword(0)) # 4
        imagen.write(dword(self.width * self.height * 3))  # 4

        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4

        #self.pixels[11][11]=color(162,0,255)

        for y in range(self.height):
            for x in range(self.width):
                imagen.write(self.pixels[y][x])

        imagen.close()


    def glLine(self, x0, y0, x1, y1):
        # x0: x inicial de la linea
        x0 = round(self.xVP + (x0 + 1) * (self.widthVP / 2))
        # x1: x final de la linea
        x1 = round(self.xVP + (x1 + 1) * (self.widthVP / 2))
        # y0: y inicial de la linea
        y0 = round(self.yVP + (y0 + 1) * (self.heightVP / 2))
        # y1: y final de la linea
        y1 = round(self.yVP + (y1 + 1) * (self.heightVP / 2))

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        cambioPixel = 0
        cambiar = 0.5

        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.pintarPixelIMG(y, x)
            else:
                self.pintarPixelIMG(x, y)

            cambioPixel += m
            if cambioPixel >= cambiar:
                if y1 > y0:
                    y += 1
                else:
                    y -= 1
                cambiar += 1

    def glLineIMG(self, x0, y0, x1, y1):

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        cambioPixel = 0
        cambiar = 0.5

        try:
            m = dy / dx
        except ZeroDivisionError:
            pass
        else:
            y = y0

            for x in range(x0, x1 + 1):
                if steep:
                    self.pintarPixelIMG(y, x)
                else:
                    self.pintarPixelIMG(x, y)

                cambioPixel += m
                if cambioPixel >= cambiar:
                    if y1 > y0:
                        y += 1
                    else:
                        y -= 1
                    cambiar += 1

    def transform(self, vertex, translate=(0,0,0), scale=(1,1,1)):
        return (round(vertex[0]*scale[0] + translate[0]),
                round(vertex[1]*scale[1] + translate[1]))
                #round(vertex[2]*scale[2] + translate[2]))

    def paintModelOBJ(self, filename, translate = (0,0,0), scale = (1,1,1), isWireframe = False):
        model = ModeloOBJ(filename)
        #print(str(model.faces))

        for cara in model.faces:

            vertices = len(cara)

            if isWireframe:

                for vert in range(vertices):
                    v1 = model.vertices[cara[vert][0] - 1]
                    v2 = model.vertices[cara[(vert + 1) % vertices][0]-1]

                    x0 = round(v1[0] * scale[0] + translate[0])
                    y0 = round(v1[1] * scale[0] + translate[0])
                    x1 = round(v2[0] * scale[0] + translate[0])
                    y1 = round(v2[1] * scale[0] + translate[0])

                    #self.pintarPixelIMG(x1, y1)
                    self.glLineIMG(x0, y0, x1, y1)

            else:
                print("cara: " +str(cara))
                pologon= []
                for vert in range(vertices):
                    v1 = model.vertices[cara[vert][0] - 1]
                    x0 = round(v1[0] * scale[0] + translate[0])
                    y0 = round(v1[1] * scale[0] + translate[0])

                    pologon.append([x0,y0])
                self.earClipping(pologon, color(random.randint(0, 255) / 255, random.randint(0, 255)/ 255, random.randint(0, 255)/ 255))


    def paintPoly(self, poly):
        largo = len(poly)

        for point in range(largo):
            v1 = poly[point]
            v2 = poly[(point + 1) % largo]
            self.glLineIMG(v1[0],v1[1],v2[0],v2[1])

    def fillTriangle(self, A, B, C, color = None):

        def flatBottom(v1, v2, v3):

            for y in range(v1[1], v3[1]+1):

                xi = round( v1[0] + (v3[0] - v1[0])/(v3[1] - v1[1])*(y - v1[1]) )
                xf = round( v2[0] + (v3[0] - v2[0])/(v3[1] - v2[1])*(y - v2[1]) )

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf +1):
                    self.pintarPixelIMG(x,y, color)

            #self.paintPoly([v1, v2, v3])

        def flatTop(v1, v2, v3):

            for y in range (v1[1], v3[1]+1):
                xi = round( v2[0] + (v2[0] - v1[0])/(v2[1] - v1[1])*(y - v2[1]) )
                xf = round( v3[0] + (v3[0] - v1[0])/(v3[1] - v1[1])*(y - v3[1]) )

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.pintarPixelIMG(x, y, color)

        #Aseguramos la forma del triangulo

        if A[1] > B[1]:
            A, B = B, A
        if A[1] > C[1]:
            A, C = C, A
        if B[1] > C[1]:
            B, C = C, B
        if A[1]==C[1]:
            return

        if A[1] == B[1]: #flatBottom
            flatBottom(A, B, C)
        elif B[1] == C[1]: #flatTop
            flatTop(A, B, C)
        else: #Otro caso

            xD = A[0] + (C[0] - A[0])/(C[1] - A[1]) * (B[1] - A[1])

            D=(round(xD), B[1])


            #Dividimos el triangulo en 2
            flatBottom(D, B, C)
            flatTop(A, B, D)

    def polyOrientation(self, polygon):
        sumPX = 0
        lar = len(polygon)

        for p in range(lar):
            sumPX += crossProductu(polygon[p], polygon[(p + 1) % lar])
        return sumPX


    def earClipping(self, polygon, _color = None):

        #Calculamos la orientación del poligon
        ori = self.polyOrientation(polygon)

        #verificamos si es CW
        if ori > 0:
            polygon.reverse()
       #print(str(polygon))
        r = 0
        g = 0
        b = 0
        while(len(polygon) >= 3):
            pz = len(polygon)
            pz2 = len(polygon)
            #print("len: "+str(len(polygon)))
            isTriRemove = True
            print(".")

            for point in range(pz):
            #point = 0
            #while(point < pz):
                #if(point+2 >= pz2):
                #    print("STOPPPP!")
                #    break

                print("pz: "+str(pz)+" point: "+str(point)+" len: "+str(len(polygon)))
                v1 = polygon[point]
                v2 = polygon[(point + 1) % pz]
                v3 = polygon[(point + 2) % pz]
                #point += 1
                oriT = self.polyOrientation([v1, v2, v3])

                if oriT > 0:
                    #print(str(oriT)+" > 0")
                    continue

                #verificar si tiene punto adentro
                for x in polygon:
                    d1 = self.polyOrientation([x, v1, v2] )
                    d2 = self.polyOrientation([x, v2, v3])
                    d3 = self.polyOrientation([x, v3, v1])
                    #print("1- "+str(d1)+" 2>"+str(d2)+" 3>"+str(d3))
                    if (d1 > 0 and d2 > 0 and d2 > 0):
                        #tiene punto
                        print("punto!")
                        continue

                r += 0.02
                g += 0.02
                b += 0.02
                #_color = color(r,g,b)
                isTriRemove = False
                self.fillTriangle(v1, v2, v3, _color)
                polygon.remove(polygon[(point + 1) % pz])
                pz2 -= 1
                #pz = len(polygon)
                #self.paintPoly(polygon)
                #if(point > pz):
                break
            if isTriRemove:
                break









    def fillPoly(self, polygon, translate = (0,0,0), scale = (1,1,1)):

        v0 = polygon[0]
        v1 = polygon[1]
        v2 = polygon[2]

        v0 = self.transform(v0, translate, scale)
        v1 = self.transform(v1, translate, scale)
        v2 = self.transform(v2, translate, scale)

        self.earClipping(polygon, color(random.randint(0, 255) / 255, random.randint(0, 255)/ 255, random.randint(0, 255)/ 255) )
        #self.fillTriangle(v0, v1, v2)




















