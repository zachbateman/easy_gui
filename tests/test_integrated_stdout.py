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
        self.gui.add_section('test_section')
        self.gui.sections['test_section'].add_widget(type='button', text='Button1', command_func=lambda e: print('Button1 working!'))
        self.gui.sections['test_section'].add_widget(type='label', text='Here\'s an awesome label!')
        
        self.gui.add_section('output_section')
        self.gui.sections['output_section'].add_widget(type='stdout')
        
        self.gui.mainloop()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main()
