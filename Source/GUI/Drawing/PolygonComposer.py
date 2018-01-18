from tkinter import *

from GUI.Drawing.drawing_state import DrawingState
from Core.Geometry.Intersections import IntersectSegments

class PolygonComposer:
    
    def __init__( self, canvas ):
        self.canvas = canvas
        self.state = DrawingState.FIRST
        self.vertices = []
        self.lineIds = []
        self.activeSegment = None

    def Cleanup(self):
        self.canvas.delete( *self.lineIds )
        self.canvas.delete( self.activeSegment )
        self.vertices = []
        self.lineIds = []
        self.activeSegment = None

    def OnClick( self, x, y ):
        if len(self.vertices) == 0:
            self.BeginPolygon( x, y )
        elif self.ValidateSegment( [ *self.vertices[-1], x, y ] ):
            self.AddSegment( x, y )

    def OnMove( self, x, y ):
        if self.activeSegment:
            segmentVertices = [ *self.vertices[-1], x, y ]
            self.canvas.coords( self.activeSegment, *segmentVertices )
            self.SetLineColor( self.activeSegment, self.ValidateSegment( segmentVertices ) )

    def FinalizePolygon( self ):
        if self.activeSegment and len(self.vertices) > 2:
            lastSegment = [ *self.vertices[-1], *self.vertices[0] ]
            if self.ValidateSegment( lastSegment, True ):
                vertices = self.vertices
                
                self.Cleanup()
                self.state += 1 #redo...
                
                return vertices
            
        return None


    def BeginPolygon( self, x, y ):
        self.vertices.append( (x, y) )
        self.activeSegment = self.CreateLine( (x,y), (x,y) )
        self.canvas.itemconfig( self.activeSegment, dash = (7,3) )

    def AddSegment( self, x, y ):
        self.vertices.append( (x, y) )
        self.lineIds.append( self.CreateLine( self.vertices[-2], self.vertices[-1] ) )

    def CreateLine( self, startPos, endPos ):
        return self.canvas.create_line( startPos, endPos, fill='black' )

    def ValidateSegment( self, segmentCoords, skipFirst = False ):
        startVert = 1 + ( 1 if skipFirst else 0 )
        for i in range( startVert, len(self.vertices) - 1 ):
            testSegment = [ *self.vertices[i-1], *self.vertices[i] ]
            if IntersectSegments( segmentCoords, testSegment ):
                return False
                    
        return True

    def SetLineColor( self, gfxId, validLine ):
        if validLine:
            self.canvas.itemconfig( gfxId, fill='black' )
        else:
            self.canvas.itemconfig( gfxId, fill='red' )

    def GetState( self ):
        return self.state

        
        
    
