import unittest
import sys
sys.path.insert(1, '..')
import easy_gui


class TestGridWithErrors(unittest.TestCase):

    def setUp(self):
        self.gui = easy_gui.EasyGUI()

    def test_gui(self):
        self.gui.configure_grid(['.  section1', 'section2   .'])

        self.gui.add_section('controls', grid_area='section1')
        self.gui.sections['controls'].configure_grid(['b1', '.', 'b2', 'l1'])

        # PLACE 'b3' AS GRID AREA IN NEXT LINE TO TRIGGER ERROR HANDLING
        self.gui.sections['controls'].add_widget(type='button', text='B1', grid_area='b3', command_func=lambda e: print('Button1 working!'))
        self.gui.sections['controls'].add_widget(type='button', text='B2', grid_area='b2', command_func=lambda e: print('Button2 working!'))
        self.gui.sections['controls'].add_widget(type='label', text='L1', grid_area='l1')

        self.gui.add_section('other_controls', grid_area='section2')
        self.gui.sections['other_controls'].add_widget(type='label', text='Other controls:')
        self.gui.sections['other_controls'].add_widget(type='button', text='Fun', command_func=lambda x: print('Fun'))

        self.gui.create_gui()
        self.assertTrue(True)

class TestGridNoErrors(unittest.TestCase):

    def setUp(self):
        self.gui = easy_gui.EasyGUI()

    def test_gui(self):
        self.gui.configure_grid(['.  section1', 'section2   .'])

        self.gui.add_section('controls', grid_area='section1')
        self.gui.sections['controls'].configure_grid(['b1', '.', 'b2'])

        self.gui.sections['controls'].add_widget(type='button', text='B1', grid_area='b1', command_func=lambda e: print('Button1 working!'))
        self.gui.sections['controls'].add_widget(type='button', text='B2', grid_area='b2', command_func=lambda e: print('Button2 working!'))

        self.gui.add_section('other_controls', grid_area='section2')
        self.gui.sections['other_controls'].add_widget(type='label', text='Other controls:')
        self.gui.sections['other_controls'].add_widget(type='button', text='Fun', command_func=lambda x: print('Fun'))

        self.gui.create_gui()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main() #buffer=True)
