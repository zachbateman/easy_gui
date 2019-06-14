'''
Python module containing "Master" classes of easy_gui project.
The classes in here are designed to be subclassed in user applications.
'''
import tkinter as tk


class EasyGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title('EasyGUI')
        self.geometry("800x600")


    def mouse_scroll(self, event):
        # TODO
        pass


class NewWidget(tk.Frame):
    def __init__(self) -> None:
        super().__init__()
