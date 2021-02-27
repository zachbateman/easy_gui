'''
Python module that supplies styling used by easy_gui widgets.
'''
from tkinter import font


class BaseStyle():
    '''
    Style class with most fundamental level of styling.
    '''
    def __init__(self) -> None:
        self.transparent = False
        self.window_color = '#DDE5EE'
        self.section_color = '#DDE5EE'
        self.menu_color = 'lightgrey'

        # _font attr provides parameters used to modify Font generated and used (don't have to provide all - leave out for defaults)
        self._font = {'size': 10, 'weight': 'normal'}
        # self._font = {'family': 'Helvetica', 'size': 10, 'weight': 'normal'}

        self.text_color = '#111'

        self.borderwidth = 1
        self.section_border = 'flat'  # can also be one of 'sunken', 'raised', 'groove', or 'ridge'

        self.frame_padx = 2
        self.frame_pady = 2
        self.label_padx = 4
        self.label_pady = 2
        self.button_padx = 4
        self.button_pady = 2

        self.widget_bg_color = self.section_color
        self.button_color = '#8AC'

    def create_font(self):
        '''
        Create self.font attribute as a tkinter font.Font object.
        A font.Font object CAN ONLY BE CREATED AFTER CREATING A ROOT WINDOW...
        ...hence, this method is called in the EasyGUI class to transform the specified
        "_font" dict attribute into a font.Font "font" attribute.
        '''
        if hasattr(self, '_font'):
            self.font = font.Font(**self._font)
        else:
            self.font = None  # passing None to widget creation will use default Tkinter Fonts



class DarkStyle(BaseStyle):
    '''
    Style with a dark theme.

    Inherits from BaseStyle and overwrites settings where appropriate.
    '''
    def __init__(self) -> None:
        super().__init__()

        self.window_color = '#555'
        self.section_color = '#555'
        self.text_color = '#FFF'
        self.widget_bg_color = self.section_color


class TransparentStyle(BaseStyle):
    '''
    Style with a transparent window.
    '''
    def __init__(self) -> None:
        super().__init__()
        self.transparent = True
        self.window_color = 'white'
        self.section_color = 'white'
