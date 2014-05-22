
#!/usr/bin/python

from scipy import *
import pylab
import numpy 
import scipy.interpolate as interpolate

class Land:
    def __init__(self,takeheight=1,length=10,landangle=30,landheight=10,takesx=0,takesy=0):
        """
        muodestetaan simppeli geometria hyppyrille
        """
        self.yy=numpy.zeros(3)
        self.xx=numpy.zeros(3)	
        self.yy[0]=takesy-takeheight
        self.yy[1]=takesy-takeheight
        self.yy[2]=takesy-takeheight-landheight
        self.xx[0]=takesx
        self.xx[1]=takesx+length
        self.xx[2]=takesx+length+(landheight)/tan(landangle*pi*2./360.)
        self.angle=landangle*pi*2./360.
        self.r=5 #radius of the knuckle
#pitää vielä lisätä numpy.linspace(alku,loppu,lkmäärä) x-koordinaatteja joiden kanssa
#saisi tuon geometrian plottia varten paremmin kun tuo pallo on pyöreä eikä kulma

    def osu(self,lento):
        """
        syotetaan lentorata ja lasketaan osuuko alastuloon ja milla indeksilla
        """
    for val in range(len(lento.sy)):
        if lento.sy[val]<alasgeom(lento.sx[val]):
            print "ONNISTUU!!:"
            return val
    return len(lento.sx)

    ##This one is more advanced geometry, nothing huge but a round knuckle
    def alasgeom(self,x):
        xx2=numpy.array(self.xx,dtype=float)
        yy2=numpy.array(self.yy,dtype=float)
        p2=interpolate.PiecewisePolynomial(xx2,yy2[:,numpy.newaxis])
        centerx=self.xx[1]-self.r*tan(self.angle/2.) #this is x coord of the center of circle of the knuckle
        if (x < centerx):
            return self.yy[1]
        elif (x < centerx + self.r*sin(self.angle)):
            return sqrt(self.r**2 - (x - centerx)**2) + (self.yy[1]-self.r)
        else:
            return p2(x)


    def reset(self,takeheight=1,length=10,landangle=30,landheight=10,takesx=0,takesy=0):
        self.yy[0]=takesy-takeheight
        self.yy[1]=takesy-takeheight
        self.yy[2]=takesy-takeheight-landheight
        self.xx[0]=takesx
        self.xx[1]=takesx+length
        self.xx[2]=takesx+length+landheight/tan(landangle*pi*2./360.)
        self.angle=landangle*pi*2./360.
