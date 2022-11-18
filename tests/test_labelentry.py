import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class GUI(easy_gui.EasyGUI):
    def __init__(self):
        self.width = 500

        e1 = self.add_widget(type='labelentry', text='Entry Spot A')
        e1.set('Hello')
        e2 = self.add_widget(type='labelentry', text='Entry Spot B', align='right', justify='center')
        e2.set('World')

        self.add_widget('lbl', 'align="center"', align='center')
        self.add_widget('lbl', 'align="left"', align='left', relief='sunken')
        self.add_widget('lbl', 'align="right"', align='right')




class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = GUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
