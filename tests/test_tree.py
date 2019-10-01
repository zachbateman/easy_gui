import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class TestGUI(easy_gui.EasyGUI):
    def __init__(self):
        super().__init__()





class TestEasyGUI(unittest.TestCase):

    def setUp(self):
        self.gui = TestGUI()


    def test_gui_creation(self):
        self.gui.add_section('test_section')
        self.gui.sections['test_section'].add_widget(type='button', text='Button1', command_func=lambda e: print('Button1 working!'))
        self.gui.sections['test_section'].add_widget(type='label', text='Here\'s an awesome label!')

        tree_section = self.gui.add_section('tree_section', title=True, return_section=True)
        tree = tree_section.add_widget(type='tree', return_widget=True)

        tree.insert_column('TestCol1')
        tree.insert_column('TestCol2')
        tree.insert_column('TestCol3')

        node1 = tree.insert_row('Node #1', ('test', 'test2', 'test3'), return_row=True, open=True)
        tree.insert_row('Node #2', ('', 'Xxxx'))
        tree.insert_row('Item A', ('test2', 'dude'), parent_row=node1)


        self.gui.mainloop()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
