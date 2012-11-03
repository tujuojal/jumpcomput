#!/usr/bin/python

from scipy import *
import pylab
import inrun2

class Lento:
	def __init__(self,sxalku=0,syalku=0,vxalku=7,vyalku=5):
		#lasketaan lentorata
		#time steps size, 100seconds / how many steps
		steps=200
		self.dt=4.5/steps
		#constants
		self.D=0.4#1.	#maybe 1.3?	# airresistance crossectional constant F_d=1/2*ro*v^2*c_d*A
		#where ro=density 1.225, A=crossectional area 1.5 m^2, c_d = drag coeff 1.5 
		self.g=9.81	#gravity
		self.m=80	#average mass of rider
		self.C=0.055	#friction coefficient
		self.A=self.D/self.m#	#airresistant coefficient
		self.sxalku=sxalku
		self.syalku=syalku
		self.vxalku=vxalku
		self.vyalku=vyalku
		#initialize with
		#zeros
		self.t=zeros((steps,1))
		self.sx=zeros((steps,1))
		self.sy=zeros((steps,1))
		self.vx=zeros((steps,1))
		self.vy=zeros((steps,1))
		self.ax=zeros((steps,1))
		self.ay=zeros((steps,1))
		self.sx=zeros((steps,1))
		self.sy=zeros((steps,1))
		self.vx[0,0]=vxalku
		self.vy[0,0]=vyalku
		self.sx[0,0]=sxalku
		self.sy[0,0]=syalku
	
		#forward stepping solution with finite differences for speed  
		for i in range(len(self.t)-1):
			self.t[i+1,0]=self.t[i,0]+self.dt
			self.ax[i+1,0]=-sqrt(self.vx[i,0]**2+self.vy[i,0]**2)*self.vx[i,0]*self.A
			self.ay[i+1,0]=-self.g-sqrt(self.vy[i,0]**2+self.vx[i,0]**2)*self.vy[i,0]*self.A
			self.vx[i+1,0]=self.dt*self.ax[i+1,0]+self.vx[i,0]
			self.vy[i+1,0]=self.dt*self.ay[i+1,0]+self.vy[i,0]
			self.sx[i+1,0]=self.dt*self.vx[i+1,0]+self.sx[i,0]
			self.sy[i+1,0]=self.dt*self.vy[i+1,0]+self.sy[i,0]
		
	def laske(self,sxalku=0,syalku=0,vxalku=7,vyalku=5):
		#forward stepping solution with finite differences for speed  
		self.vx[0,0]=vxalku
		self.vy[0,0]=vyalku
		self.sx[0,0]=sxalku
		self.sy[0,0]=syalku
		for i in range(len(self.t)-1):
			self.t[i+1,0]=self.t[i,0]+self.dt
			self.ax[i+1,0]=-sqrt(self.vx[i,0]**2+self.vy[i,0]**2)*self.vx[i,0]*self.A
			self.ay[i+1,0]=-self.g-sqrt(self.vy[i,0]**2+self.vx[i,0]**2)*self.vy[i,0]*self.A
			self.vx[i+1,0]=self.dt*self.ax[i+1,0]+self.vx[i,0]
			self.vy[i+1,0]=self.dt*self.ay[i+1,0]+self.vy[i,0]
			self.sx[i+1,0]=self.dt*self.vx[i+1,0]+self.sx[i,0]
			self.sy[i+1,0]=self.dt*self.vy[i+1,0]+self.sy[i,0]
	
# include this trick
def main():
#	[t,sx,sy,vx,vy,ax,ay]=inrun2.inrun(45,10,0,0)
	lent=Lento(0,0,7,5)
	lent.laske(10,2,5,19)
	
	pylab.plot(lent.sx,lent.sy)
	pylab.plot([0,19,19+cos(35./360.*2.*pi)*31],[0,-4,-4-sin(35./360.*2.*pi)*31])
	pylab.show()
	#print vy1
if __name__ == '__main__': 
	main()
