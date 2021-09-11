import unittest
import sys
sys.path.insert(1, '..')
from easy_gui import EasyGUI, styles


EasyGUI.style = styles.DarkStyle()


class TestGUI(EasyGUI):
    def __init__(self):
        self.add_section('test_section')
        self.sections['test_section'].add_widget(type='button', text='Button1', command_func=lambda e: print('Button1 working!'))
        self.sections['test_section'].add_widget(type='label', text='Here\'s an awesome label!')

        self.add_widget('btn', 'Popup Window', command_func=self.new_window)

    def new_window(self, *args):
        with self.popup() as popup:
            popup.add_widget('lbl', 'This is a new window')
            popup.add_widget('btn', 'Popup Button', command_func=lambda _: print('Popup Button'))



class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = TestGUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
