import unittest
import sys
sys.path.insert(1, '..')
import easy_gui


class GridNoErrors(easy_gui.EasyGUI):
    def __init__(self):
        self.configure_grid(['.  section1', 'section2   .'])

        self.add_section('controls', grid_area='section1')
        self.sections['controls'].configure_grid(['b1', '.', 'b2'])

        self.sections['controls'].add_widget(type='button', text='B1', grid_area='b1', command_func=lambda e: print('Button1 working!'))
        self.sections['controls'].add_widget(type='button', text='B2', grid_area='b2', command_func=lambda e: print('Button2 working!'))

        self.add_section('other_controls', grid_area='section2')
        self.sections['other_controls'].add_widget(type='label', text='Other controls:')
        self.sections['other_controls'].add_widget(type='button', text='Fun', command_func=lambda x: print('Fun'))


class GridWithErrors(easy_gui.EasyGUI):
    def __init__(self):
        self.configure_grid(['.  section1', 'section2   .'])

        self.add_section('controls', grid_area='section1')
        self.sections['controls'].configure_grid(['b1', '.', 'b2', 'l1'])

        # PLACE 'b3' AS GRID AREA IN NEXT LINE TO TRIGGER ERROR HANDLING
        self.sections['controls'].add_widget(type='button', text='B1', grid_area='b3', command_func=lambda e: print('Button1 working!'))
        self.sections['controls'].add_widget(type='button', text='B2', grid_area='b2', command_func=lambda e: print('Button2 working!'))
        self.sections['controls'].add_widget(type='label', text='L1', grid_area='l1')

        self.add_section('other_controls', grid_area='section2')
        self.sections['other_controls'].add_widget(type='label', text='Other controls:')
        self.sections['other_controls'].add_widget(type='button', text='Fun', command_func=lambda x: print('Fun'))


class TestGridWithErrors(unittest.TestCase):
    def test_gui(self):
        gui = GridWithErrors()
        self.assertTrue(True)

class TestGridNoErrors(unittest.TestCase):
    def test_gui(self):
        gui = GridNoErrors()
        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main() #buffer=True)
