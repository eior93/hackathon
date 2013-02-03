import wx

def TupleToColor(myTuple):
    return wx.Colour(myTuple[0], myTuple[1], myTuple[2])

colorArr = [(32.0, 30.0, 35.0), (77.0, 41.0, 41.0), (110.0, 22.0, 39.0), (98.0, 38.0, 26.0), (118.0, 97.0, 30.0), (18.0, 35.0, 30.0), (8.0, 37.0, 89.0), (60.5, 41.0, 76.0), (80.0, 88.0, 104.0), (131.0, 129.0, 131.0)]



class Band(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(30, 50))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.myColor = wx.Color(0,0,0)

    def SetColor(self, aColor):
        self.myColor = aColor

    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetBrush(wx.Brush(self.myColor, wx.SOLID))
        dc.SetPen(wx.Pen(self.myColor, 4, wx.SOLID))
        dc.DrawRectangle(0, 0, 500, 500) 



class MainWindow(wx.Frame):    

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title, size=(500,500))

        self.numBands = 3
        

        #  style=wx.SIMPLE_BORDER

        self.imgPanel = wx.Panel(self)
        self.bandPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        self.infoPanel = wx.Panel(self)

        # sizer to arrange panels
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.imgPanel, 2, wx.EXPAND)
        self.sizer.Add(self.bandPanel, 1, wx.EXPAND)
        self.sizer.Add(self.infoPanel, 1, wx.EXPAND)


        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        # self.sizer.Fit(self)


        bandArr = []

        self.bandPanel.sizer = wx.BoxSizer(wx.HORIZONTAL)


        for count in range(0,self.numBands):
            bandArr.append(Band(self.bandPanel))

            bandArr[count].SetColor(TupleToColor(colorArr[count*2]))       
            self.bandPanel.sizer.AddStretchSpacer(1)
            self.bandPanel.sizer.Add(bandArr[count], 1, wx.EXPAND)

        self.bandPanel.sizer.AddStretchSpacer(1)

        self.bandPanel.SetSizer(self.bandPanel.sizer)
        self.bandPanel.SetAutoLayout(True)
        

        clickButton = wx.Button(self.infoPanel, "CLICK ME")
        self.Bind(wx.EVT_BUTTON, self.OnClick, clickButton)

        # panel2 = wx.Panel(self)

        # self.img = wx.StaticText(panel1, label="Image here: ")
        # self.quote = wx.StaticText(panel2, label="Your quote: ", pos=(100, 100))

        # Setting up the menu.
        filemenu= wx.Menu()
        menuItem = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuItem)
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.Show(True)



    def OnAbout(self, event):
    	# A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "FIGHT THE RESISTANCE", "About us", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished. 



app = wx.App(False)
frame = MainWindow(None, "Resistor Identifier")
app.MainLoop()







