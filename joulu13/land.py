
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

    def osu(self,lento):
        """
        syotetaan lentorata ja lasketaan osuuko alastuloon ja milla indeksilla
        """
        for i in range(len(lento.t)-1):
            if (lento.sx[i]<self.xx[1] and lento.sy[i]<self.yy[0]):
                return i
            elif (lento.sx[i]<self.xx[2] and lento.sy[i]<(-self.yy[1]+(self.yy[1]-self.yy[2])*(lento.sx[i]-self.xx[1])/(self.xx[2]-self.xx[1]))):
                print (lento.sx[i]-self.xx[1])/(self.xx[2]-self.xx[1])
                return i
            elif lento.sx[i]>self.xx[2]:
                return i
            else:
                print "not hitting landing yet..."
        print "something wrong!!! landing not seen!!"
        return -1
    ##This one is more advanced geometry, nothing huge but round nuckle
    def alasgeom(self,x):
        xx2=np.array(self.xx,dtype=float)
        yy2=np.array(self.yy,dtype=float)
        p2=interpolate.PiecewisePolynomial(xx2,yy2[:,np.newaxis])
        centerx=self.xx[1]-r*tan(self.angle/2.) #this is x coord of the center of circle of the knuckle
        if (x < centerx):
            return self.yy[1]
        elif (x < centerx + r*sin(self.angle)):
            return sqrt(r**2 - (x - centerx)**2) - (self.yy[1]-r)
        else
            return p2(x)


    def reset(self,takeheight=1,length=10,landangle=30,landheight=10,takesx=0,takesy=0):
        self.yy[0]=takesy-takeheight
        self.yy[1]=takesy-takeheight
        self.yy[2]=takesy-takeheight-landheight
        self.xx[0]=takesx
        self.xx[1]=takesx+length
        self.xx[2]=takesx+length+landheight/tan(landangle*pi*2./360.)
        self.angle=landangle*pi*2./360.
