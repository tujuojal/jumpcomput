#!/usr/bin/python

from scipy import *
import scipy.integrate as integrate
import pylab
import numpy

class Lento:
    def __init__(self,sxalku=0,syalku=0,vxalku=7,vyalku=5):
        #lasketaan lentorata
        #time steps size, 100seconds / how many steps
        self.steps=20
        self.Time = 4.5
        self.dt = self.Time/self.steps
        #constants
        self.D=0.4#1.	#maybe 1.3?	# airresistance crossectional constant F_d=1/2*ro*v^2*c_d*A
        #where ro=density 1.225, A=crossectional area 1.5 m^2, c_d = drag coeff 1.5
        self.g=9.81	#gravity
        self.m=80	#average mass of rider
        self.C=0.055	#friction coefficient
        self.A=self.D/self.m	#airresistant coefficient when mass divided ou, for acceleration, not for force
        self.sxalku=sxalku
        self.syalku=syalku
        self.vxalku=vxalku
        self.vyalku=vyalku
        #initialize with
        #zeros
        self.t=numpy.zeros(self.steps)
        self.sx=numpy.zeros(self.steps)
        self.sy=numpy.zeros(self.steps)
        self.vx=numpy.zeros(self.steps)
        self.vy=numpy.zeros(self.steps)
        self.ax=numpy.zeros(self.steps)
        self.ay=numpy.zeros(self.steps)
        self.sx=numpy.zeros(self.steps)
        self.sy=numpy.zeros(self.steps)
        self.vx[0]=vxalku
        self.vy[0]=vyalku
        self.sx[0]=sxalku
        self.sy[0]=syalku

        #forward stepping solution with finite differences for speed
        for i in range(len(self.t)-1):
            self.t[i+1]=self.t[i]+self.dt
            self.ax[i+1]=-sqrt(self.vx[i]**2+self.vy[i]**2)*self.vx[i]*self.A
            self.ay[i+1]=-self.g-sqrt(self.vy[i]**2+self.vx[i]**2)*self.vy[i]*self.A
            self.vx[i+1]=self.dt*self.ax[i+1]+self.vx[i]
            self.vy[i+1]=self.dt*self.ay[i+1]+self.vy[i]
            self.sx[i+1]=self.dt*self.vx[i+1]+self.sx[i]
            self.sy[i+1]=self.dt*self.vy[i+1]+self.sy[i]

    def laske(self,sxalku=0,syalku=0,vxalku=7,vyalku=5):
        #forward stepping solution with finite differences for speed
        self.vx[0]=vxalku
        self.vy[0]=vyalku
        self.sx[0]=sxalku
        self.sy[0]=syalku
        for i in range(len(self.t)-1):
            self.t[i+1]=self.t[i]+self.dt
            self.ax[i+1]=-sqrt(self.vx[i]**2+self.vy[i]**2)*self.vx[i]*self.A
            self.ay[i+1]=-self.g-sqrt(self.vy[i]**2+self.vx[i]**2)*self.vy[i]*self.A
            self.vx[i+1]=self.dt*self.ax[i+1]+self.vx[i]
            self.vy[i+1]=self.dt*self.ay[i+1]+self.vy[i]
            self.sx[i+1]=self.dt*self.vx[i+1]+self.sx[i]
            self.sy[i+1]=self.dt*self.vy[i+1]+self.sy[i]

    def f(self,u,time):
        vx,vy,sx,sy  = u
        ret_1 = -sqrt(vx**2+vy**2)*vx*self.A
        ret_2 = -self.g - sqrt(vy**2+vx**2)*vy*self.A
        ret_3 = vx
        ret_4 = vy
        return [ret_1, ret_2, ret_3, ret_4]

    def ratkaise(self,sxalku=0,syalku=0,vxalku=7,vyalku=5):
        tt = pylab.linspace(0,self.Time,num=self.steps,endpoint=False)
        alkuarvot=[vxalku,vyalku,sxalku,syalku] #this says startposition and speed are according
        u = integrate.odeint(self.f,alkuarvot,tt)
        self.vx,self.vy,self.sx,self.sy = u.T 
        return u
# include this trick
def main():
#	[t,sx,sy,vx,vy,ax,ay]=inrun2.inrun(45,10,0,0)
    lent=Lento(0,0,7,5)
    lent.ratkaise(10,2,5,19)

    pylab.plot(lent.sx,lent.sy)
    pylab.plot([0,19,19+cos(35./360.*2.*pi)*31],[0,-4,-4-sin(35./360.*2.*pi)*31])
    pylab.show()
#print vy1
if __name__ == '__main__':
    main()
