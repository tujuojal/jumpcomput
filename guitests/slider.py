#!/usr/bin/python
# -*- coding: utf-8 -*-
#this is with python3 not backwards compatible!!

import wx
import numpy
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from lento import lento
from inrun2 import inrun
from inrun2 import takeoff2
from scipy import *

class Example(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw) 
        

        #constants, aka variables that will be binded to sliders
	self.radius=20.	#this is global constant, radius of the transitions
	self.runangle=31.*2.*pi/360.		#angle of the inrun, straight section
	self.flat=10.		#length of flat section before takeof
	self.takeoffAngle=31.*2.*pi/360.	#angle of takeoff
	self.takeoffHeight=3.5  		#height of takeoff
	self.ylengthstr=25.-(self.radius-cos(self.runangle)*self.radius)	#-yheight when transition starts, 0 is strarting level, 20 radius

        self.InitUI()
        self.drawFigure()
        

    def InitUI(self):   

        self.sp = wx.SplitterWindow(self)
        pnl = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)

        # in panel2 we have the figure
        self.pnl2 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)

        self.sp.SplitVertically(pnl,self.pnl2,300)

        button = wx.Button(pnl, label='Redraw', pos=(20, 20))
        text = wx.CheckBox(pnl, label='CheckBox', pos=(120, 50))
        combo = wx.ComboBox(pnl, pos=(120, 22), choices=['Python', 'Ruby'])
        self.slider = wx.Slider(pnl, 1, 20, 10, 30, (120, 100), (110, -1),style=wx.SL_LABELS)	#radius       
        self.slider2 = wx.Slider(pnl, 2, 30, 10, 40, (120, 150), (110, -1),style=wx.SL_LABELS) 	#runangle
        self.slider3 = wx.Slider(pnl, 3, 10, 1, 20, (120, 200), (110, -1),style=wx.SL_LABELS) 	#flat
        self.slider4 = wx.Slider(pnl, 4, 31, 10, 40, (120, 250), (110, -1),style=wx.SL_LABELS) 	#takeoffAngle
        self.slider5 = wx.Slider(pnl, 5, 3, 1, 4, (120, 300), (110, -1),style=wx.SL_LABELS) 	#takeoffHeight
        self.slider6 = wx.Slider(pnl, 6, 25, 10, 40, (120, 350), (110, -1),style=wx.SL_LABELS) 	#ylengthstr

        self.slider.Bind(wx.EVT_SCROLL, self.OnScroll, id=1)
        self.slider2.Bind(wx.EVT_SCROLL, self.OnScroll, id=2)
        self.slider3.Bind(wx.EVT_SCROLL, self.OnScroll, id=3)
        self.slider4.Bind(wx.EVT_SCROLL, self.OnScroll, id=4)
        self.slider5.Bind(wx.EVT_SCROLL, self.OnScroll, id=5)
        self.slider6.Bind(wx.EVT_SCROLL, self.OnScroll, id=6)

        arvo=self.slider.GetValue()
        #print arvo

        pnl.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)
        button.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)
        text.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)
        combo.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)
        self.slider.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)
        self.slider2.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)

	button.Bind(wx.EVT_BUTTON,self.drawFigure)

        self.sb = self.CreateStatusBar()

        self.SetSize((750, 530))
        self.SetTitle('wx.Statusbar')
        self.Centre()
        self.Show(True)     

    def drawFigure(self,*args):

        self.computations()
	self.figure = matplotlib.figure.Figure((5,4),dpi=100)
	self.canvas = FigureCanvas(self.pnl2,-1,self.figure)
	self.axes = self.figure.add_subplot(111)
	#self.y_max = 5
	self.axes.plot(self.inrunsx,self.inrunsy)
	self.axes.plot(self.lentosx,self.lentosy)

    def OnWidgetEnter(self, e):
        
        name = e.GetEventObject().GetClassName()
        self.sb.SetStatusText(name + ' widget')
        e.Skip()               
        
    def OnScroll(self,e):
        #print "Succesfull call of OnScroll"
        luku=e.GetEventObject().GetValue()
	sliderid=e.GetId()
	if sliderid==1:
		#radius
		self.radius=luku
		self.ylengthstr=self.slider6.GetValue()-(self.radius-cos(self.runangle)*self.radius)
	elif sliderid==2:
		#runangle
		self.runangle=luku*2.*pi/360.
		self.ylengthstr=self.slider6.GetValue()-(self.radius-cos(self.runangle)*self.radius)
	elif sliderid==3:
		#flat
		self.flat=luku
	elif sliderid==4:
		#takeAngle
		self.takeoffAngle=luku*2.*pi/360.
	elif sliderid==5:
		#takeHeight
		self.takeoffHeight=luku
	elif sliderid==6:
		#ylengthstr
		self.ylengthstr=luku-(self.radius-cos(self.runangle)*self.radius)
        #print luku

    def computations(self):
	##rest after
	[t,sx,sy,vx,vy,ax,ay]=inrun(self.runangle,0,0,0,self.ylengthstr,self.runangle,self.radius,self.flat,self.takeoffAngle,self.takeoffHeight)
	[kode,sxloppu,syloppu,vxloppu,vyloppu]=takeoff2(self.ylengthstr,self.runangle,self.radius,self.flat,self.takeoffAngle,self.takeoffHeight)
	self.inrunsx=sx[:kode]
	self.inrunsy=sy[:kode]
	#print (ylengthstr/tan(runangle)+radius*sin(runangle))+flat
	#print [vxloppu,vyloppu]
	#print sqrt(vxloppu**2+vyloppu**2)
	#pylab.plot(sxloppu,syloppu,'o')
	#pylab.plot([sxloppu,sxloppu+19,sxloppu+19+tan(35.*2.*pi/360.)*16.],[syloppu-4,syloppu-4,syloppu-4-16])
	[t1,sx1,sy1,vx1,vy1,ax1,ay1]=lento(sxloppu,syloppu,vxloppu,vyloppu)
	self.lentosx=sx1
	self.lentosy=sy1
##	pylab.savefig('Lahti_real.png')
	#pylab.show()
##	#print ax
##	#for i in range(len(t)-1):
##	#	print rinnekulma(sx[i,0])
#		#print arctan2(vy[i,0],vx[i,0])*360./2./pi

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()   

