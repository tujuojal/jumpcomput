
#!/usr/bin/python

from scipy import *
import pylab
import lento
#constants
#all angles given in radians!!!!

#time steps size, 100seconds / how many steps
steps=300.
dt=7.0/steps
D=.4	#airresistance crossectional constant
g=9.81	#gravity
m=80	#average mass of rider
C=.055	#friction coefficient
A=D/m#	#airresistant coefficient
def tran1(xx,kalku):
	#radius=radius			#radius of a transition from inrun to flat
	yy=sqrt(radius**2-xx**2) 	#y coordinate at position x
	agl=kalku-arcsin(xx/radius) 	#angle at point x
	return [-yy,agl]

#x is position in x-coordinate
#ylengthstr is height of straight section of inrun (before tranny)
#runangle is angle of straight section of inrun
#radius is radius of both, straigh section---flat and flat---takeoff
#flat is length of flat between transitions
#takeoffAngle is angle of takeoff
#takeoffHeight is height of takeoff after the tranny
#
def rinnekulma(x,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight):
	if tan(runangle)*x<ylengthstr:
		y=tan(runangle)
		return runangle
	elif x<=(ylengthstr/tan(runangle)+radius*sin(runangle)):
		return arcsin(((ylengthstr/tan(runangle)+radius*sin(runangle))-x)/radius)
	elif x<((ylengthstr/tan(runangle)+radius*sin(runangle))+flat):
		return 0
	elif x<((ylengthstr/tan(runangle)+radius*sin(runangle))+flat+radius*sin(takeoffAngle)):
		return -arcsin((x-(ylengthstr/(tan(runangle))+radius*sin(runangle))-flat)/radius)
	else:
		return -takeoffAngle

def invradius(x,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight):
	if rinnekulma(x,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)>=runangle or -takeoffAngle+.04>rinnekulma(x,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight) or abs(rinnekulma(x,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)) < 0.01:
		return 0
	else:
		return 1./radius
	
def inrun(kalku,valku,sxalku,syalku,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight):
	#radius = radius# same radius as in tran1, 
	#lasketaan lentorata
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
	vx[0,0]=cos(kalku)*valku
	vy[0,0]=sin(kalku)*valku
	
	#forward stepping solution with finite differences for speed  
	for i in range(len(t)-1):
		t[i+1,0]=t[i,0]+dt
		ax[i+1,0]=-sqrt(vx[i,0]**2+vy[i,0]**2)*vx[i,0]*A+g*cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*sin(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))-g*C*cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))+sin(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*(vx[i,0]**2+vy[i,0]**2)*invradius(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)-cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*C*(vx[i,0]**2+vy[i,0]**2)*invradius(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)
		ay[i+1,0]=-g-sqrt(vy[i,0]**2+vx[i,0]**2)*vy[i,0]*A + g*cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))+g*C*cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*sin(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))+cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*(vx[i,0]**2+vy[i,0]**2)*invradius(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)+sin(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*C*(vx[i,0]**2+vy[i,0]**2)*invradius(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)		
		vx[i+1,0]=dt*ax[i+1,0]+vx[i,0]
		vy[i+1,0]=dt*ay[i+1,0]+vy[i,0]
		sx[i+1,0]=dt*vx[i+1,0]+sx[i,0]
		sy[i+1,0]=dt*vy[i+1,0]+sy[i,0]
		#if rinnekulma(sx[i+1,0])<=-36.*2.*pi/360.:
		#	break	
	
	return [t,sx,sy,vx,vy,ax,ay]
#this is to locate the takeoff
def takeoff2(ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight):
	[t,sx,sy,vx,vy,ax,ay]=inrun(runangle,0,0,0,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)
	kode=1
	while rinnekulma(sx[kode,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)>-takeoffAngle and kode<steps:
		kode=kode+1
		if kode==steps-1: print "Warning warning, timesteps not reaching takeoff!!"
	while sy[kode,0]+ylengthstr<takeoffHeight:
		kode=kode+1
		if kode>=steps-1:print "Warning warning, timesteps reached max, fix inrun2.py!!"
	print kode 
	print "--maximum--" 
	print steps
	return [kode,sx[kode,0],sy[kode,0],vx[kode,0],vy[kode,0]]
	

# include this trick

if __name__ == '__main__': 
##rest after

	radius=20.	#this is global constant, radius of the transitions
	runangle=31.*2.*pi/360.		#angle of the inrun, straight section
	flat=5.		#length of flat section before takeof
	takeoffAngle=31.*2.*pi/360.	#angle of takeoff
	takeoffHeight=1.		#height of takeoff
	ylengthstr=25.-(radius-cos(runangle)*radius)	#-yheight when transition starts, 0 is strarting level, 20 radius
	[t,sx,sy,vx,vy,ax,ay]=inrun(runangle,0,0,0,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)
	[kode,sxloppu,syloppu,vxloppu,vyloppu]=takeoff2(ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)
	pylab.plot(sx[:kode],sy[:kode])
	print (ylengthstr/tan(runangle)+radius*sin(runangle))+flat
	print [vxloppu,vyloppu]
	print sqrt(vxloppu**2+vyloppu**2)
	pylab.plot(sxloppu,syloppu,'o')
	pylab.plot([sxloppu,sxloppu+19,sxloppu+19+tan(35.*2.*pi/360.)*16.],[syloppu-4,syloppu-4,syloppu-4-16])
	[t1,sx1,sy1,vx1,vy1,ax1,ay1]=lento.lento(sxloppu,syloppu,vxloppu,vyloppu)
	pylab.plot(sx1,sy1)
##	pylab.savefig('Lahti_real.png')
	pylab.show()
##	#print ax
##	#for i in range(len(t)-1):
##	#	print rinnekulma(sx[i,0])
#		#print arctan2(vy[i,0],vx[i,0])*360./2./pi
