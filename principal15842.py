"""
UVG
GRAFICAS POR COMPUTADORA - seccion 20

Davis Alvarez - 15842

SR1: Points
"""
from render import *

img = render()

img.glInit() #5
img.glCreateWindow(1000,500) #5
img.glClearColor(0.5,1,0.36) #10
img.glClear() #20
img.glViewPort(1,1,398,398) #10
img.glColor(0,0,0)#15
#img.glVertex(0.75,0.12)#30

poli1 = [(165, 380), (185, 360), (180, 330), (207, 345),
         (233, 330), (230, 360), (250, 380), (220, 385),
         (205, 410), (193, 383)]

poli2 = [(321, 335), (288, 286), (339, 251), (374, 302)]

poli3 = [(377, 249), (411, 197), (436, 249)]

poli4 = [(413, 177), (448, 159), (502, 88), (553, 53),
         (535, 36), (676, 37), (660, 52), (750, 145),
         (761, 179), (672, 192), (659, 214), (615, 214),
         (632, 230), (580, 230), (597, 215), (552, 214),
         (517, 144), (466, 180)]

poli5 = [(682, 175), (708, 120), (735, 148), (739, 170)]

img.paintPoly(poli1)
img.paintPoly(poli2)
img.paintPoly(poli3)
img.paintPoly(poli4)
img.paintPoly(poli5)


img.glFinish() #5






