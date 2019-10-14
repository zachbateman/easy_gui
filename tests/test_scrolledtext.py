import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class TestGUI(easy_gui.EasyGUI):
    def __init__(self):
        super().__init__()





class TestEasyGUI(unittest.TestCase):

    def setUp(self):
        self.gui = TestGUI()


    def test_gui_creation(self):
        section = self.gui.add_section('test_section', return_section=True)

        scrldtext = section.add_widget(type='scrolledtext', return_widget=True)

        section.add_widget(type='button', text='Print Text', command_func=lambda e: print(scrldtext.get()))

        self.gui.mainloop()
        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main() #buffer=True)
