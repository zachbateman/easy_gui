import unittest
import sys
sys.path.insert(1, '..')
import easy_gui

easy_gui.EasyGUI.style.section_border='raised'

class GUI(easy_gui.EasyGUI):
    def __init__(self):
        self.configure_grid(['column1  column2'])

        col1 = self.add_section('column1', grid_area='column1')
        col2 = self.add_section('column2')  # IMPLICITLY set grid_area!

        top_left = col1.add_section('topleft')
        top_left.add_widget('lbl', 'Top Left')
        bot_left = col1.add_section('bot_left')
        bot_left.add_widget('lbl', 'Bottom Left')

        col2.configure_grid(['top', 'bottom'])
        top_right = col2.add_section('top')  # IMPLICITLY set grid_area!
        top_right.add_widget('lbl', 'Top Right')
        top_right.add_widget('lbl', 'Top Right 2')
        col2.add_widget('lbl', 'Bottom Right', grid_area='bottom')


class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = GUI()
        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()  # buffer=True)
