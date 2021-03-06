import wx
import cStringIO
from image_to_color_bands import image_to_color_bands

def TupleToColor(myTuple):
    return wx.Colour(myTuple[2], myTuple[1], myTuple[1])

# colorArr = [(32.0, 30.0, 35.0), (77.0, 41.0, 41.0), (110.0, 22.0, 39.0), (98.0, 38.0, 26.0), (118.0, 97.0, 30.0), (18.0, 35.0, 30.0), (8.0, 37.0, 89.0), (60.5, 41.0, 76.0), (80.0, 88.0, 104.0), (131.0, 129.0, 131.0)]

colorDict = {"black":(10, 10, 10), "brown":(88, 60, 50), "red":(231, 47, 39), "orange":(238, 113, 25), "yellow":(255, 228, 15 ),
"green":(43, 106, 23), "blue":(46, 20, 141), "purple":(79, 71, 115), "grey":(213, 210, 213), "white":(244, 244, 244)}

colorNames = ["black", "brown", "red", "orange", "yellow", "green", "blue", "purple", "grey", "white"]

bandColors = ["black", "black", "black"]

def SetBandColor(number, color):
    bandColors[number] = color
    frame.UpdateBandColor(number, color)


def ScaleBitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result


class MyImgPanel(wx.Panel):
    def __init__(self, parent):
        # create the panel
        wx.Panel.__init__(self, parent)


    def SetImage(self, image):
        try:
            # pick a .jpg file you have in the working folder
            imageFile = image
            data = open(imageFile, "rb").read()
            # convert to a data stream
            stream = cStringIO.StringIO(data)
            # convert to a bitmap
            bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))

            print self.GetSize()

            width = self.GetSize()[0]
            height = self.GetSize()[1]

            bmp2 = ScaleBitmap(bmp, width, height)

            print bmp2.GetSize()

            # show the bitmap, (5, 5) are upper left corner coordinates
            wx.StaticBitmap(self, -1, bmp2, (0, 0))
            # alternate (simpler) way to load and display a jpg image from a file
            # actually you can load .jpg .png .bmp or .gif files
            # bitmap upper left corner is in the position tuple (x, y) = (5, 5)
        except IOError:
            print "Image file %s not found" % imageFile
            raise SystemExit



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

        self.imgPanel = MyImgPanel(self)
        


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

        self.Show(True)
        self.imgPanel.SetImage('inImage.jpg')

        self.bandArr = []
        self.bandModArr = []

        self.bandPanel.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.modPanel.sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Configure Bands
        for count in range(0,self.numBands):
            self.bandArr.append(Band(self.bandPanel))
            self.bandModArr.append(BandMod(self.modPanel, count))

            # self.bandArr[count].SetColor(TupleToColor(colorArr[count*2]))       
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

        # Setting up the menu.
        filemenu= wx.Menu()
        menuItem = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuItem)

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.Show(True)

    def UpdateBandColor(self, number, color):
        print 'number', number
        print 'color', color
        self.bandArr[number].SetColor(colorDict[color])

    def OnAbout(self, event):
    	# A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "FIGHT THE RESISTANCE", "About us", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished. 

    def OnClick(self, event):
        color_ids = image_to_color_bands('inImage');
        self.imgPanel.SetImage('inImage_cropped.jpg')

        SetBandColor(0, colorNames[color_ids[0]])
        SetBandColor(1, colorNames[color_ids[1]])
        SetBandColor(2, colorNames[color_ids[2]])

        answer = (colorNames.index(bandColors[0])*10 + colorNames.index(bandColors[1])) * pow(10,colorNames.index(bandColors[2]))
        self.resistance.SetLabel("Resistance: " + str(answer))


app = wx.App(False)
frame = MainWindow(None, "FIGHT THE RESISTANCE")
app.MainLoop()







