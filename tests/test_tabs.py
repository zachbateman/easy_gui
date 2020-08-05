import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class TestGUI(easy_gui.EasyGUI):
    def __init__(self):
        self.geometry('500x400')
        test = self.add_section('test_section')

        test.add_widget(type='button', text='Button1', command_func=lambda e: print('Button1 working!'))
        test.add_widget(type='label', text='Here\'s an awesome label!')


        tabs = test.add_section('tab_section', tabbed=True)

        tab1 = tabs.add_tab('Tab1')  # returns a new Section
        lbl1 = tab1.add_widget('lbl', 'TEST tab1 Label!')
        btnt1 = tab1.add_widget('btn', 'BtnT1', command_func=lambda x: print('Tab 1 Button'))

        tab2 = tabs.add_tab('Tab2')
        lbl2 = tab2.add_widget('lbl', 'tab2 Label Yo')

        tabs.add_tab('TAB-3')


        self.add_section('output_section')
        self.sections['output_section'].add_widget(type='stdout', height=20, width=40)



class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = TestGUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main()
