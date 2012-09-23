#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx

class Example(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw) 
        
        self.InitUI()
                
    def InitUI(self):

        pnl = wx.Panel(self)
        grid = wx.GridSizer(3, 2)

        grid.AddMany([(wx.Button(pnl, wx.ID_CANCEL), 0, wx.TOP | wx.LEFT, 9),
            (wx.Button(pnl, wx.ID_DELETE), 0, wx.TOP, 9),
            (wx.Button(pnl, wx.ID_SAVE), 0, wx.LEFT, 9),
            (wx.Button(pnl, wx.ID_EXIT)),
            (wx.Button(pnl, wx.ID_STOP), 0, wx.LEFT, 9),
            (wx.Button(pnl, wx.ID_NEW))])

        self.Bind(wx.EVT_BUTTON, self.OnQuitApp, id=wx.ID_EXIT)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
	pnl.SetSizer(grid)

        self.SetSize((220, 180))
        self.SetTitle("Standard ids")
        self.Centre()
        self.Show(True)

    def OnQuitApp(self, event):

	self.Close()

    def OnCloseWindow(self,e):

        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            
        ret = dial.ShowModal()
        
        if ret == wx.ID_YES:
            self.Destroy()
        else:
            e.Veto()
        

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()  
