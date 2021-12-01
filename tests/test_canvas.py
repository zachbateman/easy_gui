import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class GUI(easy_gui.EasyGUI):
    def __init__(self):
        self.geometry('400x340')
        sec = self.add_section('test_section', equal_button_width=True)
        sec.add_widget(type='button', text='Button1', command_func=lambda e: print('Button1 working!'))
        self.test_lbl = sec.add_widget(type='label', text='Here\'s an awesome label!')
        canvas = sec.add_widget('canvas')
        canvas.create_line(20, 20, 50, 100)


class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = GUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
