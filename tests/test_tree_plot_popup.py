import unittest
import sys
sys.path.insert(1, '..')
import easy_gui
from matplotlib.figure import Figure
from pprint import pprint as pp



class TestGUI(easy_gui.EasyGUI):
    def __init__(self):
        self.geometry('600x800')

        self.add_section('test_section')
        self.sections['test_section'].add_widget(type='button', text='Button1', command_func=lambda e: print('Button1 working!'))
        self.sections['test_section'].add_widget(type='label', text='Here\'s an awesome label!')

        # tree_section = self.add_section('tree_section', title=True)
        # x = tree_section.add_widget('LabelEntry', 'Test...')
        # x.bind_select(self.plot_current)

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
        
        self.plot.bind_select(self.show_popup) #, separate_thread=True)
        # breakpoint()
        pp(self.sections)
    

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
        
    def show_popup(self, *args):
        with self.popup() as popup:
            popup.add_widget('lbl', 'Test Label')
            popup.add_widget('btn', 'Test Button 1', command_func=lambda *args: print('Test Button 1 clicked'))
            popup.add_widget('lbl', 'Test Label2')
            label3 = popup.add_widget('lbl', 'Test Label3')
            label3.set('Hello World')

            popup.add_widget('checkbox', 'Checkbox')
            popup.add_widget('labelentry', 'Label Entry')
            popup.add_widget('listbox')
            
            sec = popup.add_section('sec')
            sec.add_widget('btn', 'Test Button 2', command_func=lambda *args: sec.add_widget('lbl', 'ADDED'))
            sec.add_widget('lbl', 'Label in Section...')
            
            plot = popup.add_widget('matplotlibplot')
            x = list(range(1, 11))
            y = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
            if self.tree.current_row['text'] == 'Item A':
                y = [5, 5, 5, 5, 5] + y[5:]
            elif self.tree.current_row['text'] == 'Item B':
                y = y[:5] + [14, 14, 14, 14, 14]
            fig = Figure(figsize=(5, 3), dpi=100)
            ax = fig.add_subplot(111)
            ax.scatter(x, y)
            plot.draw_plot(mpl_figure=fig)


class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = TestGUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
