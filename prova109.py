import wx

# Set some constants

GaBEPMax = 5.00e-7
AlBEPMax = 2.50e-7
InBEPMax = 7.50e-7

class MyFrame(wx.Frame):
   def __init__(self, parent, title):
       wx.Frame.__init__(self, parent, -1, title, pos=(150, 150),
                         size=(550, 400))

       # Create a panel

       panel = wx.Panel(self)

       # Add a few button controls

       ExitBtn = wx.Button(panel, -1, "Exit")
       AlloyBtn = wx.Button(panel, -1, "Alloy")

       # Bind the button events to handlers

       self.Bind(wx.EVT_BUTTON, self.OnAlloy, AlloyBtn)
       self.Bind(wx.EVT_BUTTON, self.OnNowExit, ExitBtn)

       # Use a sizer to layout the controls, stacked vertically and with
       # a 10 pixel border around each
       sizer = wx.BoxSizer(wx.VERTICAL)

       sizer.Add(AlloyBtn, 0, wx.ALL, 10)
       sizer.Add(ExitBtn, 0, wx.ALL, 10)

       panel.SetSizer(sizer)
       panel.Layout()

       # need to define text....
       self.text = "This is some test text"

   def OnNowExit(self, evt):
       # Event handler for the Exit button click.
       print "Now Exiting..."
       self.Close()

   def OnAlloy(self, evt):
       # Event handler for the Alloy button click.
       # print "In Alloy..."
       dlg = AlloyBEPDialog(self, -1, "Quick Alloy Calculations", self.text)
       dlg.CenterOnScreen()
       dlg.ShowModal()
       dlg.Destroy()

class AlloyBEPDialog(wx.Dialog):
   def __init__(self, parent, ID, title, txt):
       wx.Dialog.__init__(self, parent, -1, title, (0,0), wx.Size(340,300))

       # Get the X value for the alloy
       # Start with the slider at 0
       AlloyQueryText = wx.StaticText(self, -1, "Ternary Alloy Mole Fraction (%): ", wx.Point(70,10))
       self.sliderX = wx.Slider(self, -1, 0, 0, 100, pos=(80,30),
                          size=(150,50),
                          style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS |wx.SL_LABELS )
       self.sliderX.SetTickFreq(5, 1)
       self.sliderX.Bind(wx.EVT_SLIDER, self.slideXValue)

       # Enlarge the default font to make this easier to read.  The last parameter is bold, etc.
       font1 = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)

       # Label the Columns for the In, Al and Ga BEP columns
       BEPText = wx.StaticText(self, -1, "BEP (Torr)", wx.Point(160, 85))
       BEPText.SetFont(font1)
       InColumnText = wx.StaticText(self, -1, "Indium", wx.Point(75, 100))
       InColumnText.SetFont(font1)
       AlColumnText = wx.StaticText(self, -1, "Aluminum", wx.Point(160, 100))
       AlColumnText.SetFont(font1)
       GaColumnText = wx.StaticText(self, -1, "Gallium",wx.Point(255, 100), style=wx.BOLD)
       GaColumnText.SetFont(font1)

       AlGaPText = wx.StaticText(self, -1, "AlGaP", wx.Point(5,120))
       AlGaPText.SetForegroundColour('blue')
       InGaPText = wx.StaticText(self, -1, "InGaP", wx.Point(5, 140))
       InGaPText.SetForegroundColour('red')
       InAlPText = wx.StaticText(self, -1, "InAlP", wx.Point(5, 160))
       InAlPText.SetForegroundColour('violet')

       wx.Button(self, wx.ID_OK, "Close", wx.Point(130,200))

       self.AlBEPText = wx.TextCtrl(self, -1, str("%.3e" % 0),pos=(150, 120), size=(80,20))  # for AlGaP
       self.AlBEPText2 = wx.TextCtrl(self, -1, str("%.3e" % 0),pos=(150, 160), size=(80,20)) # for InAlP
       self.GaBEPText = wx.TextCtrl(self, -1, str("%.3e" % 0),pos=(240, 120), size=(80,20))  # for AlGaP
       self.GaBEPText2 = wx.TextCtrl(self, -1, str("%.3e" % 0),pos=(240, 140), size=(80,20)) # for InGaP
       self.InBEPText = wx.TextCtrl(self, -1, str("%.3e" % 0),pos=(60, 140), size=(80,20))   # for InGaP
       self.InBEPText2 = wx.TextCtrl(self, -1, str("%.3e" % 0),pos=(60, 160), size=(80,20))  # for InAlP
       
       
   def slideXValue(self, evt):
       self.sliderX.XValue = self.sliderX.GetValue()
       # Need to have fixed format to avoid formatting errors on repainting
       AlBEP = self.sliderX.XValue * AlBEPMax * 0.01

       # Use TextControls to position the values.
       self.AlBEPText.SetValue("%.3e" % AlBEP)
       
       # For InAlP
       if self.sliderX.XValue > 0:
           AlBEP2 = (100.0 - self.sliderX.XValue) * AlBEPMax * 0.01
       else:
           AlBEP2 = AlBEPMax

       self.AlBEPText2.SetValue("%.3e" % AlBEP)

       # For AlGaP and InGaP
       if self.sliderX.XValue > 0:
           GaBEP = (100.0 - self.sliderX.XValue) * GaBEPMax * 0.01
       else:
           GaBEP = GaBEPMax
       self.GaBEPText.SetValue("%.3e" % GaBEP)
       self.GaBEPText2.SetValue("%.3e" % GaBEP)

       InBEP = self.sliderX.XValue * InBEPMax * 0.01
       self.InBEPText.SetValue("%.3e" % InBEP)
       self.InBEPText2.SetValue("%.3e" % InBEP)
       

class MyApp(wx.App):
   def OnInit(self):
       frame = MyFrame(None, "Quick Alloy Calculations - 21 January 2008")
       self.SetTopWindow(frame)

       frame.Show(True)
       return True

app = MyApp(redirect=True)
app.MainLoop()

