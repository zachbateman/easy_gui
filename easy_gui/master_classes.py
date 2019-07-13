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

        self.add_menu()

        self.sections: dict = {}


    def mouse_scroll(self, event):
        # TODO
        pass


    def add_section(self, name=''):
        '''
        Add a Section object to the root window.
        '''
        if name == '':
            name = f'section{len(self.sections) + 1}'
        # TODO
        section = Section(name)

        self.sections[name] = section


    def add_menu(self, commands={'File': lambda: print('File button'), 'Edit': lambda: print('Edit button')}):
        '''
        Add a Menu to the top of the root window.
        '''
        self.menu = tk.Menu(self)

        for label, cmd in commands.items():
            self.menu.add_command(label=label, command=cmd)

        self.config(menu=self.menu)



class Section(tk.Frame):
    '''
    A Section is a tk.Frame used for storing and managing widgets.
    '''
    def __init__(self, name='') -> None:
        super().__init__()
        self.name = name

        self.widgets: dict = {}


    def add_widget(self, type='label'):
        '''
        Add a Widget object to this section
        '''
        # TODO
        self.widgets['...'] = Widget()





class Widget(tk.Frame):
    def __init__(self) -> None:
        super().__init__()
