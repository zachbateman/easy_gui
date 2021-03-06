'''
Python module containing "Master" classes of easy_gui project.
The classes in here are designed to be subclassed in user applications.
'''
import tkinter as tk
import tkinter.scrolledtext
from tkinter import ttk
from tkinter import _tkinter
from .styles import BaseStyle
from . import widgets
import os
import sys
from typing import List, Dict




class GridMaster():
    def __init__(self):
        self.grid_areas = {}
        self.grid_configuration = []

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
                if name in row.split():
                    if first_row is None:
                        first_row = i  # will stay fixed at the first row containing name
                    last_row = i  # will continue to increase for multiple rows
                    if first_column is None:
                        row_list = row.split()
                        first_column = row_list.index(name)  # get far left column of name
                        last_column = len(row_list) - row_list[::-1].index(name) - 1  # reverse to get far right column

            self.grid_areas[name] = {'first_row': first_row, 'last_row': last_row,
                                'first_column': first_column, 'last_column': last_column}

        # Now make elements expand evenly with window resize by default
        if self.grid_areas != {}:
            limits = self.grid_limits()
            for row in range(limits['min_row'], limits['max_row'] + 1):
                self.grid_rowconfigure(row, weight=1)
            for col in range(limits['min_col'], limits['max_col'] + 1):
                self.grid_columnconfigure(col, weight=1)

    def add_grid_row(self, row_name: str):
        if self.grid_configuration == []:
            self.grid_configuration = [row_name]
        else:
            num_columns = len(self.grid_configuration[0].split(' '))
            self.grid_configuration.append(' '.join([row_name] * num_columns))
        self.configure_grid(self.grid_configuration)

    def grid_limits(self) -> dict:
        min_row, max_row, min_col, max_col = 500, -500, 500, -500  # arbitrarly large starting points so no risk of surpising row/col not being captured
        for area in self.grid_areas.values():
            if area['first_row'] < min_row:
                min_row = area['first_row']
            if area['last_row'] > max_row:
                max_row = area['last_row']
            if area['first_column'] < min_col:
                min_col = area['first_column']
            if area['last_column'] > max_col:
                max_col = area['last_column']
        return {'min_row': min_row, 'max_row': max_row, 'min_col': min_col, 'max_col': max_col}




class SectionMaster():
    def __init__(self):
        self.sections: dict = {}

    def add_section(self, name='', title=False, grid_area=None,
                               borderwidth=None, relief=None, tabbed: bool=False):
        '''
        Add a Section object to the parent (root window or other Section).
        '''
        if name == '':
            name = f'section{len(self.sections) + 1}'
        if name in self.sections:
            raise ValueError('Unable to add section as a section with the given name already exists!')

        if borderwidth is None:
            borderwidth = self.style.borderwidth
        if relief is None:
            relief = self.style.section_border

        # Next 2 lines set grid_area to be name if not explicitly declared and not already used as a grid_area
        if grid_area is None and name not in [s.grid_area for s in self.sections.values()]:
            grid_area = name

        section = Section(parent=self, name=name, title=title, grid_area=grid_area,
                                    borderwidth=borderwidth, relief=relief, tabbed=tabbed)
        self.sections[name] = section
        return section

    def add_tab(self, name=''):
        if not self.tabbed:
            print('Error!  Cannot .add_tab to a Section unless tabbed=True when it is created.')
            return
        section = Section(parent=self.tabs, name=name)
        self.sections[name] = section
        self.tabs.add(section, text=name)
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




class EasyGUI(tk.Tk, GridMaster, SectionMaster):
    '''
    Main class to be subclassed for full GUI window.
    '''
    style = BaseStyle()

    def __init__(self) -> None:
        super().__init__()
        GridMaster.__init__(self)
        SectionMaster.__init__(self)
        EasyGUI.style.create_font()  # have to generate font.Font object after initial tk root window is created

        self.icon(bitmap=os.path.join(os.path.dirname(__file__), 'resources', 'transparent.ico'), default=True)
        self.title('EasyGUI')
        self.geometry("200x100")
        self.configure(background=self.style.window_color)

    def __init_subclass__(cls, **kwargs):
        '''
        Wraps user subclass __init__ to implicitly handle the EasyGUI.__init__ call along with
        calling .create_gui() after application is fully defined in subclass __init__ method
        '''
        old_init = cls.__init__  # reference to original subclass method so new_init isn't recursive
        def new_init(self, *args, **kwargs):
            EasyGUI.__init__(self)  # in place of super().__init__() in subclass __init__
            old_init(self, *args, **kwargs)
            self.create()  # populates GUI elements
            self.mainloop()  # runs tkinter mainloop
        cls.__init__ = new_init  # overwrite subclass __init__ method

    def icon(self, bitmap, default: bool=False) -> None:
        '''
        Alternate method to call tk.Tk iconbitmap method using altered path handling
        so that PyInstaller can package application with specified .ico file.
        If not default, warning message is printed on failing to locate .ico file.
        '''
        try:
            super().iconbitmap(bitmap=resource_path(bitmap))
        except _tkinter.TclError:
            if default:
                pass  # Pass silently if default .ico not found occurs when using PyInstaller and not adding transparent.ico to "datas"
            else:
                print(f'Cannot locate {bitmap}!  If using PyInstaller, be sure to specify this file in "datas".')

    def create(self, force_row=False) -> None:
        '''
        Positions GUI elements in window.
        May be called recursively by child Sections as elements are positioned.
        '''
        for name, section in self.sections.items():
            section.create(force_row=force_row)

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



