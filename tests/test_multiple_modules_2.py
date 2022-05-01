import unittest
import sys
sys.path.insert(1, '..')
import easy_gui
from easy_gui import Section

data = [(1, 1), (2, 3), (3, 5), (4, 4), (5, 7), (6, 7)]


class RightSide(Section):
    def __init__(self, *args, **kwargs):
        self.add_widget('lbl', 'Right Side')
        self.add_widget('lbl', 'Right Label 2')





if __name__ == '__main__':
    print('Module only to be imported in test_multiple_modules_1')
