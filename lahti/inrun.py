
#!/usr/bin/python

from scipy import *
import pylab

	
def inrun(kalku,valku,sxalku,syalku):
	#lasketaan lentorata
	#time steps size, 100seconds / how many steps
	steps=100
	dt=5.0/steps
	#constants
	D=1.3	#airresistance crossectional constant
	g=9.81	#gravity
	m=80	#average mass of rider
	C=0.55	#friction coefficient
	A=D/m#	#airresistant coefficient
	rinnekulma=kalku*2.0*pi/360.0 #angle of the slope, constant 31, maybe a function of dx at some point
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
	vx[0,0]=cos(kalku*pi*2.0/360)*valku
	vy[0,0]=sin(kalku*pi*2.0/360)*valku
	
	#forward stepping solution with finite differences for speed  
	for i in range(len(t)-1):
		t[i+1,0]=t[i,0]+dt
		ax[i+1,0]=-sqrt(vx[i,0]**2+vy[i,0]**2)*vx[i,0]*A + g*cos(rinnekulma)*sin(rinnekulma)
		-g*C*cos(rinnekulma)*cos(rinnekulma)
		ay[i+1,0]=-g-sqrt(vy[i,0]**2+vx[i,0]**2)*vy[i,0]*A + g*cos(rinnekulma)*cos(rinnekulma)
		+g*C*cos(rinnekulma)*sin(rinnekulma)
		vx[i+1,0]=dt*ax[i+1,0]+vx[i,0]
		vy[i+1,0]=dt*ay[i+1,0]+vy[i,0]
		sx[i+1,0]=dt*vx[i+1,0]+sx[i,0]
		sy[i+1,0]=dt*vy[i+1,0]+sy[i,0]
		if sy[i+1,0]<syalku-25:
			break	
	
	return [t,sx,sy,vx,vy,ax,ay]
# include this trick

if __name__ == '__main__': 
#rest after
	[t,sx,sy,vx,vy,ax,ay]=inrun(31,0,0,0)
	pylab.plot(sx,sy)
	pylab.show()
	print sqrt(vx**2+vy**2)
	print sqrt(sx**2+sy**2)
