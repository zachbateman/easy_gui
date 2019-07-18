'''
Python module that supplies styling used by easy_gui widgets.
'''
from tkinter import font


class BaseStyle():
    '''
    Class with most fundamental level of styling.
    '''
    def __init__(self) -> None:
        self.window_color = '#DEE'
        self.section_color = '#DDE5EE'
        self.menu_color = 'lightgrey'

        # self.font = font.Font(family='Helvetica', size=14, weight='normal')
        self.text_color = '#000'

        self.frame_padx = 5
        self.frame_pady = 5
        self.label_padx = 8
        self.label_pady = 10

        self.widget_bg_color = self.section_color
        self.button_color = '#8AC'
