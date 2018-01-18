from tkinter import *
from tkinter.ttk import *
from tkinter import Canvas as TkCanvas

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

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

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

    def initialize(self):
        self.polygons = PolygonStorage()
        self.composer = PolygonComposer( self.canvas )
        self.manipulator = PolygonManipulator( self.polygons, self.canvas )
        self.hideState = False
        
        self.convexHullHidden = False # TODO (mainly debug purposes)

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
        print( 'vertex count: {}'.format( len(vertices ) ) )
        polygon = SimulationPolygon( [vector(v) for v in vertices] )
        polygonGfx = PolygonGfx( polygon, self.canvas )
        self.polygons.add( polygon, polygonGfx, polygonGfx.polygonId )
        self.manipulator.CheckCollisions( self.hideState )

    def on_token_press(self, event):
        self.manipulator.OnDragStart( event.x, event.y )

    def on_token_release(self, event):
        self.manipulator.OnDragEnd()

    def on_token_motion(self, event):
        self.manipulator.OnDrag( event.x, event.y, self.hideState )

if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.mainloop()
