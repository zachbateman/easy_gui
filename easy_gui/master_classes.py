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
from typing import List, Dict

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class GridMaster():
    def __init__(self):
        self.grid_areas = {}

    def configure_grid(self, grid_configuration: List[str]) -> Dict[str, int]:
        '''
        Specify full-window layout with CSS grid-template-area style list of strings.
        - Each item in provided grid_configuration corresponds to a grid row and spaces
        delimit each cell.
        - Individual cells or rectangular groups of contiguous cells may be indicated by name
        while unnamed cells are specified by one or more periods.
        '''
        self.grid_configuration = grid_configuration
        self.grid_rows = len(grid_configuration)
        self.grid_columns = len(grid_configuration[0].split())
        for row in grid_configuration:
            if len(grid_configuration[0].split()) != self.grid_columns:
                print('ERROR!  Differing number of grid columns specified below:')
                print(grid_configuration)
                return

        names = set(cell for row in grid_configuration for cell in row.split() if '.' not in cell)
        for name in names:
            first_row, last_row, first_column, last_column = None, None, None, None
            for i, row in enumerate(grid_configuration):
                if name in row:
                    if first_row is None:
                        first_row = i  # will stay fixed at the first row containing name
                    last_row = i  # will continue to increase for multiple rows
                    if first_column is None:
                        row_list = row.split()
                        first_column = row_list.index(name)  # get far left column of name
                        last_column = len(row_list) - row_list[::-1].index(name) - 1  # reverse to get far right column

            self.grid_areas[name] = {'first_row': first_row, 'last_row': last_row,
                                'first_column': first_column, 'last_column': last_column}



class EasyGUI(tk.Tk, GridMaster):
    '''
    Main class to be subclassed for full GUI window.
    '''
    style = BaseStyle()

    def __init__(self) -> None:
        super().__init__()
        GridMaster.__init__(self)
        EasyGUI.style.create_font()  # have to generate font.Font object after initial tk root window is created

        self.iconbitmap(bitmap=os.path.join(os.path.dirname(__file__), 'resources', 'transparent.ico'))
        self.title('EasyGUI')
        self.geometry("800x600")
        self.configure(background=self.style.window_color)

        self.sections: dict = {}


    def create_gui(self) -> None:
        '''
        Positions GUI elements in window and starts tkinter main loop.
        CALL THIS at the end of creating the GUI to make it run.
        '''
        for name, section in self.sections.items():
            section.create_section()
        self.mainloop()


    def add_section(self, name='', title=False, return_section=False, grid_area=None) -> None:
        '''
        Add a Section object to the root window.
        '''
        if name == '':
            name = f'section{len(self.sections) + 1}'
        if name in self.sections:
            raise ValueError('Unable to add section as a section with the given name already exists!')
        section = Section(parent=self, name=name, title=title, grid_area=grid_area)
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

    def mouse_scroll(self, event) -> None:
        # TODO
        pass



class Section(tk.Frame, GridMaster):
    '''
    A Section is a tk.Frame used for storing and managing widgets.
    '''
    def __init__(self, parent=None, name='', title=False, grid_area=None) -> None:
        super().__init__(borderwidth=1,
                         bg=EasyGUI.style.section_color,
                         padx=EasyGUI.style.frame_padx,
                         pady=EasyGUI.style.frame_pady,
                         relief='ridge')
        GridMaster.__init__(self)
        self.parent = parent
        self.name = name
        self.grid_area = grid_area
        self.widgets: dict = {}
        if title:  # title kwargs can be provided as True or a string
            if isinstance(title, str):  # if string, use title for label text
                self.add_widget(type='label', text=title)
            elif title == True:  # if True, use the name as the label text
                self.add_widget(type='label', text=name)

    def create_section(self):
        '''
        Positions this section within the parent along with
        positioning all children (Sections and/or Widgets).
        '''
        self.position()
        for name, child in self.widgets.items():
            try:
                child.create_section()  # if child is another Section object
            except AttributeError:
                child.position()  # if child is a Widget object

    def position(self) -> None:
        '''
        Physically position this Section within its parent container.
        '''
        if self.grid_area:
            bounds = self.parent.grid_areas[self.grid_area]
            self.grid(row=bounds['first_row'], column=bounds['first_column'], rowspan=bounds['last_row']-bounds['first_row']+1, columnspan=bounds['last_column']-bounds['first_column']+1)
        else:
            self.pack()

    def add_widget(self, type='label', text='', widget_name=None, grid_area=None, return_widget=False, **kwargs):
        '''
        Add a Widget object to this section
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
        elif type.lower() == 'dropdown':
            new_widget = DropDown(master=self, grid_area=grid_area, **kwargs)
            self.widgets[new_widget_name('dropdown')] = new_widget
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

    @property
    def width(self) -> float:
        '''
        Estimate and return width desired by this Section.
        '''
        return float(max(widget.width for widget in self.widgets.values()))

    @property
    def height(self) -> float:
        '''
        Estimate and return height desired by this Section.
        '''
        return float(sum(widget.height for widget in self.widgets.values()))




class Widget(tk.Frame):
    '''
    To be subclassed into specific EasyGUI widgets.
    Class assumes the "_widget" attribute is the actual tkinter widget (if used)
    '''
    def __init__(self, master=None, bg=None, grid_area=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.parent = master  # master attr used in tkinter; parent attr used in this code
        self.grid_area = grid_area
        self.configure(background=EasyGUI.style.widget_bg_color)


    def position(self) -> None:
        '''
        Physically position this Widget within its parent Section.
        '''
        if self.grid_area:
            try:
                bounds = self.parent.grid_areas[self.grid_area]
                self.grid(row=bounds['first_row'], column=bounds['first_column'], rowspan=bounds['last_row']-bounds['first_row']+1, columnspan=bounds['last_column']-bounds['first_column']+1)
            except KeyError:
                print(f'{self.grid_area} not found in parent\'s grid areas.\nResorting to pack.')
                self._widget.pack()
        else:
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




class Button(Widget):
    def __init__(self, master=None, text='button', command_func=lambda x: None, separate_thread=False, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        # self.parent = master
        self.text = text
        del kwargs['grid_area']
        self._widget = tk.Button(master=master, text=text, highlightbackground=EasyGUI.style.button_color, font=EasyGUI.style.font, **kwargs)
        self.bind_click(command_func, separate_thread)

    def place(self) -> None:
        '''
        Override Widget method for proper padding on outside!
        (have to supply padx and pady on pack call for button
        '''
        self._widget.pack(padx=EasyGUI.style.button_padx, pady=EasyGUI.style.button_pady)

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
        super().__init__()
        self.text = text
        self._widget = tk.Label(master=master, text=text, bg=EasyGUI.style.widget_bg_color, fg=EasyGUI.style.text_color,
                                padx=EasyGUI.style.label_padx, pady=EasyGUI.style.label_pady, font=EasyGUI.style.font, **kwargs)

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

        current_row_iid_index = [index for index, iid in enumerate(iids) if iid == current_row][0]

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
