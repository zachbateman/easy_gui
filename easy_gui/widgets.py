'''
Python module containing Widget classes (Widget subclasses) of easy_gui project.
The classes in here are the individual GUI elements.
'''
# from .master_classes import Widget
import tkinter as tk
import tkinter.scrolledtext
from tkinter import ttk
from tkinter import _tkinter
import sys
import threading
from typing import List
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure




class Widget(tk.Frame):
    '''
    To be subclassed into specific EasyGUI widgets.
    Class assumes the "_widget" attribute is the actual tkinter widget (if used)
    '''
    def __init__(self, master=None, bg=None, grid_area=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.parent = master  # master attr used in tkinter; parent attr used in this code
        self.grid_area = grid_area
        self.configure(background=self.style.widget_bg_color)

    @property
    def style(self):
        '''Goes upsteam to evenually reference EasyGUI.style'''
        return self.parent.style

    def position(self, force_pack: bool=False) -> None:
        '''
        Physically position this Widget within its parent Section.
        '''
        if self.grid_area and not force_pack:
            try:
                bounds = self.parent.grid_areas[self.grid_area]
                try:
                    self._widget.grid(row=bounds['first_row'], column=bounds['first_column'], rowspan=bounds['last_row']-bounds['first_row']+1, columnspan=bounds['last_column']-bounds['first_column']+1)
                except _tkinter.TclError:
                    print(f'\n--- GRID FAILED for Widget: "{self}" ---\nTry ensuring "grid_area" arg is given for all Sections in a given parent.'
                           '\nUsing "pack" placement instead.')
                    self.parent.create(force_pack=True)  # go back and fully recreate section forcing all children to be packed
            except KeyError:
                print(f'"{self.grid_area}" not found in "{self.parent.name}" Section grid areas.\nResorting to pack.')
                self._widget.pack()
        else:
            self._widget.pack()

    def bind_click(self, command_func, separate_thread: bool=False) -> None:
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

    def bind_event(self, event: str, command_func, separate_thread: bool=False) -> None:
        '''
        Bind an event (specified by "event" string such as '<<ComboboxSelected>>' to trigger a target "command_func" function.
        Note that the "_widget" attribute of subclasses is assumed to be the tkinter widget itself!!!
        '''
        if separate_thread:
            def threaded_command_func(*args):
                threading.Thread(target=command_func).start()
            self._widget.bind(event, threaded_command_func)
        else:
            self._widget.bind(event, command_func)

    def destroy(self):
        self._widget.destroy()

    @property
    def width(self) -> float:
        '''
        Return width used by this Widget.
        '''
        return float(self._widget['width'])

    @property
    def height(self) -> float:
        '''
        Return height used by this Widget.
        '''
        return float(self._widget['height'])


def add_widget(self, type='label', text='', widget_name=None, grid_area=None, **kwargs):
        '''
        Add a Widget subclass object to the 'self' Section.
        This is used as a Section method in master_classes.Section.
        ('self' is passed in as a reference to the parent Section)
        '''
        def new_widget_name(w_type):
            if widget_name:
                return widget_name
            else:
                return f'{len(self.widgets) + 1}' + '_' + w_type

        if type.lower() in ['label', 'lbl']:
            new_widget = Label(master=self, text=text, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('label')] = new_widget
        elif type.lower() in ['button', 'btn']:
            new_widget = Button(master=self, text=text, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('button')] = new_widget
        elif type.lower() == 'entry':
            new_widget = Entry(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('entry')] = new_widget
        elif type.lower() in ['checkbox', 'checkbutton']:
            new_widget = CheckBox(master=self, text=text, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('checkbox')] = new_widget
        elif type.lower() == 'dropdown':
            new_widget = DropDown(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('dropdown')] = new_widget
        elif type.lower() == 'listbox':
            new_widget = ListBox(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('listbox')] = new_widget
        elif type.lower() == 'tree':
            new_widget = Tree(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('tree')] = new_widget
        elif type.lower() == 'matplotlib':
            new_widget = MatplotlibPlot(master=self, section=self, widget_name=new_widget_name('matplotlibplot'), grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('matplotlibplot')] = new_widget
        elif type.lower() == 'stdout':
            new_widget = StdOutBox(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('stdout')] = new_widget
        elif type.lower() == 'scrolledtext':
            new_widget = ScrolledText(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('scrolledtext')] = new_widget
        elif type.lower() in ['progress', 'progressbar']:
            new_widget = ProgressBar(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('progressbar')] = new_widget
        else:
            raise Exception(f'Error!  Widget type "{type}" not supported. (check spelling?)\n')

        return new_widget



class Button(Widget):
    def __init__(self, master=None, text='button', command_func=lambda x: None, separate_thread=False, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.text = text
        del kwargs['grid_area']
        self._widget = tk.Button(master=master, text=text, highlightbackground=self.style.button_color, font=self.style.font, **kwargs)
        self.bind_click(command_func, separate_thread)

    def place(self) -> None:
        '''
        Override Widget method for proper padding on outside!
        (have to supply padx and pady on pack call for button
        '''
        self._widget.pack(padx=self.style.button_padx, pady=self.style.button_pady)

    @property
    def width(self) -> float:
        '''
        Return width used by this Button.
        Overwrites Widget method.
        '''
        return 6.6 * len(self.text)

    @property
    def height(self) -> float:
        '''
        Return height used by this Button.
        Overwrites Widget method.
        '''
        return 39


class Label(Widget):
    def __init__(self, master=None, text='label', **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.text = text
        del kwargs['grid_area']
        self._widget = tk.Label(master=master, text=text, bg=self.style.widget_bg_color, fg=self.style.text_color,
                                padx=self.style.label_padx, pady=self.style.label_pady, font=self.style.font, **kwargs)

    @property
    def width(self) -> float:
        '''
        Return width used by this Label.
        Overwrites Widget method.
        '''
        return 6.6 * len(self.text)

    @property
    def height(self) -> float:
        '''
        Return height used by this Label.
        Overwrites Widget method.
        '''
        return 39


class Entry(Widget):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.strvar = tk.StringVar()
        del kwargs['grid_area']
        self._widget = tk.Entry(master=master, textvariable=self.strvar, **kwargs)

    def get(self):
        return self._widget.get()

    def set(self, value):
        self.strvar.set(value)


class CheckBox(Widget):
    def __init__(self, master=None, text='checkbox', **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        del kwargs['grid_area']
        self._widget = ttk.Checkbutton(master=master, text=text, offvalue=False, onvalue=True, **kwargs)
        self._widget.invoke()  # switch from whatever starting state to checked
        self._widget.invoke()  # switch from checked to unchecked

    def get(self) -> bool:
        return True if 'selected' in self._widget.state() else False


class DropDown(Widget):
    def __init__(self, master=None, dropdown_options=[], **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.strvar = tk.StringVar()
        self.dropdown_options = dropdown_options
        del kwargs['grid_area']
        self._widget = ttk.Combobox(master, textvariable=self.strvar, values=dropdown_options, **kwargs)

    def get(self):
        return self._widget.get()

    def set(self, value):
        if value in self.dropdown_options:
            self.strvar.set(value)
        else:
            print(f'Error: {value} is not in current dropdown_options.')
            print('Please set to an existing option or use .set_options to set a new list of dropdown_options.')

    def set_options(self, dropdown_options):
        self._widget['values'] = dropdown_options
        self.strvar.set('')

    def bind_select(self, command_func, separate_thread: bool=False):
        '''
        Shortcut/convenience binding method
        '''
        self.bind_event('<<ComboboxSelected>>', command_func, separate_thread=separate_thread)


class ListBox(Widget):
    def __init__(self, master=None, options=[], **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.options = options
        del kwargs['grid_area']
        self._widget = tk.Listbox(master, selectmode=tk.MULTIPLE, **kwargs)
        for option in options:
            self._widget.insert(tk.END, option)

    def get(self) -> List[str]:
        return sorted(self._widget.get(i) for i in self._widget.curselection())


class Tree(Widget):
    def __init__(self, master=None, tree_col_header: str='Name', tree_col_width: int=120, **kwargs) -> None:
        super().__init__(master=master, **kwargs)

        del kwargs['grid_area']
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

    def bind_select(self, command_func, separate_thread=False):
        '''
        Shortcut/convenience binding method
        '''
        self.bind_event('<<TreeviewSelect>>', command_func, separate_thread=separate_thread)

    def get_iids(self) -> List[str]:
        '''
        Return list of all row iid values in current order of rows.
        '''
        def children_iids(parent) -> List[str]:
            '''Recursive function that returns (in order) all children of a given iid'''
            running_iids = []
            for child in self._widget.get_children(parent):
                running_iids.append(child)
                grandkids = children_iids(child)
                if grandkids != ():
                    for grandkid in grandkids:
                        running_iids.extend(children_iids(grandkid))
            return running_iids
        iids = []
        for top_level in self._widget.get_children():
            iids.append(top_level)
            iids.extend(children_iids(top_level))
        return iids

    def _up_down_arrow(self, a, up_or_down: str) -> None:
        '''
        Allows Up or Down arrow to change the row selection in the tree
        '''
        current_row = self._widget.focus()
        iids = self.get_iids()
        for iid in iids:  # unselect all rows
            self._widget.item(iid, tags='0')

        current_row_iid_index = next(index for index, iid in enumerate(iids) if iid == current_row)

        if up_or_down == 'up':
            if current_row == iids[0]:
                new_iid = current_row
            else:
                new_iid = iids[current_row_iid_index - 1]
        elif up_or_down == 'down':
            if current_row == iids[-1]:
                new_iid = current_row
            else:
                new_iid = iids[current_row_iid_index + 1]

        self._widget.item(new_iid, tags='selected')
        self._widget.focus(new_iid)

    def up_arrow(self, a) -> None:
        '''
        Go up a selection in the tree on user's up-arrow.
        '''
        self._up_down_arrow(a, 'up')

    def down_arrow(self, a) -> None:
        '''
        Go down a selection in the tree on user's down-arrow.
        '''
        self._up_down_arrow(a, 'down')


class MatplotlibPlot(Widget):
    def __init__(self, master=None, section=None, widget_name=None, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.section = section  # grabbing handle to Section so IT can handle replotting
        self.widget_name = widget_name
        self.grid_area = kwargs.get('grid_area')
        self.kwargs = kwargs
        if 'grid_area' in kwargs:
            del kwargs['grid_area']
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
            self.section._clear_and_recreate_plot(mpl_figure, self.widget_name, self.grid_area, self.kwargs)
        else:
            self.plot_drawn = True
            self.mpl_figure = mpl_figure
            self.fig_canvas = FigureCanvasTkAgg(self.mpl_figure, self._widget)
            self.toolbar = NavigationToolbar2Tk(self.fig_canvas, self._widget)
            self.fig_canvas.get_tk_widget().pack(expand=True)

            # Check if provided figure is wide enough to prevent unstable width changing on mouseover...
            if mpl_figure.bbox._points[1][0] < 400:
                print('\nCaution!  Plot Matplotlib Figure with width >=4 to prevent unstable chart width.')

    def __repr__(self):
        return f'MatplotlibPlot Widget: {self.widget_name} which belongs to: {self.section}'


class ProgressBar(Widget):
    def __init__(self, master=None, orient: str='horizontal', mode='determinate', length=100, **kwargs) -> None:
        '''mode arg can be "determinate" or "indeterminate" '''
        super().__init__(master=master, **kwargs)
        self.length = length
        del kwargs['grid_area']
        self._widget = ttk.Progressbar(master, orient=orient, mode=mode, length=length, **kwargs)
        self._widget['value'] = 0

    def set(self, value: float=0):
        self._widget['value'] = value

    def get(self):
        return self._widget['value']

    def progress_handler(self, *args):
        self._widget['value'] += 1
        if self._widget['value'] > self.length:
            self._widget['value'] %= self.length


class ScrolledText(Widget):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        del kwargs['grid_area']
        self._widget = tk.scrolledtext.ScrolledText(master, wrap=tk.WORD, **kwargs)

    def get(self) -> List[str]:
        '''Return the lines of text in this widget'''
        return list(self._widget.get(1.0, tk.END).split('\n'))


class StdOutBox(Widget):
    def __init__(self, master=None, height: int=10, width: int=30, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        del kwargs['grid_area']
        self._widget = tk.Text(master, wrap='word', height=height, width=width, **kwargs)
        sys.stdout = self

    def write(self, s):
        '''Write printed text to text box on a new line'''
        self._widget.insert(tk.END, s)
        self._widget.see(tk.END)

    def flush(self):
        '''
        Method must be implemented for stdout replacement.
        Makes self a "file-like object."
        '''
        pass


class Tabs(Widget):
    def __init__(self, master=None, height: int=30, width: int=50, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        del kwargs['grid_area']
        self._widget = ttk.Notebook(master, height=height, width=width, **kwargs)

    def bind_change(self, command_func, separate_thread: bool=False):
        '''
        Shortcut/convenience binding method.
        '''
        self.bind_event('<<NotebookTabChanged>>', command_func, separate_thread=separate_thread)


class DatePicker(Widget):
    '''
    Widget for selecting a date - calendar style.
    '''
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master=master, **kwargs)

        # TODO: Make this widget...
