import unittest
import sys
sys.path.insert(1, '..')
import easy_gui

data = [(1, 1), (2, 3), (3, 5), (4, 4), (5, 7), (6, 7)]


class TestPlotterGUI(unittest.TestCase):

    def setUp(self):
        self.gui = easy_gui.EasyGUI()


    def test_gui(self):
        self.gui.add_section('controls')
        self.gui.sections['controls'].add_widget(type='button', text='Scatter Plot', command_func=lambda e: print('Button1 working!'))
        self.gui.sections['controls'].add_widget(type='button', text='Line Plot', command_func=lambda e: print('Button1 working!'))

        self.gui.add_section('display')
        self.gui.sections['display'].add_widget(type='matplotlib')

        self.gui.mainloop()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
