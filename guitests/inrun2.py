
#!/usr/bin/python
"""
This computes the inrun for the python gui
nothing is final, bugs included
"""
from scipy import *
import pylab
import lento
#constants
#all angles given in radians!!!!

#time steps size, 100seconds / how many steps
steps=2600.
dt=17.0/steps
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
	"""rinnekulma(x,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)
	where 
	x=x-coordinate
	ylengthstr= height of inrun from top to lowest point
	runangle= angle of inrun in radians!!
	radius = radius of transitions
	flat = length of flat before takeoff
	takeoffAngle = angle of takeoff
	takeoffHeight = height of takeoff from lowest point of inrun to end of takeoff

	returns an angle of inrun at current x-coordinate
	in radians
	"""
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
	"""
	invradius(x,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)
	returns inverse radius at x-coord of inrun, used to correct the support force of inrun 
	(and therefore frictional force) in transitions
	"""
	if rinnekulma(x,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)>=runangle or -takeoffAngle>=rinnekulma(x,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight) or abs(rinnekulma(x,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)) == 0:
		return 0
	else:
		return 1./radius
	
def inrun(kalku,valku,sxalku,syalku,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight):
	"""
	kalku=angle of speed at beginning
	valku=velocity at beginning
	sxalku=x-coordinate at begin
	syalku=y-coordinate at begin
	ylengthstr= height of inrun from top to lowest point
	runangle= angle of inrun in radians!!
	radius = radius of transitions
	flat = length of flat before takeoff
	takeoffAngle = angle of takeoff
	takeoffHeight = height of takeoff from lowest point of inrun to end of takeoff

	as in flight.py
	airresistance quadratic wrt speed
	D=0.4 constant from http://biomekanikk.nih.no/xchandbook/ski4.html
	friction coefficient
	C=0.055
	"""
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
	check=0		#this is check code if something is done or not
	
	#forward stepping solution with finite differences for speed  
	for i in range(len(t)-1):
		t[i+1,0]=t[i,0]+dt
		ax[i+1,0]=-sqrt(vx[i,0]**2+vy[i,0]**2)*vx[i,0]*A+g*cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*sin(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))-g*C*cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))+sin(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*(vx[i,0]**2+vy[i,0]**2)*invradius(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)-cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*C*(vx[i,0]**2+vy[i,0]**2)*invradius(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)
		ay[i+1,0]=-g-sqrt(vy[i,0]**2+vx[i,0]**2)*vy[i,0]*A + g*cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))+g*C*cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*sin(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))+cos(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*(vx[i,0]**2+vy[i,0]**2)*invradius(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)+sin(rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight))*C*(vx[i,0]**2+vy[i,0]**2)*invradius(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)		
		vx[i+1,0]=dt*ax[i+1,0]+vx[i,0]
		vy[i+1,0]=dt*ay[i+1,0]+vy[i,0]
		sx[i+1,0]=dt*vx[i+1,0]+sx[i,0]
		sy[i+1,0]=dt*vy[i+1,0]+sy[i,0]
		if rinnekulma(sx[i,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)==0 and check==0:
			check=1
			print "Y-height at the bottom:"
			print sy[i,0]
	
	return [t,sx,sy,vx,vy,ax,ay]
#this is to locate the takeoff
def takeoff2(ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight):
	"""
	takeoff2(ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)
	to compute the information for takeoff
	returns
	array of 5 which includes:
	timestep when at takeoff
	x-coordinate
	y-coodinate
	x-component of speed
	y-component of speed

	"""
	[t,sx,sy,vx,vy,ax,ay]=inrun(runangle,0,0,0,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)
	kode=1
	while rinnekulma(sx[kode,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)>-takeoffAngle and kode<steps:
		kode=kode+1
		if sy[kode,0]+ylengthstr+(radius-cos(runangle)*radius)>takeoffHeight and rinnekulma(sx[kode,0],ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)<0: 
			print "Warniiing!!, takeofHeight reached, but angle not!!! fix your parameters stupid!! \n Angle now:"
			trueAngle=arctan2(sy[kode,0]-sy[kode-1,0],sx[kode,0]-sx[kode-1,0])*360./2./pi
			print trueAngle
			break
		if kode==steps-1: 
		        print "Warning warning, timesteps not reaching takeoff!!"
	while sy[kode,0]+ylengthstr+(radius-cos(runangle)*radius)<takeoffHeight:
		print "angle ok, reaching for height!!"
		kode=kode+1
		if kode>=steps-1:
		        print "Warning warning, timesteps reached max, fix inrun2.py!!"
		        break
	#print kode 
	#print "--maximum--" 
	#print steps
	print "Y-height at the takeoff:"
	print sy[kode,0]

	startAngleTrue=arctan2(sy[30,0]-sy[29,0],sx[30,0]-sx[29,0])*360./2./pi
	print "starting angle as computed:"
	print startAngleTrue
	#same with acceleration
	startAngleTrue=arctan2(ay[30,0],ax[30,0])*360./2./pi
	print "starting angle as computed by acceleration:"
	print startAngleTrue
	trueAngle=arctan2(sy[kode,0]-sy[kode-1,0],sx[kode,0]-sx[kode-1,0])*360./2./pi
	print "takeoffAngle now:"
	print trueAngle
	#same with acceleration 
	trueAngle=arctan2(vy[kode,0],vx[kode,0])*360./2./pi
	print "takeoffAngle now by speed:"
	print trueAngle
	print "Testing Testing"

	pylab.plot(vx[kode,0],vy[kode,0],'o')
	pylab.plot(vx[kode-1,0],vy[kode-1,0],'o')
	return [kode,sx[kode,0],sy[kode,0],vx[kode,0],vy[kode,0]]
	


# include this trick

if __name__ == '__main__': 
##rest after

	radius=15.	#this is global constant, radius of the transitions
	runangle=20.*2.*pi/360.		#angle of the inrun, straight section
	flat=10.		#length of flat section before takeof
	takeoffAngle=46.*2.*pi/360.	#angle of takeoff
	takeoffHeight=5.5  #-(radius-cos(takeoffAngle)*radius)		#height of takeoff
	ylengthstr=31.-(radius-cos(runangle)*radius)	#-yheight when transition starts, 0 is strarting level, 20 radius
	[t,sx,sy,vx,vy,ax,ay]=inrun(runangle,0,0,0,ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)
	[kode,sxloppu,syloppu,vxloppu,vyloppu]=takeoff2(ylengthstr,runangle,radius,flat,takeoffAngle,takeoffHeight)
	pylab.plot(sx[:kode],sy[:kode])
	#print (ylengthstr/tan(runangle)+radius*sin(runangle))+flat
	#print [vxloppu,vyloppu]
	#print sqrt(vxloppu**2+vyloppu**2)
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
