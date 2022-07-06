import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class TestGUI(easy_gui.EasyGUI):
    def __init__(self):
        # self.geometry('550x500')
        self.width = 550
        self.height = 500
        self.center = True

        sec = self.add_section('test_section')
        sec.add_widget(type='label', text='Testing a Table Widget!')

        self.table = sec.add_widget('table')
        self.table[2, 3] = '-TEST-'

        sec.add_widget('btn', text='Print cell row=2, column=3', command_func=self.print_cell)
        sec.add_widget('canvasbutton', text='Change table[1, 1]', command_func=self.change_cell, width=150)

    def print_cell(self, *args):
        print(self.table[2, 3])
        self.table[3, 3] = self.table[2, 3] + '2'

    def change_cell(self, *args):
        self.table[1, 1] = '/' + self.table[1, 1] + '/'



class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = TestGUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
