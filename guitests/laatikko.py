#!/usr/bin/python

from scipy import *
import pylab
import inrun2
import lento
class Laatikko:
    def __init__(self):
	    pieces=100		#how many pieces in box, at some point more complex geometries!!
            self.Drop=1		#drop from the takeoff
            self.Length=14		#length of the table
            self.Land_Angle=39.*2.*pi/360.	#angle of landing
            self.Land_Height=20		#height of the landing
            self.xland=zeros((pieces,1))
            self.yland=zeros((pieces,1))
            self.curvelength=self.Length+self.Land_Height/sin(self.Land_Angle)	#length of the curve determining the box
            self.ds=self.curvelength/pieces				#steplength along the curve
            for i in range(len(self.xland)-1):
	            if self.xland[i]<self.Length:
	        	    self.xland[i+1]=self.xland[i]+self.ds
	            else:
		            self.xland[i+1]=self.xland[i]+cos(self.Land_Angle)*self.ds
		            self.yland[i+1]=self.yland[i]-sin(self.Land_Angle)*self.ds

    def hit_land(self,t1,sx1,sy1,syloppu):
        self.xland=self.xland+sx1[0]
	self.yland=self.yland+sy1[0]-self.Drop
	indexset=[len(t1)-1,len(self.xland)-1]
        for index in range(len(t1)-1):
            for j in range(len(self.xland)-1):
                    if self.xland[j]>sx1[index] and self.yland[j]>sy1[index] and sy1[index]<0:
                        print "Clear"
                        indexset=[index,j]
			return indexset
        return indexset

def main():
    [t,sx,sy,vx,vy,ax,ay]=inrun2.inrun(0,0,0,0,25,31.*2.*pi/360.,20,5.,31.*2.*pi/360.0,3)
    [kode,sxloppu,syloppu,vxloppu,vyloppu]=inrun2.takeoff2(25,31.*2.*pi/360.,20,5.,31.*2.*pi/360.0,3)
    [t1,sx1,sy1,vx1,vy1,ax1,ay1]=lento.lento(sxloppu,syloppu,vxloppu,vyloppu)
    pylab.plot(sx1,sy1)
    laatikko=Laatikko()
    inddd=laatikko.hit_land(t1,sx1,sy1,syloppu)
    [ind,jj]=inddd
    pylab.plot(sx1[ind],sy1[ind],'o')
    pylab.plot(laatikko.xland[jj],laatikko.yland[jj],'x')
    pylab.plot(laatikko.xland,laatikko.yland)
    pylab.show()
#	#print vy1
				
				
					

if __name__ == '__main__': 
	main()
##rest after
