'''
Python module containing "Master" classes of easy_gui project.
The classes in here are designed to be subclassed in user applications.
'''
import tkinter as tk
import tkinter.scrolledtext
from tkinter import ttk
from .styles import BaseStyle
import os
import sys
import threading
from typing import List

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure



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
        if name in self.sections:
            raise ValueError('Unable to add section as a section with the given name already exists!')
        section = Section(name, title)
        self.sections[name] = section
        if return_section:
            return section

    def delete_section(self, section_name) -> None:
        '''
        Fully delete a section and all of its child widgets.
        Pass without issue if the section doesn't exist.
        '''
        try:
            for key, widget in self.sections[section_name].widgets.items():
                widget._widget.destroy()
            self.sections[section_name].destroy()
            del self.sections[section_name]
        except:
            pass

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
        if title:  # title kwargs can be provided as True or a string
            if isinstance(title, str):  # if string, use title for label text
                self.add_widget(type='label', text=title)
            elif title == True:  # if True, use the name as the label text
                self.add_widget(type='label', text=name)


    def add_widget(self, type='label', text='', widget_name=None, return_widget=False, **kwargs):
        '''
        Add a Widget object to this section
        '''
        def new_widget_name(w_type):
            if widget_name:
                return widget_name
            else:
                return f'{len(self.widgets) + 1}' + '_' + w_type

        if type.lower() in ['label', 'lbl']:
            new_widget = Label(master=self, text=text, **kwargs)
            new_widget.place()
            self.widgets[new_widget_name('label')] = new_widget
        elif type.lower() in ['button', 'btn']:
            new_widget = Button(master=self, text=text, **kwargs)
            new_widget.place()
            self.widgets[new_widget_name('button')] = new_widget
        elif type.lower() == 'entry':
            new_widget = Entry(master=self, **kwargs)
            new_widget.place()
            self.widgets[new_widget_name('entry')] = new_widget
        elif type.lower() == 'dropdown':
            new_widget = DropDown(master=self, **kwargs)
            new_widget.place()
            self.widgets[new_widget_name('dropdown')] = new_widget
        elif type.lower() == 'tree':
            new_widget = Tree(master=self, **kwargs)
            new_widget.place()
            self.widgets[new_widget_name('tree')] = new_widget
        elif type.lower() == 'matplotlib':
            new_widget = MatplotlibPlot(master=self, section=self, widget_name=new_widget_name('matplotlibplot'), **kwargs)
            new_widget.place()
            self.widgets[new_widget_name('matplotlibplot')] = new_widget
        elif type.lower() == 'stdout':
            new_widget = StdOutBox(master=self, **kwargs)
            new_widget.place()
            self.widgets[new_widget_name('stdout')] = new_widget
        elif type.lower() == 'scrolledtext':
            new_widget = ScrolledText(master=self, **kwargs)
            new_widget.place()
            self.widgets[new_widget_name('scrolledtext')] = new_widget
        else:
            raise Exception(f'Error!  Widget type "{type}" not supported. (check spelling?)\n')
        if return_widget:
            return new_widget

    def delete_widget(self, widget_name) -> None:
        '''
        Fully delete a widget.
        Pass without issue if the widget doesn't exist.
        '''
        try:
            self.widgets[widget_name].destroy()
            del self.widgets[widget_name]
        except:
            pass

    def delete_all_widgets(self) -> None:
        '''
        Fully delete all child widgets of this section.
        '''
        for w_name in list(self.widgets.keys()):
            self.delete_widget(w_name)

    def _clear_and_recreate_plot(self, mpl_figure, widget_name, kwargs):
        self.delete_widget(widget_name)
        new_widget = self.add_widget(type='matplotlib', widget_name=widget_name, return_widget=True)
        new_widget.draw_plot(mpl_figure=mpl_figure)


    def replace_widget(self, widget_name='', type='label', text='', return_widget=False, **kwargs):
        '''
        Replace a widget with a new one.
        '''
        if type.lower() == 'matplotlib':
            new_widget = MatplotlibPlot(master=self, **kwargs)
            new_widget.place()
            if widget_name == '':
                widget_name = [k for k in self.widgets.keys() if 'matplotlibplot' in k][0]
            self.widgets[widget_name] = new_widget
        if return_widget:
            return new_widget





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


    def bind_click(self, command_func, separate_thread=False) -> None:
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

    def destroy(self):
        self._widget.destroy()





class Button(Widget):
    def __init__(self, master=None, text='button', command_func=lambda x: None, separate_thread=False, **kwargs) -> None:
        super().__init__(self)
        self._widget = tk.Button(master=master, text=text, highlightbackground=EasyGUI.style.button_color, **kwargs)
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
        self._widget = tk.Label(master=master, text=text, bg=EasyGUI.style.widget_bg_color, padx=EasyGUI.style.label_padx, pady=EasyGUI.style.label_pady, **kwargs)


