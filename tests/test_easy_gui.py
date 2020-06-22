import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class GUI(easy_gui.EasyGUI):
    def __init__(self):
        self.add_section('test_section')
        self.sections['test_section'].add_widget(type='button', text='Button1', command_func=lambda e: print('Button1 working!'))
        self.test_lbl = self.sections['test_section'].add_widget(type='label', text='Here\'s an awesome label!')
        self.sections['test_section'].add_widget('btn', 'Update Label', command_func=self.update_lbl)

    def update_lbl(self, *args):
        self.test_lbl.set(self.test_lbl.get() + 'X')


class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = GUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
