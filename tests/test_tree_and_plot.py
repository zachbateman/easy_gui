import unittest
import sys
sys.path.insert(1, '..')
import easy_gui
from matplotlib.figure import Figure



class TestGUI(easy_gui.EasyGUI):
    def __init__(self):
        self.geometry('500x500')

        self.add_section('test_section')
        self.sections['test_section'].add_widget(type='button', text='Button1', command_func=lambda e: print('Button1 working!'))
        self.sections['test_section'].add_widget(type='label', text='Here\'s an awesome label!')

        tree_section = self.add_section('tree_section', title=True)
        tree = tree_section.add_widget(type='tree')
        self.tree = tree
        self.tree.bind_select(self.plot_current)

        tree.insert_column('TestCol1')
        tree.insert_column('TestCol2')
        tree.insert_column('TestCol3')

        node1 = tree.insert_row('Node #1', ('test', 'test2', 'test3'), open=True)
        node2 = tree.insert_row('Node #2', ('', 'Xxxx'))
        tree.insert_row('Item A', ('test2', 'dude'), parent_row=node1)
        tree.insert_row('Item B', ('...', '...'), parent_row=node1)
        tree.insert_row('Item C', ('...', '...'), parent_row=node2)

        self.plot_section = self.add_section('plot')
        self.plot = self.plot_section.add_widget(type='matplotlib')


    def plot_current(self, *args):
        x = list(range(1, 11))
        y = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        if self.tree.current_row['text'] == 'Item A':
            y = [5, 5, 5, 5, 5] + y[5:]
        elif self.tree.current_row['text'] == 'Item B':
            y = y[:5] + [14, 14, 14, 14, 14]

        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.scatter(x, y)

        self.plot.draw_plot(mpl_figure=fig)




class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = TestGUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
