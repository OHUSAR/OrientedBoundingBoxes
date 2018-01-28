from tkinter import *
from GUI.gui import Application
from Core.Utils.Logger import LOGGER
from Debug.DrawingTool import DRAW_TOOL

_DEBUG = False

LOGGER.setDebug( _DEBUG )
DRAW_TOOL.setDebug( _DEBUG )

cWidth = 1200
cHeight = 800

if _DEBUG:
    cWidth = 300
    cHeight = 300

root = Tk()
app = Application(master=root, DEBUG = _DEBUG, width = cWidth, height = cHeight )
app.mainloop()
