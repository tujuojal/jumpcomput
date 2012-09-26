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
        
	#x and y values for plotting
	self.t=[2,4,6]
	self.s=[1,5,3]

        #constants, aka variables that will be binded to sliders
	self.radius=20.	#this is global constant, radius of the transitions
	self.runangle=31.*2.*pi/360.		#angle of the inrun, straight section
	self.flat=10.		#length of flat section before takeof
	self.takeoffAngle=31.*2.*pi/360.	#angle of takeoff
	self.takeoffHeight=3.5 -(self.radius-cos(self.takeoffAngle)*self.radius) 		#height of takeoff
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
        text = wx.CheckBox(pnl, label='CheckBox', pos=(20, 90))
        combo = wx.ComboBox(pnl, pos=(120, 22), choices=['Python', 'Ruby'])
        slider = wx.Slider(pnl, 5, 20, 1, 20, (120, 90), (110, -1))        
        slider2 = wx.Slider(pnl, 6, 0, 1, 20, (120, 120), (110, -1))        

        slider.Bind(wx.EVT_SCROLL, self.OnScroll, id=5)
        slider2.Bind(wx.EVT_SCROLL, self.OnScroll, id=6)

        arvo=slider.GetValue()
        #print arvo

        pnl.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)
        button.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)
        text.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)
        combo.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)
        slider.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)
        slider2.Bind(wx.EVT_ENTER_WINDOW, self.OnWidgetEnter)

	button.Bind(wx.EVT_BUTTON,self.drawFigure)

        self.sb = self.CreateStatusBar()

        self.SetSize((550, 530))
        self.SetTitle('wx.Statusbar')
        self.Centre()
        self.Show(True)     

    def drawFigure(self,*args):

	self.figure = matplotlib.figure.Figure((5,4),dpi=100)
	self.canvas = FigureCanvas(self.pnl2,-1,self.figure)
	self.axes = self.figure.add_subplot(111)
	#self.y_max = 5
	self.axes.plot(self.t,self.s)
	self.axes.plot([1,2,3],[3,3,3])

    def OnWidgetEnter(self, e):
        
        name = e.GetEventObject().GetClassName()
        self.sb.SetStatusText(name + ' widget')
        e.Skip()               
        
    def OnScroll(self,e):
        #print "Succesfull call of OnScroll"
        luku=e.GetEventObject().GetValue()
	self.s=[1,luku,2]
        #print luku

    def computations(self,e):
	##rest after
	[t,sx,sy,vx,vy,ax,ay]=inrun(self.runangle,0,0,0,self.ylengthstr,self.runangle,self.radius,self.flat,self.takeoffAngle,self.takeoffHeight)
	[kode,sxloppu,syloppu,vxloppu,vyloppu]=takeoff2(self.ylengthstr,self.runangle,self.radius,self.flat,self.takeoffAngle,self.takeoffHeight)
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

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()   

