
#!/usr/bin/python
"""
This computes the inrun for the python gui
nothing is final, bugs included
"""
from scipy import *
import pylab
import lento2
#constants
#all angles given in radians!!!!
class Inrun:
	def __init__(self,ylengthstr=25,runangle=30.*2.*pi/360.,radius=30,flat=5,radius2=20,takeoffAngle=25.*2.*pi/360.,takeoffHeight=3):
		self.ylengthstr=ylengthstr
		self.runangle=runangle
		self.radius=radius
		self.flat=flat
		self.radius2=radius2
		self.takeoffAngle=takeoffAngle
		self.takeoffHeight=takeoffHeight
		#time steps size, 100seconds / how many steps
		self.steps=4600.
		self.dt=27.0/self.steps
		self.D=.4	#airresistance coefficient, old one
		self.g=9.81	#gravity
		self.m=80	#average mass of rider
		self.C=.055	#friction coefficient
		self.A=self.D/self.m #airresistant coefficient for accel, mass divided out


		self.t=zeros((self.steps,1))
		self.sx=zeros((self.steps,1))
		self.sy=zeros((self.steps,1))
		self.vx=zeros((self.steps,1))
		self.vy=zeros((self.steps,1))
		self.ax=zeros((self.steps,1))
		self.ay=zeros((self.steps,1))
		self.sx=zeros((self.steps,1))
		self.sy=zeros((self.steps,1))
		#x is position in x-coordinate
		#ylengthstr is height of straight section of inrun (before tranny)
		#runangle is angle of straight section of inrun
		#radius is radius of both, straigh section---flat and flat---takeoff
		#flat is length of flat between transitions
		#takeoffAngle is angle of takeoff
		#takeoffHeight is height of takeoff after the tranny
		#
	def rinnekulma(self,x):
		"""rinnekulma(x)
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
		if tan(self.runangle)*x<self.ylengthstr:
			y=tan(self.runangle)
			return self.runangle
		elif x<=(self.ylengthstr/tan(self.runangle)+self.radius*sin(self.runangle)):
			return arcsin(((self.ylengthstr/tan(self.runangle)+self.radius*sin(self.runangle))-x)/self.radius)
		elif x<((self.ylengthstr/tan(self.runangle)+self.radius*sin(self.runangle))+self.flat):
			return 0
		elif x<((self.ylengthstr/tan(self.runangle)+self.radius*sin(self.runangle))+self.flat+self.radius2*sin(self.takeoffAngle)):
			return -arcsin((x-(self.ylengthstr/(tan(self.runangle))+self.radius*sin(self.runangle))-self.flat)/self.radius2)
		else:
			return -self.takeoffAngle

	def invradius(self,x):
		"""
		invradius(x)
		returns inverse radius at x-coord of inrun, used to correct the support force of inrun
		(and therefore frictional force) in transitions
		"""
		if self.rinnekulma(x)>=self.runangle or -self.takeoffAngle>=self.rinnekulma(x) or abs(self.rinnekulma(x)) == 0:
			return 0
		elif self.rinnekulma(x)<0:
			return 1./self.radius2
                else:
                	return 1./self.radius

	def inrun(self):
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
		check=0		#this is check code if something is done or not

		#forward stepping solution with finite differences for speed
		for i in range(len(self.t)-1):
			rk=self.rinnekulma(self.sx[i,0])
			self.t[i+1,0]=self.t[i,0]+self.dt
			self.ax[i+1,0]=-sqrt(self.vx[i,0]**2+self.vy[i,0]**2)*self.vx[i,0]*self.A+self.g*cos(rk)*sin(rk)-self.g*self.C*cos(rk)*cos(rk)+sin(rk)*(self.vx[i,0]**2+self.vy[i,0]**2)*self.invradius(self.sx[i,0])-cos(rk)*self.C*(self.vx[i,0]**2+self.vy[i,0]**2)*self.invradius(self.sx[i,0])
			self.ay[i+1,0]=-self.g-sqrt(self.vy[i,0]**2+self.vx[i,0]**2)*self.vy[i,0]*self.A + self.g*cos(rk)*cos(rk)+self.g*self.C*cos(rk)*sin(rk)+cos(rk)*(self.vx[i,0]**2+self.vy[i,0]**2)*self.invradius(self.sx[i,0])+sin(rk)*self.C*(self.vx[i,0]**2+self.vy[i,0]**2)*self.invradius(self.sx[i,0])
			self.vx[i+1,0]=self.dt*self.ax[i+1,0]+self.vx[i,0]

			self.vy[i+1,0]=self.dt*self.ay[i+1,0]+self.vy[i,0]
			self.sx[i+1,0]=self.dt*self.vx[i+1,0]+self.sx[i,0]
			self.sy[i+1,0]=self.dt*self.vy[i+1,0]+self.sy[i,0]
			if rk==0 and check==0:
				check=1
				print "Y-height at the bottom:"
				print self.sy[i,0]

	#this is to locate the takeoff
	def takeoff2(self):
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
		kode=1
		while self.rinnekulma(self.sx[kode,0])>-self.takeoffAngle and kode+10<self.steps:
			kode=kode+1
			if self.sy[kode,0]+self.ylengthstr+(self.radius-cos(self.runangle)*self.radius)>self.takeoffHeight and self.rinnekulma(self.sx[kode,0])<0:
				print "Warniiing!!, takeofHeight reached, but angle not!!! fix your parameters stupid!! \n Angle now:"
				trueAngle=arctan2(self.sy[kode,0]-self.sy[kode-1,0],self.sx[kode,0]-self.sx[kode-1,0])*360./2./pi
				print trueAngle
				break
			if kode==self.steps-1:
			        print "Warning warning, timesteps not reaching takeoff!!"
		while self.sy[kode,0]+self.ylengthstr+(self.radius-cos(self.runangle)*self.radius)<self.takeoffHeight:
			print "angle ok, reaching for height!!"
			kode=kode+1
			if kode>=self.steps-1:
			        print "Warning warning, timesteps reached max, fix inrun2.py!!"
			        break
		#print kode
		#print "--maximum--"
		#print steps
		print "Y-height at the takeoff:"
		print self.sy[kode,0]

		startAngleTrue=arctan2(self.sy[30,0]-self.sy[29,0],self.sx[30,0]-self.sx[29,0])*360./2./pi
		print "starting angle as computed:"
		print startAngleTrue
		#same with acceleration
		startAngleTrue=arctan2(self.ay[30,0],self.ax[30,0])*360./2./pi
		print "starting angle as computed by acceleration:"
		print startAngleTrue
		trueAngle=arctan2(self.sy[kode,0]-self.sy[kode-1,0],self.sx[kode,0]-self.sx[kode-1,0])*360./2./pi
		print "takeoffAngle now:"
		print trueAngle
		#same with acceleration
		trueAngle=arctan2(self.vy[kode,0],self.vx[kode,0])*360./2./pi
		print "takeoffAngle now by speed:"
		print trueAngle
		print "Testing Testing"

	#	pylab.plot(self.vx[kode,0],self.vy[kode,0],'o')
	#	pylab.plot(self.vx[kode-1,0],self.vy[kode-1,0],'o')
		return kode


	# include this trick

if __name__ == '__main__':
##rest after
	radius=45.	#this is global constant, radius of the transition1
	radius2=5.	#this is global constant, radius of the transition2
	runangle=20.*2.*pi/360.		#angle of the inrun, straight section
	flat=10.		#length of flat section before takeof
	takeoffAngle=46.*2.*pi/360.	#angle of takeoff
	takeoffHeight=5.5  #-(radius-cos(takeoffAngle)*radius)		#height of takeoff
	ylengthstr=31.-(radius-cos(runangle)*radius)	#-yheight when transition starts, 0 is strarting level, 20 radius
	inr=Inrun(ylengthstr,runangle,radius,flat,radius2,takeoffAngle,takeoffHeight)
	inr.inrun()
	kode=inr.takeoff2()
	pylab.plot(inr.sx[:kode],inr.sy[:kode])
	#print (ylengthstr/tan(runangle)+radius*sin(runangle))+flat
	#print [vxloppu,vyloppu]
	#print sqrt(vxloppu**2+vyloppu**2)
	pylab.plot(inr.sx[kode,0],inr.sy[kode,0],'o')
	sxloppu=inr.sx[kode,0]
	syloppu=inr.sy[kode,0]
	vxloppu=inr.vx[kode,0]
	vyloppu=inr.vy[kode,0]
	pylab.plot([sxloppu,sxloppu+19,sxloppu+19+tan(35.*2.*pi/360.)*16.],[syloppu-4,syloppu-4,syloppu-4-16])
	lent=lento2.Lento(sxloppu,syloppu,vxloppu,vyloppu)
	pylab.plot(lent.sx,lent.sy)
#		pylab.savefig('Lahti_real.png')
	pylab.show()
##	#print ax
##	#for i in range(len(t)-1):
##	#	print rinnekulma(sx[i,0])
#		#print arctan2(vy[i,0],vx[i,0])*360./2./pi
