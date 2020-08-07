
import struct

#Reserva 1 Byte en memoria
def char(c):
    return struct.pack('=c', c.enconde('ascii'))

#Reserva 2 Byte en memoria
def word(w):
    return struct.pack('=h',w)

#Reserva 4 Byte en memoria
def dword(d):
    return struct.pack('=l',d)

def crossProductu(pointA, pointB):
    return (pointA[0]*pointB[1]) - (pointA[1]*pointB[0])