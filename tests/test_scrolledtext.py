import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class TestGUI(easy_gui.EasyGUI):
    def __init__(self):
        self.geometry('800x500')
        section = self.add_section('test_section')
        scrldtext = section.add_widget(type='scrolledtext')
        section.add_widget(type='button', text='Print Text', command_func=lambda e: print(scrldtext.get()))



class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = TestGUI()
        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main() #buffer=True)
