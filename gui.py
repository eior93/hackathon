import wx

def TupleToColor(myTuple):
    return wx.Colour(myTuple[0], myTuple[1], myTuple[2])

colorArr = [(32.0, 30.0, 35.0), (77.0, 41.0, 41.0), (110.0, 22.0, 39.0), (98.0, 38.0, 26.0), (118.0, 97.0, 30.0), (18.0, 35.0, 30.0), (8.0, 37.0, 89.0), (60.5, 41.0, 76.0), (80.0, 88.0, 104.0), (131.0, 129.0, 131.0)]

colorDict = {"black":(32.0, 30.0, 35.0), "brown":(77.0, 41.0, 41.0), "red":(110.0, 22.0, 39.0), "orange":(98.0, 38.0, 26.0), "yellow":(118.0, 97.0, 30.0), "green":(18.0, 35.0, 30.0), "blue":(8.0, 37.0, 89.0),"purple":(60.5, 41.0, 76.0), "grey":(80.0, 88.0, 104.0), "white":(131.0, 129.0, 131.0)}

colorNames = ["black", "brown", "red", "orange", "yellow", "green", "blue", "purple", "grey", "white"]

bandColors = [colorDict["black"], colorDict["black"], colorDict["black"]]

def SetBandColor(number, color):
    bandColors[number] = colorDict[color]
    frame.UpdateBandColor(number, color)


class Band(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(30, 50))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.myColor = wx.Color(0,0,0)

    def SetColor(self, aColor):
        self.myColor = aColor
        self.OnPaint()

    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetBrush(wx.Brush(self.myColor, wx.SOLID))
        dc.SetPen(wx.Pen(self.myColor, 4, wx.SOLID))
        dc.DrawRectangle(0, 0, 500, 500) 

class BandMod(wx.ComboBox):

    def __init__(self, parent, number):
        wx.ComboBox.__init__(self, parent, choices=colorNames)
        self.number = number
        self.Bind(wx.EVT_COMBOBOX, self.OnChoice)

    def OnChoice(self, event=None):
        SetBandColor(self.number, self.GetValue())



class MainWindow(wx.Frame):    

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title, size=(500,500))

        self.numBands = 3

        #  style=wx.SIMPLE_BORDER

        self.imgPanel = wx.Panel(self)
        self.bandPanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        self.modPanel = wx.Panel(self)
        self.infoPanel = wx.Panel(self)

        # sizer to arrange panels
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.imgPanel, 8, wx.EXPAND)
        self.sizer.Add(self.bandPanel, 4, wx.EXPAND)
        self.sizer.Add(self.modPanel, 1, wx.EXPAND)
        self.sizer.Add(self.infoPanel, 4, wx.EXPAND)


        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        # self.sizer.Fit(self)


        self.bandArr = []
        self.bandModArr = []

        self.bandPanel.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.modPanel.sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Configure Bands
        for count in range(0,self.numBands):
            self.bandArr.append(Band(self.bandPanel))
            self.bandModArr.append(BandMod(self.modPanel, count))

            self.bandArr[count].SetColor(TupleToColor(colorArr[count*2]))       
            self.bandPanel.sizer.AddStretchSpacer(1)
            self.bandPanel.sizer.Add(self.bandArr[count], 1, wx.EXPAND)

            self.modPanel.sizer.AddStretchSpacer(1)
            self.modPanel.sizer.Add(self.bandModArr[count], 1, wx.EXPAND)

        self.bandPanel.sizer.AddStretchSpacer(1)
        self.modPanel.sizer.AddStretchSpacer(1)

        self.bandPanel.SetSizer(self.bandPanel.sizer)
        self.bandPanel.SetAutoLayout(True)

        self.modPanel.SetSizer(self.modPanel.sizer)
        self.modPanel.SetAutoLayout(True)
        

        self.clickButton = wx.Button(self.infoPanel, label="CLICK ME")
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.clickButton)

        self.resistance = wx.StaticText(self.infoPanel, label="Resistance: ")

        self.infoPanel.sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.infoPanel.sizer.AddStretchSpacer(1)
        self.infoPanel.sizer.Add(self.resistance, 1, wx.ALIGN_CENTER)
        self.infoPanel.sizer.AddStretchSpacer(2)
        self.infoPanel.sizer.Add(self.clickButton, 1, wx.ALIGN_CENTER)
        self.infoPanel.sizer.AddStretchSpacer(1)


        self.infoPanel.SetSizer(self.infoPanel.sizer)
        self.infoPanel.SetAutoLayout(True)


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

    def UpdateBandColor(self, number, color):
        self.bandArr[number].SetColor(colorDict[color])

    def OnAbout(self, event):
    	# A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "FIGHT THE RESISTANCE", "About us", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished. 

    def OnClick(self, event):
        print "AAA\n"


app = wx.App(False)
frame = MainWindow(None, "Resistor Identifier")
app.MainLoop()







