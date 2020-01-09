import unittest
import sys
sys.path.insert(1, '..')
import easy_gui


class TestPlotterGUI(unittest.TestCase):

    def setUp(self):
        self.gui = easy_gui.EasyGUI()


    def test_gui(self):
        # print(self.gui.grid_areas)
        # self.gui.configure_grid(['.  section1', 'section2   .'])
        # print(self.gui.grid_areas)
        
        
        self.gui.add_section('controls') #, grid_area='section1')
        print(self.gui.sections['controls'].grid_areas)
        # breakpoint()
        self.gui.sections['controls'].configure_grid(['b1', '.', 'b2'])
        print(self.gui.sections['controls'].grid_areas)
        
        
        
        # self.gui.sections['controls'].add_widget(type='button', text='B1', grid_area='b1', command_func=lambda e: print('Button1 working!'))
        # self.gui.sections['controls'].add_widget(type='button', text='B2', grid_area='b2', command_func=lambda e: print('Button2 working!'))


        # self.gui.add_section('other_controls', grid_area='section2')
        # self.gui.sections['other_controls'].add_widget(type='label', text='Other controls:')

        # self.gui.sections['other_controls'].add_widget(type='button', text='Fun', command_func=lambda x: print('Fun'))

        self.gui.create_gui()
        self.assertTrue(True)
        
class Test():

    def __init__(self):
        self.gui = easy_gui.EasyGUI()


    def test_gui(self):
        # print(self.gui.grid_areas)
        # self.gui.configure_grid(['.  section1', 'section2   .'])
        # print(self.gui.grid_areas)
        
        
        self.gui.add_section('controls') #, grid_area='section1')
        print(self.gui.sections['controls'].grid_areas)
        # breakpoint()
        self.gui.sections['controls'].configure_grid(['b1', '.', 'b2'])
        print(self.gui.sections['controls'].grid_areas)
        
        
        
        # self.gui.sections['controls'].add_widget(type='button', text='B1', grid_area='b1', command_func=lambda e: print('Button1 working!'))
        # self.gui.sections['controls'].add_widget(type='button', text='B2', grid_area='b2', command_func=lambda e: print('Button2 working!'))


        # self.gui.add_section('other_controls', grid_area='section2')
        # self.gui.sections['other_controls'].add_widget(type='label', text='Other controls:')

        # self.gui.sections['other_controls'].add_widget(type='button', text='Fun', command_func=lambda x: print('Fun'))

        self.gui.create_gui()
        # self.assertTrue(True)


if __name__ == '__main__':
    # unittest.main() #buffer=True)
    test = Test()
    test.test_gui()
