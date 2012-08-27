
#!/usr/bin/python

from scipy import *
import pylab
radius=20.	#this is global constant, radius of the transitions
runangle=31.*2.*pi/360.		#angle of the inrun, straight section
ylengthstr=25.-(radius-cos(runangle)*radius)	#-yheight when transition starts, 0 is strarting level, 20 radius
def tran1(xx,kalku):
	#radius=radius			#radius of a transition from inrun to flat
	yy=sqrt(radius**2-xx**2) 	#y coordinate at position x
	agl=kalku*2.*pi/360.-arcsin(xx/radius) 	#angle at point x
	return [-yy,agl]


def rinnekulma(x):
	if tan(runangle)*x<ylengthstr:
		y=tan(runangle)
		angle=runangle
	elif x<=(ylengthstr/tan(runangle)+radius*sin(runangle)):
		angle=arcsin(((ylengthstr/tan(runangle)+radius*sin(runangle))-x)/radius)
	else:
		angle=max(-36.*2.*pi/360.,-arcsin((x-(ylengthstr/(tan(runangle))+radius*sin(runangle)))/radius))

	return angle
def invradius(x):
	if rinnekulma(x)>=runangle or -35.*2.*pi/360.>rinnekulma(x):
		return 0
	else:
		return 1./radius
	
def inrun(kalku,valku,sxalku,syalku):
	#radius = radius# same radius as in tran1, 
	#lasketaan lentorata
	#time steps size, 100seconds / how many steps
	steps=500
	dt=13.0/steps
	#constants
	D=.1#.	#airresistance crossectional constant
	g=9.81	#gravity
	m=80	#average mass of rider
	C=0.055	#friction coefficient
	A=D/m#	#airresistant coefficient
	#rinnekulma=kalku*2.0*pi/360.0 #angle of the slope, constant 45, maybe a function of dx at some point
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
		ax[i+1,0]=-sqrt(vx[i,0]**2+vy[i,0]**2)*vx[i,0]*A+g*cos(rinnekulma(sx[i,0]))*sin(rinnekulma(sx[i,0]))-g*C*cos(rinnekulma(sx[i,0]))*cos(rinnekulma(sx[i,0]))+sin(rinnekulma(sx[i,0]))*(vx[i,0]**2+vy[i,0]**2)*invradius(sx[i,0])-cos(rinnekulma(sx[i,0]))*C*(vx[i,0]**2+vy[i,0]**2)*invradius(sx[i,0])
		ay[i+1,0]=-g-sqrt(vy[i,0]**2+vx[i,0]**2)*vy[i,0]*A + g*cos(rinnekulma(sx[i,0]))*cos(rinnekulma(sx[i,0]))+g*C*cos(rinnekulma(sx[i,0]))*sin(rinnekulma(sx[i,0]))+cos(rinnekulma(sx[i,0]))*(vx[i,0]**2+vy[i,0]**2)*invradius(sx[i,0])+sin(rinnekulma(sx[i,0]))*C*(vx[i,0]**2+vy[i,0]**2)*invradius(sx[i,0])		
		vx[i+1,0]=dt*ax[i+1,0]+vx[i,0]
		vy[i+1,0]=dt*ay[i+1,0]+vy[i,0]
		sx[i+1,0]=dt*vx[i+1,0]+sx[i,0]
		sy[i+1,0]=dt*vy[i+1,0]+sy[i,0]
		#if rinnekulma(sx[i+1,0])<=-36.*2.*pi/360.:
		#	break	
	
	return [t,sx,sy,vx,vy,ax,ay]
# include this trick

if __name__ == '__main__': 
#rest after
	[t,sx,sy,vx,vy,ax,ay]=inrun(45,0,0,0)
	#pylab.plot(t,sqrt(vx**2+vy**2))
	pylab.plot(vx,vy)
	pylab.plot(sx,sy)
	pylab.show()
	print (ylengthstr/tan(runangle)+radius*sin(runangle))
	#print ax
	#for i in range(len(t)-1):
	#	print rinnekulma(sx[i,0])
		#print arctan2(vy[i,0],vx[i,0])*360./2./pi
