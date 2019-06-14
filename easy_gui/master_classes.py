'''
Python module containing "Master" classes of easy_gui project.
The classes in here are designed to be subclassed in user applications.
'''
import tkinter as tk
from .styles import BaseStyle
import os



class EasyGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.style = BaseStyle()

        self.iconbitmap(bitmap=os.path.join(os.path.dirname(__file__), 'resources', 'transparent.ico'))
        self.title('EasyGUI')
        self.geometry("800x600")
        self.configure(background=self.style.window_color)


    def mouse_scroll(self, event):
        # TODO
        pass



class NewWidget(tk.Frame):
    def __init__(self) -> None:
        super().__init__()
