import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class GUI(easy_gui.EasyGUI):
    def __init__(self):
        sec = self.add_section('test_section', equal_button_width=True)
        btn1 = sec.add_widget(type='button', text='Button1', command_func=lambda e: print('Button1 working!'))
        btn1.add_tooltip('Here is a reeeeaaaalllyyyyyyy LONGGGGGG tooltip.  The text just keeps on going!!!  And GOIINNNGGG!!!!!', delay=2)
        
        self.test_lbl = sec.add_widget(type='label', text='Here\'s an awesome label!')
        self.test_lbl.add_tooltip('This is a standard label')
        
        btn2 = sec.add_widget('btn', 'Update Label', command_func=self.update_lbl)
        btn2.add_tooltip('This button will update the above Label text.')


    def update_lbl(self, *args):
        self.test_lbl.set(self.test_lbl.get() + 'X')



class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = GUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
