import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class GUI(easy_gui.EasyGUI):
    def __init__(self):
        sec = self.add_section('test_section', equal_button_width=True)
        sec.add_widget(type='button', text='Button1', command_func=lambda e: print('Button1 working!'))
        self.test_lbl = sec.add_widget(type='label', text='Here\'s an awesome label!')
        self.test_lbl2 = sec.add_widget(type='label', text='Here\'s an awesome COPYABLE label!', copyable=True)
        sec.add_widget('btn', 'Update Label', command_func=self.update_lbl)

        self.lblentry = sec.add_widget('labelentry', text='LabelEntry')
        sec.add_widget('btn', 'Update LabelEntry', command_func=self.update_lbl2)

    def update_lbl(self, *args):
        self.test_lbl.set(self.test_lbl.get() + 'X')

    def update_lbl2(self, *args):
        self.lblentry.set(self.lblentry.get())


class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = GUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
