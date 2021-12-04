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
from contextlib import nullcontext
import datetime
import calendar



class Widget(tk.Frame):
    '''
    To be subclassed into specific EasyGUI widgets.
    Class assumes the "_widget" attribute is the actual tkinter widget (if used)
    '''
    def __init__(self, master=None, bg=None, grid_area=None, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.parent = master  # master attr used in tkinter; parent attr used in this code
        self.grid_area = grid_area
        self.configure(background=self.style.widget_bg_color)

    @property
    def style(self):
        '''Goes upsteam to evenually reference EasyGUI.style'''
        return self.parent.style

    @property
    def root(self):
        '''Goes upsteam to evenually reference EasyGUI as root'''
        return self.parent.root

    def position(self, force_row: bool=False) -> None:
        '''
        Physically position this Widget within its parent Section.
        '''
        try:
            if self.parent.grid_areas != {} and self.grid_area and not force_row:
                try:
                    bounds = self.parent.grid_areas[self.grid_area]
                    if isinstance(self, Tree):
                        self.grid(row=bounds['first_row'], column=bounds['first_column'], rowspan=bounds['last_row']-bounds['first_row']+1, columnspan=bounds['last_column']-bounds['first_column']+1, sticky='NSEW')
                        self._widget.pack(side='left', fill=tk.BOTH, expand=True)
                        self.scrollbar.pack(side='left', fill='y')
                    elif isinstance(self, LabelEntry):
                        self.grid(row=bounds['first_row'], column=bounds['first_column'], rowspan=bounds['last_row']-bounds['first_row']+1, columnspan=bounds['last_column']-bounds['first_column']+1)
                        self._lbl_widget.pack(side='left', expand=True)
                        self._widget.pack(side='left')
                    elif isinstance(self, Table):
                        self.grid(row=bounds['first_row'], column=bounds['first_column'], rowspan=bounds['last_row']-bounds['first_row']+1, columnspan=bounds['last_column']-bounds['first_column']+1) #, sticky='NSEW')
                        self.grid_cells()
                    elif isinstance(self, DatePicker):
                        self.grid(row=bounds['first_row'], column=bounds['first_column'], rowspan=bounds['last_row']-bounds['first_row']+1, columnspan=bounds['last_column']-bounds['first_column']+1)
                        self.grid_interior()
                    else:
                        self._widget.grid(row=bounds['first_row'], column=bounds['first_column'], rowspan=bounds['last_row']-bounds['first_row']+1, columnspan=bounds['last_column']-bounds['first_column']+1) #, sticky='NSEW')
                    return  # early return if everything works fine with initial attempt (no other actions needed)
                except KeyError:
                    print(f'"{self.grid_area}" not found in parent\'s grid areas.\nResorting to a new row.')
            name = self.__class__.__name__
            existing_grid_areas = [n for n in self.parent.grid_areas if name in n]
            self.grid_area = name if name not in existing_grid_areas else next((name + str(i) for i in range(1, 100) if name + str(i) not in existing_grid_areas))
            self.parent.add_grid_row(self.grid_area)
            self.parent.create()
        except _tkinter.TclError:
            print(f'\n--- GRID FAILED for Widget: "{ self.__class__.__name__}" ---\nTry ensuring "grid_area" arg is given for all Widgets in a given parent.\nAdding to a new row instead.')
            self.parent.create(force_row=True)  # go back and fully recreate section forcing all children to be packed/in new rows

    def bind_click(self, command_func, separate_thread: bool=False) -> None:
        '''
        Bind a left-mouse click to the widget to trigger a target "command_func" function.
        '''
        self.bind_event('<Button-1>', command_func, separate_thread=separate_thread)

    def bind_select(self, command_func, separate_thread: bool=False) -> None:
        '''
        Bind a left-mouse click to the widget to trigger a target "command_func" function.
        '''
        self.bind_event('<Button-1>', command_func, separate_thread=separate_thread)

    def bind_event(self, event: str, command_func, separate_thread: bool=False) -> None:
        '''
        Bind an event (specified by "event" string such as '<<ComboboxSelected>>' to trigger a target "command_func" function.
        Note that the "_widget" attribute of subclasses is assumed to be the tkinter widget itself!!!
        '''
        if separate_thread:
            def threaded_command_func(*args):
                threading.Thread(target=command_func).start()
            self._widget.bind(event, threaded_command_func, add='+')
        else:
            self._widget.bind(event, command_func, add='+')

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

    def config(self, *args, **kwargs):
        '''Just pass a config call through to the tkinter widget itself.'''
        return self._widget.config(*args, **kwargs)


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

        type_lower = type.lower()
        if type_lower in ['label', 'lbl']:
            new_widget = Label(master=self, text=text, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('label')] = new_widget
        elif type_lower in ['button', 'btn']:
            new_widget = Button(master=self, text=text, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('button')] = new_widget
        elif type_lower in ['canvas']:
            new_widget = Canvas(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('canvas')] = new_widget
        elif type_lower in ['entry', 'input']:
            new_widget = Entry(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('entry')] = new_widget
        elif type_lower in ['labelentry', 'entrylabel']:
            new_widget = LabelEntry(master=self, text=text, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('labelentry')] = new_widget
        elif type_lower in ['checkbox', 'checkbutton']:
            new_widget = CheckBox(master=self, text=text, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('checkbox')] = new_widget
        elif type_lower == 'dropdown':
            new_widget = DropDown(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('dropdown')] = new_widget
        elif type_lower == 'listbox':
            new_widget = ListBox(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('listbox')] = new_widget
        elif type_lower == 'table':
            new_widget = Table(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('table')] = new_widget
        elif type_lower == 'tree':
            new_widget = Tree(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('tree')] = new_widget
        elif type_lower in ['matplotlib', 'matplotlibplot']:
            new_widget = MatplotlibPlot(master=self, section=self, widget_name=new_widget_name('matplotlibplot'), grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('matplotlibplot')] = new_widget
        elif type_lower == 'stdout':
            new_widget = StdOutBox(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('stdout')] = new_widget
        elif type_lower == 'scrolledtext':
            new_widget = ScrolledText(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('scrolledtext')] = new_widget
        elif type_lower == 'slider':
            new_widget = Slider(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('slider')] = new_widget
        elif type_lower in ['progress', 'progressbar']:
            new_widget = ProgressBar(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('progressbar')] = new_widget
        elif type_lower in ['date', 'datepicker']:
            new_widget = DatePicker(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('datepicker')] = new_widget
        else:
            raise Exception(f'Error!  Widget type "{type}" not supported. (check spelling?)\n')

        return new_widget



class Button(Widget):
    def __init__(self, master=None, text='button', image=None, command_func=lambda x: None, separate_thread=False, use_ttk: bool=False, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.text = text
        self.image = None
        if image:
            if image[-4:].lower() != '.png':
                print('Error!  Can only use a ".png" file as a button image.')
            else:
                self.image = tk.PhotoImage(file=image)
        if 'grid_area' in kwargs:
            del kwargs['grid_area']
        if not use_ttk:
            self._widget = tk.Button(master=master, text=text, image=self.image, highlightbackground=self.style.button_color, font=self.style.font, **kwargs)
        else:
            self._widget = ttk.Button(master=master, text=text, image=self.image, **kwargs)
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


class Canvas(Widget):
    def __init__(self, master=None, width=300, height=250, background='gray85', **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        if 'grid_area' in kwargs:
            del kwargs['grid_area']
        self._widget = tk.Canvas(master=master, width=width, height=height, background=background, **kwargs)

    def itemconfigure(self, *args, **kwargs) -> None:
        '''See tkinter.Canvas.itemconfigure... Used to change tagged items.'''
        self._widget.itemconfigure(*args, **kwargs)

    def create_line(self, x1, y1, x2, y2, fill='blue', width=3, tags=None):
        self._widget.create_line(x1, y1, x2, y2, fill=fill, width=width, tags=tags)

    def create_text(self, x, y, text='Text', anchor='nw', fill='black', tags=None):
        self._widget.create_text(x, y, text=text, anchor=anchor, fill=fill, tags=tags)



class Label(Widget):
    def __init__(self, master=None, text='label', bold=False, underline=False, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.text = text
        self.strvar = tk.StringVar()
        self.set(text)
        if 'grid_area' in kwargs:
            del kwargs['grid_area']
        font = self.style.font
        if bold:
            font = self.style.font_bold
        if underline:
            font = self.style.font_underline
        if bold and underline:
            font = self.style.font_bold_underline
        self._widget = tk.Label(master=master, textvariable=self.strvar, bg=self.style.widget_bg_color, fg=self.style.text_color,
                                padx=self.style.label_padx, pady=self.style.label_pady, font=font, **kwargs)

    def get(self):
        return self.strvar.get()

    def set(self, value):
        self.strvar.set(value)

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
        if 'grid_area' in kwargs:
            del kwargs['grid_area']
        self._widget = tk.Entry(master=master, textvariable=self.strvar, **kwargs)

    def get(self):
        return self._widget.get()

    def set(self, value):
        self.strvar.set(value)


class LabelEntry(Widget):
    '''
    Widget combining a Label and and Entry in one (common use case).
    '''
    def __init__(self, master=None, text='label', bold=False, underline=False, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.text = text
        self.lbl_strvar = tk.StringVar()
        self.set(text)
        del kwargs['grid_area']
        font = self.style.font
        if bold:
            font = self.style.font_bold
        if underline:
            font = self.style.font_underline
        if bold and underline:
            font = self.style.font_bold_underline
        self._lbl_widget = tk.Label(master=self, textvariable=self.lbl_strvar, bg=self.style.widget_bg_color, fg=self.style.text_color,
                                padx=self.style.label_padx, pady=self.style.label_pady, font=font, **kwargs)

        self.strvar = tk.StringVar()
        self._widget = tk.Entry(master=self, textvariable=self.strvar, **kwargs)

    def destroy(self):
        '''Need custom destroy method as also have a _lbl_widget.'''
        self._lbl_widget.destroy()
        self._widget.destroy()

    def get(self):
        '''Get the value in the Entry box.'''
        return self._widget.get()

    def set(self, value):
        '''Set the value in the Label.'''
        self.lbl_strvar.set(value)


class CheckBox(Widget):
    def __init__(self, master=None, text='checkbox', **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        del kwargs['grid_area']
        self._widget = ttk.Checkbutton(master=master, text=text, offvalue=False, onvalue=True, **kwargs)
        self._widget.invoke()  # switch from whatever starting state to checked
        self._widget.invoke()  # switch from checked to unchecked

    def get(self) -> bool:
        return True if 'selected' in self._widget.state() else False

    def switch(self):
        self._widget.invoke()

    def check(self):
        if not self.get():
            self.switch()

    def uncheck(self):
        if self.get():
            self.switch()


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


class Table(Widget):
    # TODO:
    # Need copy/paste ability if enabled
    # Want to be able to double-click on a cell and trigger event (like drill down into more data with a popup window?)
    def __init__(self, master=None, widget_name=None, type:str='label', rows:int=4, columns:int=3, border: bool=False, **kwargs) -> None:
        '''
        type can be 'label' or 'entry'
        '''
        super().__init__(master=master, **kwargs)
        self.widget_name = widget_name
        self.type = type
        self.rows = rows
        self.column = columns
        self.grid_area = kwargs.get('grid_area')
        self.kwargs = kwargs
        if 'grid_area' in kwargs:
            del kwargs['grid_area']

        self.cells = {row: {col: None for col in range(1, columns+1)} for row in range(1, rows+1)}
        self.cell_list = []  # another reference to the same cell objects in list form for easier access in some cases
        for row in range(1, rows+1):
            for col in range(1, columns+1):
                if self.type == 'label':
                    new_cell = Label(master=self, borderwidth=(1 if border else 0), relief='solid')  # self is a tk.Frame
                    new_cell.set(f'Cell [{row}, {col}]')
                elif self.type == 'entry':
                    new_cell = Entry(master=self)  # self is a tk.Frame
                new_cell.row = row
                new_cell.column = col
                self.cells[row][col] = new_cell
                self.cell_list.append(new_cell)


    def grid_cells(self):
        for cell in self.cell_list:
            cell._widget.grid(row=cell.row-1, column=cell.column-1, sticky='NSEW')

    def __getitem__(self, indices):
        row, column = indices
        return self.cells[row][column].get()

    def __setitem__(self, indices, value):
        row, column = indices
        self.cells[row][column].set(value)

    def destroy(self):
        for cell in self.cell_list:
            cell.destroy()


class Tree(Widget):
    def __init__(self, master=None, tree_col_header: str='Name', height: int=30, tree_col_width: int=120, **kwargs) -> None:
        super().__init__(master=master, **kwargs)

        del kwargs['grid_area']
        self._widget = ttk.Treeview(self, columns=(), style='Treeview', show='tree headings', height=height, **kwargs)
        self.tree_col_header = tree_col_header
        self.column_definitions = [{'column_name': '#0', 'width': tree_col_width, 'minwidth': 20, 'stretch': tk.NO}]
        self.scrollbar = ttk.Scrollbar(self, orient='vertical')
        self.scrollbar.configure(command=self._widget.yview)
        self._widget.configure(yscrollcommand=self.scrollbar.set)


    @property
    def current_row(self) -> dict:
        return self._widget.item(self._widget.focus())

    @property
    def current_rows(self) -> List[dict]:
        return [self._widget.item(id) for id in self._widget.selection()]

    def select_first_row(self):
        self._widget.focus(self._widget.get_children()[0])
        self._widget.selection_set(self._widget.get_children()[0])

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

    def insert_row(self, text, values=('',), parent_row=None, open=False):
        '''
        Values arg must be provided as tuple of strings
        '''
        if parent_row is None:
            new_row = self._widget.insert('', 'end', text=text, values=values, open=open)
        else:
            new_row = self._widget.insert(parent_row, 'end', text=text, values=values, open=open)
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
        def command_func_with_tree_reselect(*args):
            command_func()
            # NEXT LINE NECESSARY to allow refocusing on tree due to odd Matplotlib behavior/bug?
            # See: https://github.com/matplotlib/matplotlib/issues/14081  (issue with FigureCanvasTkAgg.__init__ steals focus)
            self.root.update()
            self._widget.focus_set()  # want to refocus/keep focus on tree if lost it during command_func

        self.bind_event('<<TreeviewSelect>>', command_func_with_tree_reselect, separate_thread=separate_thread)


class Slider(Widget):
    def __init__(self, master=None, min=0, max=100, start=None, resolution=5, tickinterval=25, length=10, hz_or_vt='vt',
                      command_func=None, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        del kwargs['grid_area']
        orient = 'horizontal' if hz_or_vt.lower() == 'hz' else 'vertical'
        self._widget = tk.Scale(master, from_=min, to=max, resolution=resolution, tickinterval=tickinterval, orient=orient,
                                        length=length, command=command_func, **kwargs)
        if start:
            self.set(start)

    def get(self):
        return self._widget.get()

    def set(self, value):
        self._widget.set(value)


class MatplotlibPlot(Widget):
    def __init__(self, master=None, section=None, widget_name=None, toolbar=True, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.section = section  # grabbing handle to Section so IT can handle replotting
        self.widget_name = widget_name
        self.toolbar = toolbar
        self.grid_area = kwargs.get('grid_area')
        self.kwargs = kwargs
        if 'grid_area' in kwargs:
            del kwargs['grid_area']
        self._widget = tk.Canvas(master=master, **kwargs)
        self.plot_drawn = False
        self.bindings = []
        self.small_figure_warning_given = False

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
            self.fig_canvas = FigureCanvasTkAgg(mpl_figure, self._widget)
            if self.toolbar:
                toolbar = NavigationToolbar2Tk(self.fig_canvas, self._widget)
                # NOW TO MINIMIZE CRAZY FLICKERING/REDRAWING......
                # The next line overwrites and ignores the ._wait_cursor_for_draw_cm method
                # which is a context manager call in matplotlib.backends.backend_agg.FigureCanvasAgg.draw (line ~390).
                # This context manager appears to only attempt to change the cursor to a "wait" cursor... but I don't see it actually doing that,
                # and it's slow and therefore making the plot redraw take way too long and look ridiculous.
                toolbar._wait_cursor_for_draw_cm = lambda: nullcontext()
            self.fig_canvas.get_tk_widget().pack(expand=True)

            self.reset_bindings()
            # Check if provided figure is wide enough to prevent unstable width changing on mouseover...
            if mpl_figure.bbox._points[1][0] < 400 and not self.small_figure_warning_given:
                print('\nCaution!  Plot Matplotlib Figure with width >=4 to prevent unstable chart width.')
                self.small_figure_warning_given = True  # used to only print warning once

    def bind_event(self, event: str, command_func, separate_thread: bool=False) -> None:
        '''
        Custom bind_event method as need to intercept/store these and bind them AFTER every call to draw_plot.
        '''
        self.bindings.append((event, command_func, separate_thread))

    def reset_bindings(self):
        for event, command_func, separate_thread in self.bindings:
            if separate_thread:
                def threaded_command_func(*args):
                    threading.Thread(target=command_func).start()
                self.fig_canvas._tkcanvas.bind(event, threaded_command_func, add='+')
            else:
                self.fig_canvas._tkcanvas.bind(event, command_func, add='+')

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


class DatePicker(Widget):
    '''
    Widget for selecting a date - calendar style.
    '''
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self._widget = self
        self.grid_area = kwargs.get('grid_area')
        self.kwargs = kwargs
        if 'grid_area' in kwargs:
            del kwargs['grid_area']

        self.selected_day = None
        self.selected_month = 9
        self.selected_year = 2021

        self.previous_month_btn = Button(master=self, text='<')
        self.previous_month_btn.bind_click(self.previous_month)
        self.current_month_year = Label(master=self)
        self.update_month_year()
        self.next_month_btn = Button(master=self, text='>')
        self.next_month_btn.bind_click(self.next_month)

        self.day_labels = []
        first_day, days_in_month = calendar.monthrange(self.selected_year, self.selected_month)
        self.build_days(days_in_month)


    def build_days(self, max_day):
        '''Handle creating labels (toggles/buttons) for each day in the month.'''
        if self.day_labels:
            for lbl in self.day_labels:
                lbl.destroy()
            self.day_labels = []

        for day_count in range(1, max_day+1):
            day_lbl = Label(master=self, text=day_count, borderwidth=1, relief='raised')  # self is a tk.Frame
            self.day_labels.append(day_lbl)

        # Not totally sure why below shenanigans is needed...
        # But had trouble with last day getting reference for all day clicks.
        def config_func(label):
            def func(*args):
                for lbl in self.day_labels:
                    lbl.config(bg=self.style.widget_bg_color)
                label.config(bg='#99BBFF')
                self.selected_day = int(label.get())
            return func
        for label in self.day_labels:
            label.bind_click(config_func(label))

    def get(self) -> datetime.date:
        try:
            return datetime.date(self.selected_year, self.selected_month, self.selected_day)
        except:
            return None

    def previous_month(self, *args):
        if self.selected_month == 1:
            self.selected_month = 12
            self.selected_year -= 1
        else:
            self.selected_month -= 1
        self.update_month_year()
        self.grid_interior()

    def next_month(self, *args):
        if self.selected_month == 12:
            self.selected_month = 1
            self.selected_year += 1
        else:
            self.selected_month += 1
        self.update_month_year()
        self.grid_interior()

    def update_month_year(self):
        mo_from_int = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        self.current_month_year.set(f'{mo_from_int[self.selected_month]} {self.selected_year}')

    def grid_interior(self):
        first_day, days_in_month = calendar.monthrange(self.selected_year, self.selected_month)
        self.build_days(days_in_month)

        self.previous_month_btn._widget.grid(row=1, column=1)
        self.current_month_year._widget.grid(row=1, column=2, columnspan=5)
        self.next_month_btn._widget.grid(row=1, column=7)

        for i, day_of_week in enumerate(('S', 'M', 'T', 'W', 'T', 'F', 'S')):
            lbl = Label(master=self, text=day_of_week)
            lbl._widget.grid(row=2, column=i+1)

        # day_count adjusted so week is Sunday-> Saturday and moves day 1 to correct column
        day_count = -first_day - 1 if first_day != 6 else 0
        for row in range(1, 7):
            for col in range(1, 8):
                try:
                    if day_count >= 0:
                        day_lbl = self.day_labels[day_count]
                        day_lbl._widget.grid(row=row+2, column=col, stick='NSEW')
                except IndexError:
                    pass
                day_count += 1

    def destroy(self):
        for lbl in self.day_labels:
            lbl.destroy()
