#!/usr/bin/python
# -*- coding: utf-8 -*-
#this is with python3 not backwards compatible!!

import wx
import numpy
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas, \
		NavigationToolbar2WxAgg as NavigationToolbar
from lento import lento
from inrun2 import inrun
from inrun2 import takeoff2
from scipy import *
import os

class Example(wx.Frame):
    """ Just first tests...."""
    title = 'EasyJumpComputatio'

    def __init__(self):
        wx.Frame.__init__(self,None,-1,self.title) 
        

        #constants, aka variables that will be binded to sliders
	self.radius=20.	#this is global constant, radius of the transitions
	self.runangle=31.*2.*pi/360.		#angle of the inrun, straight section
	self.flat=10.		#length of flat section before takeof
	self.takeoffAngle=25.*2.*pi/360.	#angle of takeoff
	self.takeoffHeight=3.  		#height of takeoff
	self.ylengthstr=25.-(self.radius-cos(self.runangle)*self.radius)	#-yheight when transition starts, 0 is strarting level, 20 radius

        self.InitUI()
        self.drawFigure()
	self.create_menu()
	self.create_status_bar()
        
    def create_menu(self):
        self.menubar = wx.MenuBar()
        
        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        
        menu_help = wx.Menu()
        m_about = menu_help.Append(-1, "&About\tF1", "About the computation")
        self.Bind(wx.EVT_MENU, self.on_about, m_about)
        
        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menu_help, "&Help")
        self.SetMenuBar(self.menubar)
    def InitUI(self):   

        self.sp = wx.SplitterWindow(self)
        pnl = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)

        # in panel2 we have the figure
        self.pnl2 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)

        self.sp.SplitVertically(pnl,self.pnl2,300)

        button = wx.Button(pnl, label='Redraw', pos=(20, 20))
        text = wx.CheckBox(pnl, label='CheckBox', pos=(120, 50))
        combo = wx.ComboBox(pnl, pos=(120, 22), choices=['Python', 'Ruby'])
        
	self.slider = wx.Slider(pnl, 1, 200, 100, 300, (120, 100), (110, -1),style=wx.SL_AUTOTICKS)	#radius       
	self.textRadius = wx.TextCtrl(pnl, -1, str(self.slider.GetValue()/10.),pos=(230, 100), size=(50,20))
	textInfoRadius = wx.StaticText(pnl, -1, "Radius", wx.Point(20,100))
	
	self.slider2 = wx.Slider(pnl, 2, 300, 100, 400, (120, 150), (110, -1),style=wx.SL_AUTOTICKS) 	#runangle
	self.textRunAngle = wx.TextCtrl(pnl, -1, str(self.slider2.GetValue()/10.),pos=(230, 150), size=(50,20))
	textInfoRunAngle = wx.StaticText(pnl, -1, "Inrun Angle", wx.Point(20,150))
        
	self.slider3 = wx.Slider(pnl, 3, 100, 10, 200, (120, 200), (110, -1),style=wx.SL_AUTOTICKS) 	#flat
	self.textFlat = wx.TextCtrl(pnl, -1, str(self.slider3.GetValue()/10.),pos=(230, 200), size=(50,20))
	textInfoFlat = wx.StaticText(pnl, -1, "Flat", wx.Point(20,200))
        
	self.slider4 = wx.Slider(pnl, 4, 250, 100, 400, (120, 250), (110, -1),style=wx.SL_AUTOTICKS) 	#takeoffAngle
	self.textTakeoffAngle = wx.TextCtrl(pnl, -1, str(self.slider4.GetValue()/10.),pos=(230, 250), size=(50,20))
	textInfoTakeoffAngle = wx.StaticText(pnl, -1, "Takeoff Angle", wx.Point(20,250))
        
	self.slider5 = wx.Slider(pnl, 5, 30, 10, 40, (120, 300), (110, -1),style=wx.SL_AUTOTICKS) 	#takeoffHeight
	self.textTakeoffHeight = wx.TextCtrl(pnl, -1, str(self.slider5.GetValue()/10.),pos=(230, 300), size=(50,20))
	textInfoTakeoffHeight = wx.StaticText(pnl, -1, "Takeoff Height", wx.Point(20,300))

        self.slider6 = wx.Slider(pnl, 6, 250, 100, 400, (120, 350), (110, -1),style=wx.SL_AUTOTICKS) 	#ylengthstr
	self.textYlengthstr = wx.TextCtrl(pnl, -1, str(self.slider6.GetValue()/10.),pos=(230, 350), size=(50,20))
	textInfoYlengthstr = wx.StaticText(pnl, -1, "Inrun Height", wx.Point(20,350))

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


        self.SetSize((750, 530))
        self.Centre()
        self.Show(True)     

    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()

    def drawFigure(self,*args):
        self.dpi = 100
        self.computations()
	self.figure = matplotlib.figure.Figure((5,4),dpi=self.dpi)
	self.canvas = FigureCanvas(self.pnl2,-1,self.figure)
	self.axes = self.figure.add_subplot(111)
	#self.y_max = 5
	self.axes.plot(self.inrunsx,self.inrunsy)
	self.axes.plot(self.lentosx,self.lentosy)
	self.toolbar = NavigationToolbar(self.canvas)

    def OnWidgetEnter(self, e):
        
        name = e.GetEventObject().GetClassName()
        self.statusbar.SetStatusText(name + ' widget')
        e.Skip()               
        
    def OnScroll(self,e):
        #print "Succesfull call of OnScroll"
        luku=e.GetEventObject().GetValue()
	sliderid=e.GetId()
	if sliderid==1:
		#radius
		self.radius=luku/10.
		self.ylengthstr=self.slider6.GetValue()/10.-(self.radius-cos(self.runangle)*self.radius)
		self.textRadius.SetValue(str(self.radius))
	elif sliderid==2:
		#runangle
		self.runangle=luku/10.*2.*pi/360.
		self.ylengthstr=self.slider6.GetValue()/10.-(self.radius-cos(self.runangle)*self.radius)
		self.textRunAngle.SetValue(str(luku/10.))
	elif sliderid==3:
		#flat
		self.flat=luku/10.
		self.textFlat.SetValue(str(self.flat))
	elif sliderid==4:
		#takeAngle
		self.takeoffAngle=luku/10.*2.*pi/360.
		self.textTakeoffAngle.SetValue(str(luku/10.))
	elif sliderid==5:
		#takeHeight
		self.takeoffHeight=luku/10.
		self.textTakeoffHeight.SetValue(str(self.takeoffHeight))
	elif sliderid==6:
		#ylengthstr
		self.ylengthstr=luku/10.-(self.radius-cos(self.runangle)*self.radius)
		self.textYlengthstr.SetValue(str(self.ylengthstr))
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
    
    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)
        else:
		self.flash_status_message("Not saved!! ERROR ERROR")
           
    def on_about(self, event):
        msg = """ A computation with airdrag and friction:
        
         * Constants of computation from ??
         * Forward stepping scheme, no idea about numerical error
         * Inrun is drawn according to path computed from forces
         * Forces are computed according to geometry determined by parameters
         * Lots of bugs, even in numerics probably
         * 
	 * Version 0.001
        """
        dlg = wx.MessageDialog(self, msg, "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy() 

    def flash_status_message(self, msg, flash_len_ms=1500):
        self.statusbar.SetStatusText(msg)
        self.timeroff = wx.Timer(self)
        self.Bind(
            wx.EVT_TIMER, 
            self.on_flash_status_off, 
            self.timeroff)
        self.timeroff.Start(flash_len_ms, oneShot=True)
    
    def on_flash_status_off(self, event):
        self.statusbar.SetStatusText('')

    def on_exit(self, event):
        self.Destroy()


def main():
    
    ex = wx.App()
    Example()
    ex.MainLoop()    

if __name__ == '__main__':
    main()   

