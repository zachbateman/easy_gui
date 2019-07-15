'''
Python module containing "Master" classes of easy_gui project.
The classes in here are designed to be subclassed in user applications.
'''
import tkinter as tk
from .styles import BaseStyle
import os



class EasyGUI(tk.Tk):
    '''
    Main class to be subclassed for full GUI window.
    '''
    style = BaseStyle()

    def __init__(self) -> None:
        super().__init__()

        self.iconbitmap(bitmap=os.path.join(os.path.dirname(__file__), 'resources', 'transparent.ico'))
        self.title('EasyGUI')
        self.geometry("800x600")
        self.configure(background=self.style.window_color)

        self.add_menu()

        self.sections: dict = {}

        for name, section in self.sections.items():
            section.pack()


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


    def add_menu(self, commands=
                                   {'File': lambda: print('File button'), 'Edit': lambda: print('Edit button')},
                                   cascades=
                                   {'Options': {'Option 1': lambda: print('Option 1'), 'Option 2': lambda: print('Option 2')}}):
        '''
        Add a Menu to the top of the root window.
        '''
        self.menu = tk.Menu(self)

        for label, cmd in commands.items():
            self.menu.add_command(label=label, command=cmd)

        for cascade, c_commands in cascades.items():
            cascade_menu = tk.Menu(self.menu, tearoff=0)
            for label, cmd in c_commands.items():
                cascade_menu.add_command(label=label, command=cmd)
            self.menu.add_cascade(label=cascade, menu=cascade_menu)

        self.config(menu=self.menu)



class Section(tk.Frame):
    '''
    A Section is a tk.Frame used for storing and managing widgets.
    '''
    def __init__(self, name='') -> None:
        super().__init__()
        self.name = name

        self.widgets: dict = {}
        self.pack()


    def add_widget(self, type='label', text=''):
        '''
        Add a Widget object to this section
        '''
        # TODO
        if type.lower() == 'label':
            new_widget = Label(master=self, text=text)
            new_widget.place()
            self.widgets[f'{len(self.widgets) + 1}_button'] = new_widget
        elif type.lower() == 'button':
            new_widget = Button(master=self, text=text)
            new_widget.place()
            self.widgets[f'{len(self.widgets) + 1}_button'] = new_widget





class Widget(tk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(bg=EasyGUI.style.widget_bg_color)


    def place(self) -> None:
        '''
        Place widget in parent Section; just pack for now.
        Later, get more sophisticated with positioning...
        '''
        self._widget.pack()



class Button(Widget):
    def __init__(self, master=None, text='button') -> None:
        super().__init__()
        self._widget = tk.Button(master=master, text=text, bg=EasyGUI.style.button_color)


class Label(Widget):
    def __init__(self, master=None, text='label') -> None:
        super().__init__()
        self._widget = tk.Label(master=master, text=text, bg=EasyGUI.style.widget_bg_color)


class Tree(Widget):
    def __init__(self, master=None) -> None:
        super().__init__()
