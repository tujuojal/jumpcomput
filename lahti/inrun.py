
#!/usr/bin/python

from scipy import *
import pylab

def tran1(xx,kalku):
	radius=20 			#radius of a transition from inrun to flat
	yy=sqrt(radius**2-xx**2) 	#y coordinate at position x
	agl=kalku*2.*pi/360.-arcsin(xx/radius) 	#angle at point x
	return [-yy,agl]

def rinnekulma(x):
	if tan(31.*2.*pi/360.)*x<25:
		y=tan(31.*2.*pi/360.)
		angle=31.*2.*pi/360.
	else:
		angle=max(-36.*2.*pi/360.,31.*2.*pi/360.-arcsin((x-25./tan(31.*2.*pi/360.))/20.))
	return angle

	
def inrun(kalku,valku,sxalku,syalku):
	#lasketaan lentorata
	#time steps size, 100seconds / how many steps
	steps=200
	dt=7.0/steps
	#constants
	D=1.	#airresistance crossectional constant
	g=9.81	#gravity
	m=80	#average mass of rider
	C=0.55	#friction coefficient
	A=D/m#	#airresistant coefficient
	#rinnekulma=kalku*2.0*pi/360.0 #angle of the slope, constant 31, maybe a function of dx at some point
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
		ax[i+1,0]=-sqrt(vx[i,0]**2+vy[i,0]**2)*vx[i,0]*A + g*cos(rinnekulma(sx[i,0]))*sin(rinnekulma(sx[i,0]))
		-g*C*cos(rinnekulma(sx[i,0]))*cos(rinnekulma(sx[i,0]))
		ay[i+1,0]=-g-sqrt(vy[i,0]**2+vx[i,0]**2)*vy[i,0]*A + g*cos(rinnekulma(sx[i,0]))*cos(rinnekulma(sx[i,0]))
		+g*C*cos(rinnekulma(sx[i,0]))*sin(rinnekulma(sx[i,0]))
		vx[i+1,0]=dt*ax[i+1,0]+vx[i,0]
		vy[i+1,0]=dt*ay[i+1,0]+vy[i,0]
		sx[i+1,0]=dt*vx[i+1,0]+sx[i,0]
		sy[i+1,0]=dt*vy[i+1,0]+sy[i,0]
		if rinnekulma(sx[i+1,0])<-36.*2.*pi/360.:
			break	
	
	return [t,sx,sy,vx,vy,ax,ay]
# include this trick

if __name__ == '__main__': 
#rest after
	[t,sx,sy,vx,vy,ax,ay]=inrun(31,0,0,0)
	pylab.plot(t,sqrt(vx**2+vy**2))
	pylab.plot(sx,sy)
	pylab.plot(vx,vy)
	pylab.show()
	for i in range(len(t)-1):
		print rinnekulma(sx[i,0])*360./2./pi
		print arctan(vy[i,0]/vx[i,0])*360./2./pi
		#print 31.*2.*pi/360.-arcsin((27.-25./tan(31.*2.*pi/360.))/20.)*360./2./pi
