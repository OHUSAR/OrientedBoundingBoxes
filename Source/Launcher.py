from tkinter import *
from GUI.gui import Application
from Core.Utils.Logger import LOGGER

_DEBUG = True

LOGGER.setDebug( _DEBUG )

root = Tk()
app = Application(master=root, DEBUG = _DEBUG )
app.mainloop()
