
#!/usr/bin/python

from scipy import *
import pylab

	
def inrun(kalku,valku,sxalku,syalku):
	#lasketaan lentorata
	#time steps size, 100seconds / how many steps
	steps=100
	dt=5.0/steps
	#constants
	D=0.25	#airresistance crossectional constant
	g=9.81	#gravity
	m=80	#average mass of rider
	C=0.055	#friction coefficient
	A=D/m#	#airresistant coefficient
	#initialize with
	#zeros
	#direction positive is upwards (and right) 
	t=zeros((steps,1))
	sx=zeros((steps,1))
	sy=zeros((steps,1))
	vx=zeros((steps,1))
	vy=zeros((steps,1))
	ax=zeros((steps,1))
	ay=zeros((steps,1))
	sx=zeros((steps,1))
	sy=zeros((steps,1))
	vx[0,0]=cos(kalku+0*pi*2.0/360)*valku
	vy[0,0]=sin(kalku+0*pi*2.0/360)*valku
	
	#forward stepping solution with finite differences for speed  
	for i in range(len(t)-1):
		t[i+1,0]=t[i,0]+dt
		ax[i+1,0]=-sqrt(vx[i,0]**2+vy[i,0]**2)*vx[i,0]*A + g*cos(1.0*2.0*pi/360.0)*C*cos(1.0*2.0*pi/360.0)
		ay[i+1,0]=-g-sqrt(vy[i,0]**2+vx[i,0]**2)*vy[i,0]*A - g*cos(1.0*2.0*pi/360.0)*C*sin(1.0*2.0*pi/360.0)
		vx[i+1,0]=dt*ax[i+1,0]+vx[i,0]
		vy[i+1,0]=dt*ay[i+1,0]+vy[i,0]
		sx[i+1,0]=dt*vx[i+1,0]+sx[i,0]
		sy[i+1,0]=dt*vy[i+1,0]+sy[i,0]
		
	
	pylab.plot(sx+sxalku,sy+syalku)
	pylab.show()
	return [t,sx,sy,vx,vy,ax,ay]
inrun(0,0,0,0)
