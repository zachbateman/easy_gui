'''
Python module containing "Master" classes of easy_gui project.
The classes in here are designed to be subclassed in user applications.
'''
import tkinter as tk
from .styles import BaseStyle
import os
import threading



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


    def mouse_scroll(self, event) -> None:
        # TODO
        pass


    def add_section(self, name='', title=False, return_section=False) -> None:
        '''
        Add a Section object to the root window.
        '''
        if name == '':
            name = f'section{len(self.sections) + 1}'
        # TODO
        section = Section(name, title)
        self.sections[name] = section
        if return_section:
            return section


    def add_menu(self,
                 commands={'File': lambda: print('File button'), 'Edit': lambda: print('Edit button')},
                 cascades={'Options': {'Option 1': lambda: print('Option 1'), 'Option 2': lambda: print('Option 2')}}) -> None:
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
    def __init__(self, name='', title=False) -> None:
        super().__init__(borderwidth=1,
                                bg=EasyGUI.style.section_color,
                                padx=EasyGUI.style.frame_padx,
                                pady=EasyGUI.style.frame_pady,
                                relief='ridge')
        self.name = name

        self.widgets: dict = {}
        self.pack()
        if title:  # title kwarg can be provided as True or a string
            if isinstance(title, str):  # if string, use title for label text
                self.add_widget(type='label', text=title)
            elif title == True:  # if True, use the name as the label text
                self.add_widget(type='label', text=name)


    def add_widget(self, type='label', text='', **kwargs):
        '''
        Add a Widget object to this section
        '''
        if type.lower() == 'label':
            new_widget = Label(master=self, text=text, **kwargs)
            new_widget.place()
            self.widgets[f'{len(self.widgets) + 1}_button'] = new_widget
        elif type.lower() == 'button':
            new_widget = Button(master=self, text=text, **kwargs)
            new_widget.place()
            self.widgets[f'{len(self.widgets) + 1}_button'] = new_widget
        elif type.lower() == 'matplotlib':
            new_widget = MatplotlibPlot(master=self, **kwargs)
            new_widget.place()
            self.widgets[f'{len(self.widgets) + 1}_matplotlibplot'] = new_widget





class Widget(tk.Frame):
    '''
    To be subclassed into specific EasyGUI widgets.
    Class assumes the "_widget" attribute is the actual tkinter widget (if used)
    '''
    def __init__(self, master=None, bg=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.configure(background=EasyGUI.style.widget_bg_color)


    def place(self) -> None:
        '''
        Place widget in parent Section; just pack for now.
        Later, get more sophisticated with positioning...
        '''
        self._widget.pack()


    def bind_click(self, command_func=lambda e: print('TEST'), separate_thread=False) -> None:
        '''
        Bind a left-mouse click to the widget to trigger a target "command_func" function.
        Note that the "_widget" attribute of subclasses is assumed to be the tkinter widget itself!!!
        '''
        if separate_thread:
            def threaded_command_func(*args):
                threading.Thread(target=command_func).start()
            self._widget.bind('<Button-1>', threaded_command_func)
        else:
            self._widget.bind('<Button-1>', command_func)





class Button(Widget):
    def __init__(self, master=None, text='button', command_func=lambda e: print('TEST'), separate_thread=False, **kwargs) -> None:
        super().__init__(self)
        self._widget = tk.Button(master=master, text=text, highlightbackground=EasyGUI.style.button_color)
        self.bind_click(command_func, separate_thread)

    def place(self) -> None:
        '''
        Override Widget method for proper padding on outside!
        (have to supply padx and pady on pack call for button
        '''
        self._widget.pack(padx=EasyGUI.style.button_padx, pady=EasyGUI.style.button_pady)


class Label(Widget):
    def __init__(self, master=None, text='label', **kwargs) -> None:
        super().__init__()
        self._widget = tk.Label(master=master, text=text, bg=EasyGUI.style.widget_bg_color, padx=EasyGUI.style.label_padx, pady=EasyGUI.style.label_pady)


class Tree(Widget):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__()

    def up_arrow(self, a) -> None:
        '''
        Go up a selection in the tree on user's up-arrow.
        '''
        pass

    def down_arrow(self, a) -> None:
        '''
        Go down a selection in the tree on user's down-arrow.
        '''
        pass


class MatplotlibPlot(Widget):
    def __init__(self, master=None, **kwargs) -> None:
        import matplotlib
        matplotlib.use('TkAgg')
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        from matplotlib.figure import Figure

        super().__init__()
        self._widget = tk.Canvas(master=master)

    def draw_plot(self, mpl_figure=None) -> None:
        '''
        Draw new Matplotlib Figure (mpl_figure kwarg) on the widget.
        '''
        pass
