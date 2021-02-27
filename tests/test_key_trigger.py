import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class GUI(easy_gui.EasyGUI):
    def __init__(self):
        self.add_widget(type='button', text='Button1', command_func=lambda e: print('Button1 working!'))
        self.test_lbl = self.add_widget(type='label', text='Here\'s an awesome label!')
        self.add_widget('btn', 'Update Label', command_func=self.update_lbl)
        self.add_key_trigger('clear', lambda: self.test_lbl.set('Clear'))

    def update_lbl(self, *args):
        self.test_lbl.set(self.test_lbl.get() + 'X')


class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        GUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
