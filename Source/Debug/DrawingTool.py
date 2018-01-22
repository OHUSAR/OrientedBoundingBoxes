from tkinter import *

from GUI.Canvas.FancyPolygon import FancyPolygon
from GUI.StaticData.Colors import Colors

class DrawingTool:
    def __init__( self, canvasW = 300, canvasH = 300 ):
        self.width = canvasW
        self.height = canvasH

        self.currentWidnow = None
        self.currentCanvas = None

        self._DEBUG = False

    def NewWindow( self, title = None ):
        if self._DEBUG:
            self.currentWindow = Tk()
            if title:
                self.currentWindow.title( title )

    def NewCanvas( self, side ):
        if self._DEBUG:            
            self.currentCanvas = Canvas( master = self.currentWindow, width = self.width, height = self.height )
            self.currentCanvas.pack( side = side )
            return self.currentCanvas

    def DrawPoly( self, vertices, newCanvas = False, side = LEFT ):
        if self._DEBUG:
            if newCanvas or self.currentCanvas is None:
                self.NewCanvas( side )
            
            vertices = [ tuple( v ) for v in vertices ]
            print( vertices )
            FancyPolygon( self.currentCanvas ).Invalidate( vertices )

    def DrawLinePoly( self, vertices, newCanvas = False, side = LEFT ):
        if self._DEBUG:
            if newCanvas or self.currentCanvas is None:
                self.NewCanvas( side )
    
            vertices = [ tuple( v ) for v in vertices ]
            print(vertices)
            if vertices[0] != vertices[-1]:
                vertices.append( vertices[0] )
            
            self.currentCanvas.create_line( vertices, fill = Colors.OOBB, width = 2 )       

    def setDebug( self, dbg ):
        self._DEBUG = dbg

DRAW_TOOL = DrawingTool()
        
