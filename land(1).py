
#!/usr/bin/python

from scipy import *
import pylab
import numpy

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
        self.xx[2]=takesx+length+landheight/tan(landangle*pi*2./360.)

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

    def reset(self,takeheight=1,length=10,landangle=30,landheight=10,takesx=0,takesy=0):
        self.yy[0]=takesy-takeheight
        self.yy[1]=takesy-takeheight
        self.yy[2]=takesy-takeheight-landheight
        self.xx[0]=takesx
        self.xx[1]=takesx+length
        self.xx[2]=takesx+length+landheight/tan(landangle*pi*2./360.)