class Entry(Widget):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__()
        self.strvar = tk.StringVar()
        self._widget = tk.Entry(master=master, textvariable=self.strvar, **kwargs)

    def get(self):
        return self._widget.get()


class DropDown(Widget):
    def __init__(self, master=None, dropdown_options=[], **kwargs) -> None:
        super().__init__()
        self.strvar = tk.StringVar()
        self.dropdown_options = dropdown_options
        self._widget = ttk.Combobox(master, textvariable=self.strvar, values=dropdown_options, **kwargs)

    def get(self):
        return self._widget.get()

    def set_options(self, dropdown_options):
        self._widget['values'] = dropdown_options
        self.strvar.set('')


class Tree(Widget):
    def __init__(self, master=None, tree_col_header: str='Name', tree_col_width: int=120, **kwargs) -> None:
        super().__init__()

        self._widget = ttk.Treeview(master, columns=(), style='Treeview', show='tree headings', height=30, **kwargs)
        self.tree_col_header = tree_col_header
        self.column_definitions = [{'column_name': '#0', 'width': tree_col_width, 'minwidth': 20, 'stretch': tk.NO}]
        self.scrollbar = ttk.Scrollbar(master, orient='vertical')


    def insert_column(self, column_name, width=120, minwidth=40, stretch=tk.YES) -> None:
        '''
        Insert a column and associated heading (column title) at the top in the tree.
        Use "column_name" arg both for the displayed text and to reference this column in code.
        '''
        self.column_definitions.append({'column_name': column_name, 'width': width, 'minwidth': minwidth, 'stretch': stretch})
        self._rebuild_columns()

    def _rebuild_columns(self) -> None:
        '''
        Recreate columns each time one is added, because all columns
        must be set up before assigning headers.
        '''
        columns = [col['column_name'] for col in self.column_definitions]
        self._widget['columns'] = columns[1:]  # don't include assumed first "tree" column

        for col in self.column_definitions:
            self._widget.column(col['column_name'], width=col['width'], minwidth=col['minwidth'], stretch=col['stretch'])

        self._widget.heading('#0', text=self.tree_col_header, anchor=tk.W)
        for col in self.column_definitions[1:]:
            self._widget.heading(col['column_name'], text=col['column_name'], anchor=tk.W)

    def insert_row(self, text, values=('',), parent_row=None, return_row=False, open=False):
        '''
        Values arg must be provided as tuple of strings
        '''
        if parent_row is None:
            new_row = self._widget.insert('', 'end', text=text, values=values, open=open)
        else:
            new_row = self._widget.insert(parent_row, 'end', text=text, values=values, open=open)
        if return_row:
            return new_row

    def clear(self) -> None:
        '''
        Clear all items from the tree.
        '''
        self._widget.delete(*self._widget.get_children())

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
    def __init__(self, master=None, section=None, widget_name=None, **kwargs) -> None:
        super().__init__()
        self.section = section  # grabbing handle to Section so IT can handle replotting
        self.widget_name = widget_name
        self.kwargs = kwargs
        self._widget = tk.Canvas(master=master, **kwargs)
        self.plot_drawn = False

    def draw_plot(self, mpl_figure=None) -> None:
        '''
        Draw new Matplotlib Figure (mpl_figure kwarg) on the widget.

        If a plot already exists, call parent section._clear_and_recreate_plot method
        to destroy and then recreate this widget!
        Must fully destroy this widget to clear all of the matplotlib/tkinter objects.
        '''
        if self.plot_drawn:
            self.section._clear_and_recreate_plot(mpl_figure, self.widget_name, self.kwargs)
        else:
            self.plot_drawn = True
            self.mpl_figure = mpl_figure

            if not hasattr(self, 'fig_canvas'):
                self.fig_canvas = FigureCanvasTkAgg(self.mpl_figure, self._widget)
            else:
                FigureCanvasTkAgg.figure = self.mpl_figure

            if not hasattr(self, 'toolbar'):
                self.toolbar = NavigationToolbar2Tk(self.fig_canvas, self._widget)
            self.toolbar.update()
            self.fig_canvas.draw()
            self.fig_canvas.get_tk_widget().pack(expand=True)



class StdOutBox(Widget):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__()
        self._widget = tk.Text(master, wrap='word', **kwargs)
        sys.stdout = self

    def write(self, s):
        '''Write printed text to text box on a new line'''
        self._widget.insert(tk.END, s)
        self._widget.see(tk.END)

    def flush(self):
        '''
        Method must be implemented for stdout replacement.
        Makes self a 'file-like object'.
        '''
        pass


class ScrolledText(Widget):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__()
        self._widget = tk.scrolledtext.ScrolledText(master, wrap=tk.WORD, **kwargs)

    def get(self) -> List[str]:
        '''Return the lines of text in this widget'''
        return list(self._widget.get(1.0, tk.END).split('\n'))


class DatePicker(Widget):
    '''
    Widget for selecting a date - calendar style.
    '''
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__()

        # TODO: Make this widget...
