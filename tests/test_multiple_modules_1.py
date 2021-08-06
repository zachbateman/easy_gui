import unittest
import sys
sys.path.insert(1, '..')
import easy_gui
from easy_gui import Section
from test_multiple_modules_2 import RightSide


class MultipleModuleGUI(easy_gui.EasyGUI):
    def __init__(self):
        self.geometry('900x700')

        self.configure_grid(['left_side   right_side'])

        left_side = self.add_section('left_side', grid_area='left_side')
        left_side.add_widget('lbl', 'Left Side')
        left_side.add_widget('lbl', 'Label 1')
        left_side.add_widget('lbl', 'Label 2')
        self.count = 0
        self.update_label = left_side.add_widget('lbl', 'Update Label: ' + str(self.count))
        self.update = left_side.add_widget('btn', 'Update Label', command_func=self.update)
       
        right_side = self.add_section(external_section=RightSide, grid_area='right_side', relief='sunken')


    def update(self, *args):
        self.count += 1
        self.update_label.set('Update Label: ' + str(self.count))



class TestPlotterGUI(unittest.TestCase):
    def test_gui(self):
        gui = MultipleModuleGUI()
        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main() #buffer=True)
