#!/usr/bin/python
# -*- coding: utf-8 -*-
#this is with python3 not backwards compatible!!

import wx
import numpy
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class Example(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw) 
        
        self.InitUI()
        
    def InitUI(self):   

        self.sp = wx.SplitterWindow(self)
        pnl = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)

        # in panel2 we have the figure
        pnl2 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)
	self.figure = matplotlib.figure.Figure((5,4),dpi=100)
	self.canvas = FigureCanvas(pnl2,-1,self.figure)
	self.axes = self.figure.add_subplot(111)
	t=[1,2,3,4,5]
	s=[1,1-1,1-1]
	#self.y_max = 5
	self.axes.plot(t,s)

        self.sp.SplitVertically(pnl,pnl2,300)

        button = wx.Button(pnl, label='Button', pos=(20, 20))
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

        self.sb = self.CreateStatusBar()

        self.SetSize((550, 530))
        self.SetTitle('wx.Statusbar')
        self.Centre()
        self.Show(True)     

    def OnWidgetEnter(self, e):
        
        name = e.GetEventObject().GetClassName()
        self.sb.SetStatusText(name + ' widget')
        e.Skip()               
        
    def OnScroll(self,e):
        #print "Succesfull call of OnScroll"
        luku=e.GetEventObject().GetValue()
        #print luku


def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()   

