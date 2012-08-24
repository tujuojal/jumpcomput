#!/usr/bin/python

from scipy import *
import pylab
import inrun

	
def lento(kalku,valku,sxalku,syalku):
	#lasketaan lentorata
	#time steps size, 100seconds / how many steps
	steps=100
	dt=2.5/steps
	#constants
	D=1.3	# airresistance crossectional constant F_d=1/2*ro*v^2*c_d*A
	#where ro=density 1.225, A=crossectional area 1.5 m^2, c_d = drag coeff 1.5 
	g=9.81	#gravity
	m=80	#average mass of rider
	C=0.055	#friction coefficient
	A=D/m#	#airresistant coefficient
	#initialize with
	#zeros
	t=zeros((steps,1))
	sx=zeros((steps,1))
	sy=zeros((steps,1))
	vx=zeros((steps,1))
	vy=zeros((steps,1))
	ax=zeros((steps,1))
	ay=zeros((steps,1))
	sx=zeros((steps,1))
	sy=zeros((steps,1))
	vx[0,0]=cos(kalku*pi*2/360)*valku
	vy[0,0]=sin(kalku*pi*2/360)*valku
	
	#forward stepping solution with finite differences for speed  
	for i in range(len(t)-1):
		t[i+1,0]=t[i,0]+dt
		ax[i+1,0]=-sqrt(vx[i,0]**2+vy[i,0]**2)*vx[i,0]*A
		ay[i+1,0]=-g-sqrt(vy[i,0]**2+vx[i,0]**2)*vy[i,0]*A
		vx[i+1,0]=dt*ax[i+1,0]+vx[i,0]
		vy[i+1,0]=dt*ay[i+1,0]+vy[i,0]
		sx[i+1,0]=dt*vx[i+1,0]+sx[i,0]
		sy[i+1,0]=dt*vy[i+1,0]+sy[i,0]
		
	return [t,sx,sy,vx,vy,ax,ay]

# include this trick

if __name__ == '__main__': 
#rest after
	#[t,sx,sy,vx,vy,ax,ay]=inrun.inrun(45,10,0,0)
	[t1,sx1,sy1,vx1,vy1,ax1,ay1]=lento(36.87,17,0,0)
	
	pylab.plot(sx1,sy1)
	pylab.plot([19,19+cos(35./360.*2.*pi)*31],[-4,-4-sin(35./360.*2.*pi)*31])
	pylab.show()
	print vy1
