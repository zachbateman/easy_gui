import unittest
import sys
sys.path.insert(1, '..')
import easy_gui
import time



class GUI(easy_gui.EasyGUI):
    def __init__(self):
        sec = self.add_section('test_section', equal_button_width=True)
        sec.add_widget(type='button', text='Button1', command_func=lambda e: print('Button1 working!'))
        self.test_lbl = sec.add_widget(type='label', text='Here\'s an awesome label!')
        sec.add_widget('btn', 'Update Label', command_func=self.update_lbl)

        self.lblentry = sec.add_widget('labelentry', text='LabelEntry')
        sec.add_widget('btn', 'Update LabelEntry', command_func=self.update_lbl2)

        self.add_widget('btn', 'Add new Stuff!', command_func=self.add_label)

    def update_lbl(self, *args):
        self.test_lbl.set(self.test_lbl.get() + 'X')

    def update_lbl2(self, *args):
        self.lblentry.set(self.lblentry.get())

    def add_label(self, *args):
        self.add_widget('lbl', 'New Label!')
        new = self.add_section()
        new.configure_grid(['1  2',
                                   '3   4'])
        new.add_widget('lbl', 'Label 1', grid_area='1')
        new.add_widget('lbl', 'Label 2', grid_area='2')
        new.add_widget('lbl', 'Label 3', grid_area='3')
        new.add_widget('lbl', 'Label 4', grid_area='4')



class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = GUI()




if __name__ == '__main__':
    unittest.main() #buffer=True)
