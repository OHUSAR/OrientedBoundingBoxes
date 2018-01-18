from tkinter import *
from tkinter.ttk import *
from tkinter import Canvas as TkCanvas
from tkinter import Scale as TkScale

from Core.BasicDefs import vector
from Core.SimulationObjects import SimulationPolygon

from GUI.StaticData.Strings import Strings
from GUI.Drawing.drawing_state import DrawingState
from GUI.Drawing.PolygonComposer import PolygonComposer
from GUI.PolygonGfx import PolygonGfx
from GUI.polygon_storage import PolygonStorage
from GUI.Interaction.PolygonManipulator import PolygonManipulator


class Canvas(TkCanvas):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw, width=1200, height=800, bg='white')
        self.pack(fill='both', expand=True, side='left')


class Application(Frame):

    def __init__(self, master=None, DEBUG = False, **kwargs):
        super().__init__(master, **kwargs)

        self._DEBUG = DEBUG

        self.MIN_BVH_DEPTH = 0
        self.MAX_BVH_DEPTH = 2
        self.BVH_DEPTH_DEFAULT = 1

        self.initializeGui()
        self.initialize()

        self.BindDrawEvents()
        self.pack()

    def initializeGui(self):
        self.canvas = Canvas(master=self)

        # Toolbar
        self.frame = Frame(master=self, height=800, width=20)
        self.frame.pack(side='right')

        # Toolbar controls
        self.clear = Button(master=self.frame, text=Strings.BTN_CLEAR, command=self.clear, width=20)
        self.oobbStateButton = Button(master=self.frame, text=Strings.BTN_OOBB_HIDE, command=self.swapOobbState, width=20)
        self.clear.pack(side='top')
        self.oobbStateButton.pack(side='top')

        # BVolume Settings
        self.boundVolumeTypes = { "Oriented Bounding Box": "oobb",
                                  "Convex Hull" : "convHull" }
        self.boundVolumeChoice = StringVar()
        self.boundVolumeChoice.set( "Oriented Bounding Box" )

        
        self.settingsFrame = LabelFrame( master = self.frame, height = 200, width = 20,
                                         padding = 10,
                                         text = "BVH Settings", labelanchor="nw",
                                         )
        
        self.bvTypeMenu = OptionMenu( self.settingsFrame, self.boundVolumeChoice,
                                      self.boundVolumeChoice.get(),
                                      *list( self.boundVolumeTypes.keys() ),
                                      command = self.ChangeBvType )

        self.bvhDepthLabel = Label( self.settingsFrame, text = 'BVH Depth' )
        self.bvhDepthSlider = TkScale(   self.settingsFrame,
                                         from_ = self.MIN_BVH_DEPTH,
                                         to = self.MAX_BVH_DEPTH,
                                         resolution = 1, orient = HORIZONTAL,
                                         command = self.ChangeBvType )
        self.bvhDepthSlider.set( self.BVH_DEPTH_DEFAULT )

        self.settingsFrame.pack( side = 'top' )
        self.bvTypeMenu.pack( side = 'top' )
        self.bvhDepthLabel.pack( side = 'top' )
        self.bvhDepthSlider.pack( side = 'top' )
 
        # DEBUG
        if self._DEBUG:
            self.debugFrame = LabelFrame( master = self.frame, height = 200, width = 20,
                                          padding = 10,
                                          text = "Dangerous Stuff!", labelanchor = "nw" )                           
            self.printBtn = Button( master=
                                    self.debugFrame, text="Print Objects", command = self.DEBUG_PRINT )

            self.debugFrame.pack( side = 'bottom' )
            self.printBtn.pack( side = 'top' )

    def initialize(self):
        self.polygons = PolygonStorage()
        self.composer = PolygonComposer( self.canvas )
        self.manipulator = PolygonManipulator( self.polygons, self.canvas )
        self.hideState = False
        
        self.convexHullHidden = False # TODO (mainly debug purposes)

    def BindDrawEvents(self):
        self.canvas.bind("<ButtonPress-1>", self.onDrawClick)
        self.canvas.bind("<ButtonPress-3>", self.onDrawEnd)
        self.canvas.bind("<Double-Button-1>", self.onDrawEnd)
        self.canvas.bind("<Motion>", self.onDrawMove)

    def UnbindDrawEvents(self):
        self.canvas.unbind("<ButtonPress-1>" )
        self.canvas.unbind("<ButtonPress-3>" )
        self.canvas.unbind("<Double-Button-1>")
        self.canvas.unbind("<Motion>")

    def BindMoveEvents(self):
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.on_token_press)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind("token", "<B1-Motion>", self.on_token_motion)

    def UnbindMoveEvents(self):
        self.canvas.tag_unbind("token", "<ButtonPress-1>")
        self.canvas.tag_unbind("token", "<ButtonRelease-1>")
        self.canvas.tag_unbind("token", "<B1-Motion>")

    def clear(self):
        self.canvas.delete("all")

        hide = self.hideState
        self.initialize()
        self.hideState = hide
        

        self.UnbindMoveEvents()
        self.BindDrawEvents()

    def swapOobbState(self):
        self.hideState = not self.hideState
        if self.hideState:
            self.oobbStateButton["text"] = Strings.BTN_OOBB_SHOW
        else:
            self.oobbStateButton["text"] = Strings.BTN_OOBB_HIDE
        self.manipulator.CheckCollisions( self.hideState )


    def onDrawClick( self, event ):
        self.composer.OnClick( event.x, event.y )

    def onDrawMove( self, event ):
        self.composer.OnMove( event.x, event.y )

    def onDrawEnd( self, event ):
        vertices = self.composer.FinalizePolygon()
        if vertices is not None:
            self.add_polygon( vertices )

            if self.composer.GetState() == DrawingState.DONE:
                self.UnbindDrawEvents()
                self.BindMoveEvents()

    def add_polygon(self, vertices):
        bvType = self.boundVolumeTypes[ self.boundVolumeChoice.get() ]
        bvhDepth = self.bvhDepthSlider.get()
        
        polygon = SimulationPolygon( [vector(v) for v in vertices], bvhDepth, bvType )
        polygonGfx = PolygonGfx( polygon, self.canvas )
        self.polygons.add( polygon, polygonGfx, polygonGfx.polygonId )
        self.manipulator.CheckCollisions( self.hideState )

    def on_token_press(self, event):
        self.manipulator.OnDragStart( event.x, event.y )

    def on_token_release(self, event):
        self.manipulator.OnDragEnd()

    def on_token_motion(self, event):
        self.manipulator.OnDrag( event.x, event.y, self.hideState )

    def ChangeBvType( self, dummyArg ):
        bvhDepth = self.bvhDepthSlider.get()
        bvType = self.boundVolumeTypes[ self.boundVolumeChoice.get() ]

        newCache = dict()
        
        for polyI in range( len( self.polygons ) ):
            poly = self.polygons.get(polyI, True)
            poly.polygon.InvalidateBVH( bvhDepth, bvType )
            poly.polygonGfx.Invalidate( poly.polygon, self.canvas, True )
            newCache[poly.polygonGfx.polygonId] = poly
            
        self.polygons.ReplaceBy( newCache )
        self.manipulator.CheckCollisions( self.hideState )

    ## DEBUG STUFF
    def DEBUG_PRINT( self ):
        for objI in range( len(self.polygons) ):
            print( "Object{}".format( objI ) )
            for v in self.polygons.get( objI, True ).polygon.originalPolygon.GetVertices():
                print( "{}, {}".format( v[0], v[1] ) )

if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.mainloop()
