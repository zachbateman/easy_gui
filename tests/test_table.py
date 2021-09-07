import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class TestGUI(easy_gui.EasyGUI):
    def __init__(self):
        self.geometry('550x500')

        sec = self.add_section('test_section')
        sec.add_widget(type='label', text='Testing a Table Widget!')

        self.table = sec.add_widget('table')
        self.table[2, 3] = '-TEST-'
        
        sec.add_widget('btn', text='Print cell row=2, column=3', command_func=self.print_cell)
        
    def print_cell(self, *args):
        print(self.table[2, 3])
        self.table[3, 3] = self.table[2, 3] + '2'



class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = TestGUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
