import unittest
import sys
sys.path.insert(1, '..')
import easy_gui
from easy_gui import Section

data = [(1, 1), (2, 3), (3, 5), (4, 4), (5, 7), (6, 7)]


class RightSide1(Section):
    # def __init__(self, *args, **kwargs):
    def __init__(self):
        self.configure_grid(['lbl_a   lbl_b',
                                        'lbl_c     .    '])
        self.add_widget('lbl', 'Right Side1', grid_area='lbl_a')
        self.add_widget('lbl', 'Label 2', grid_area='lbl_b')
        self.add_widget('lbl', 'Label C', grid_area='lbl_c')


class RightSide2(Section):
    def __init__(self):
        self.configure_grid(['lbl_a   lbl_b'])
        self.add_widget('lbl', 'Right Side2', grid_area='lbl_a')
        self.add_widget('lbl', 'Label 2', grid_area='lbl_b')





if __name__ == '__main__':
    print('Module only to be imported in test_multiple_modules_1')
