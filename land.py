
#!/usr/bin/python
import matplotlib
matplotlib.use("agg")
from numpy import pi, sin, tan, sqrt
import pylab
import numpy

class Land:
    def __init__(self,takeheight=1,length=10,landangle=30,landheight=10,takesx=0,takesy=0):
        """
        muodestetaan simppeli geometria hyppyrille
        """
        self.yy_info=numpy.zeros(3)
        self.xx_info=numpy.zeros(3)
        self.yy_info[0]=takesy-takeheight
        self.yy_info[1]=takesy-takeheight
        self.yy_info[2]=takesy-takeheight-landheight
        self.xx_info[0]=takesx
        self.xx_info[1]=takesx+length
        self.xx_info[2]=takesx+length+(landheight)/tan(landangle*pi*2./360.)
        self.angle=landangle*pi*2./360.
        self.r=15 #radius of the knuckle
        self.xx = numpy.linspace(self.xx_info[0],self.xx_info[2],50) #this is saying that 50 points to define the geometry piecewise
        self.yy = numpy.zeros(len(self.xx)) #this is initialization of the yy coordinates
        for i in range(len(self.xx)):
            self.yy[i] = self.alasgeom(self.xx[i])
        #this is just construction of the geometry via alasgeom function

    def osu(self,lento):
        """
        syotetaan lentorata ja lasketaan osuuko alastuloon ja milla indeksilla
        """
        for val in range(len(lento.sy)):
            if lento.sy[val]<self.alasgeom(lento.sx[val]):
                print("ONNISTUU!!:")
                return val
        return len(lento.sx)

    def alasgeom(self,x):
        centerx=self.xx_info[1]-self.r*tan(self.angle/2.)
        if (x < centerx):
            return self.yy_info[1]
        elif (x < centerx + self.r*sin(self.angle)):
            return sqrt(self.r**2 - (x - centerx)**2) + (self.yy_info[1]-self.r)
        else:
            # straight slope tangent to the arc at the knuckle exit point
            x_end = centerx + self.r*sin(self.angle)
            y_end = self.r*numpy.cos(self.angle) + self.yy_info[1] - self.r
            return y_end - (x - x_end)*numpy.tan(self.angle)


    def reset(self,takeheight=1,length=10,landangle=30,landheight=10,takesx=0,takesy=0):
        self.yy_info[0]=takesy-takeheight
        self.yy_info[1]=takesy-takeheight
        self.yy_info[2]=takesy-takeheight-landheight
        self.xx_info[0]=takesx
        self.xx_info[1]=takesx+length
        self.xx_info[2]=takesx+length+landheight/tan(landangle*pi*2./360.)
        self.angle=landangle*pi*2./360.
        self.xx = numpy.linspace(self.xx_info[0],self.xx_info[2],30) #this is saying that 30 points to define the geometry piecewise
        self.yy = numpy.zeros(len(self.xx)) #this is initialization of the yy coordinates
        for i in range(len(self.xx)):
            self.yy[i] = self.alasgeom(self.xx[i])
        #this is just construction of the geometry via alasgeom function
