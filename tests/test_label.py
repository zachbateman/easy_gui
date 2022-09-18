import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class GUI(easy_gui.EasyGUI):
    def __init__(self):
        self.width = 500

        self.add_widget(type='label', text='Here\'s an awesome label!')
        self.add_widget(type='label', text='Here\'s an awesome COPYABLE label!', copyable=True)
        self.add_widget(type='label', text='Here\'s an awesome COPYABLE label with align="left"', copyable=True, align='left')

        self.add_widget('lbl', 'align="center"', align='center')
        self.add_widget('lbl', 'align="left"', align='left', relief='sunken')
        self.add_widget('lbl', 'align="right"', align='right')




class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = GUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