class Section(tk.Frame, GridMaster, SectionMaster):
    '''
    A Section is a tk.Frame used for storing and managing widgets.
    Sections exist as children of the root (EasyGUI) window or other Sections.
    '''
    def __init__(self, parent=None, name='', title=False, grid_area=None, tabbed: bool=False, **kwargs) -> None:
        borderwidth = kwargs.get('borderwidth', 1)
        relief = kwargs.get('relief', 'ridge')
        self.tabbed = tabbed
        super().__init__(master=parent,
                         bg=EasyGUI.style.section_color,
                         padx=EasyGUI.style.frame_padx,
                         pady=EasyGUI.style.frame_pady,
                         borderwidth=borderwidth,
                         relief=relief)
        GridMaster.__init__(self)
        SectionMaster.__init__(self)
        self.parent = parent
        self.name = name
        self.grid_area = grid_area
        if tabbed:
            self.tabs = ttk.Notebook(self)
            self.tabs.style = self.style
        self.widgets: dict = {}
        if title:  # title kwargs can be provided as True or a string
            if isinstance(title, str):  # if string, use title for label text
                self.add_widget(type='label', text=title)
            elif title == True:  # if True, use the name as the label text
                self.add_widget(type='label', text=name)

    @property
    def style(self):
        '''Goes upsteam to evenually reference EasyGUI.style'''
        return self.parent.style

    def create(self, force_row: bool=False):
        '''
        Positions this section within the parent along with
        positioning all children (Sections and/or Widgets).
        '''
        self.position(force_row)
        for child in {**self.widgets, **self.sections}.values():
            try:
                child.create(force_row)  # if child is another Section object
            except AttributeError:
                child.position(force_row)  # if child is a Widget object

    def position(self, force_row: bool=False) -> None:
        '''
        Physically position this Section within its parent container.
        '''
        try:
            if hasattr(self.parent, 'grid_areas'):
                if self.parent.grid_areas != {} and self.grid_area and not force_row:
                    try:
                        if not hasattr(self.parent, 'tabbed') or not self.parent.tabbed:
                            bounds = self.parent.grid_areas[self.grid_area]
                            self.grid(row=bounds['first_row'], column=bounds['first_column'], rowspan=bounds['last_row']-bounds['first_row']+1, columnspan=bounds['last_column']-bounds['first_column']+1, sticky='NSEW')
                        else:
                            self.pack()
                        if self.tabbed:
                            self.tabs.pack()
                        return  # early return if everything works fine with initial attempt (no other actions needed)
                    except KeyError:
                        if self.grid_area != self.name:  # basically, if user-specified grid_area (are same if programatically set grid_area)
                            print(f'"{self.grid_area}" not found in parent\'s grid areas.\nResorting to a new row.')
                self.parent.add_grid_row(self.name)
                self.grid_area = self.name
                self.parent.create()
        except _tkinter.TclError:
            print(f'\n--- GRID FAILED for Section: "{self.name}" ---\nTry ensuring "grid_area" arg is given for all Sections in a given parent.\nAdding to a new row instead.')
            self.parent.create(force_row=True)  # go back and fully recreate section forcing all children to be packed/in new rows

    def add_widget(self, type='label', text='', widget_name=None, grid_area=None, **kwargs):
        '''
        Add a Widget object to this Section by calling the add_widget function in widgets.py
        (Easier to keep the function there as it needs access to all the individual Widget classes.)
        '''
        return widgets.add_widget(self, type=type, text=text, widget_name=widget_name, grid_area=grid_area, **kwargs)

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

    def _clear_and_recreate_plot(self, mpl_figure, widget_name, grid_area, kwargs):
        self.delete_widget(widget_name)
        new_widget = self.add_widget(type='matplotlib', widget_name=widget_name, grid_area=grid_area)
        new_widget.draw_plot(mpl_figure=mpl_figure)
        new_widget.position()  # have to reposition/create Widget

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





def resource_path(relative_path):
    '''Get absolute path to resource to allow PyInstaller bundling.'''
    try:
        base_path = sys._MEIPASS  # PyInstaller-created temporary folder
    except:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)
