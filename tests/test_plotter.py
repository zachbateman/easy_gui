import unittest
import sys
sys.path.insert(1, '..')
import easy_gui
from matplotlib.figure import Figure
import time

data = [(1, 1), (2, 3), (3, 5), (4, 4), (5, 7), (6, 7)]


class TestPlotterGUI(unittest.TestCase):

    def setUp(self):
        self.gui = easy_gui.EasyGUI()


    def test_gui(self):
        self.gui.add_section('controls')
        self.gui.sections['controls'].add_widget(type='button', text='Scatter Plot', command_func=lambda e: print('Button1 working!'))
        self.gui.sections['controls'].add_widget(type='button', text='Line Plot', command_func=lambda e: print('Button1 working!'))

        self.gui.add_section('display')
        plot = self.gui.sections['display'].add_widget(type='matplotlib', return_widget=True)


        fig = Figure(figsize=(4,3), dpi=100)
        ax = fig.add_subplot(111)
        ax.scatter([t[0] for t in data], [t[1] for t in data])
        plot.draw_plot(mpl_figure=fig)

        time.sleep(2)

        fig = Figure(figsize=(4,3), dpi=100)
        ax = fig.add_subplot(111)
        ax.scatter([t[1] for t in data], [t[0] for t in data])
        plot.draw_plot(mpl_figure=fig)


        self.gui.mainloop()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
