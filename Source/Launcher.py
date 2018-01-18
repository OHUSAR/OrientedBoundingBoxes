from tkinter import *
from GUI.gui import Application

_DEBUG = True

root = Tk()
app = Application(master=root, DEBUG = _DEBUG )
app.mainloop()
