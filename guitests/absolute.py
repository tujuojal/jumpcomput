
#!/usr/bin/python
# -*- coding: utf-8 -*-

# absolute.py

import wx

class Example(wx.Frame):
  
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, 
            size=(260, 180))
            
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):
    
        panel = wx.Panel(self, -1)

        menubar = wx.MenuBar()
        filem = wx.Menu()
        editm = wx.Menu()
        helpm = wx.Menu()
        
	fitem = filem.Append(wx.ID_EXIT, 'Quit', 'Quit application')
	editem = editm.Append(wx.ID_EDIT, 'Nothing', 'No function')
        
	menubar.Append(filem, '&File')
        menubar.Append(editm, '&Edit')
        menubar.Append(helpm, '&Help')
        self.SetMenuBar(menubar)
       
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        
	self.SetTitle('Tekstia ja muuta')
        
	wx.TextCtrl(panel, pos=(3, 30), size=(250, 150))


    def OnQuit(self, e):
        self.Close()


if __name__ == '__main__':
  
    app = wx.App()
    Example(None, title='')
    app.MainLoop()

