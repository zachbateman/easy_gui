import unittest
import sys
sys.path.insert(1, '..')
import easy_gui

from matplotlib.figure import Figure

data = [(1, 1), (2, 3), (3, 5), (4, 4), (5, 7), (6, 7)]


class TestPlotterGUI(unittest.TestCase):

    def setUp(self):
        self.gui = easy_gui.EasyGUI()


    def test_gui(self):
        self.gui.add_section('controls')
        self.gui.sections['controls'].add_widget(type='button', text='Scatter Plot', command_func=lambda e: print('Button1 working!'))
        self.gui.sections['controls'].add_widget(type='button', text='Line Plot', command_func=lambda e: print('Button2 working!'))


        figure = Figure(dpi=100, figsize=(2, 2))
        ax = figure.add_subplot(111)
        ax.semilogy([t[0] for t in data], [t[1] for t in data])
        self.gui.add_section('display')
        mplotlib = self.gui.sections['display'].add_widget(type='matplotlib', return_widget=True)
        mplotlib.draw_plot(mpl_figure=figure)


        self.gui.add_section('other_controls')
        self.gui.sections['other_controls'].add_widget(type='label', text='Other controls:')

        self.gui.sections['other_controls'].add_widget(type='button', text='Fun', command_func=lambda x: print('Fun'))

        figure2 = Figure(dpi=100, figsize=(2, 2))
        ax2 = figure.add_subplot(111)
        ax2.semilogy([t[1] for t in data], [t[0] for t in data])

        s2 = self.gui.add_section('display2', return_section=True)
        mplotlib2 = s2.add_widget(type='matplotlib', return_widget=True)
        mplotlib2.draw_plot(mpl_figure=figure2)

        self.gui.mainloop()
        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main() #buffer=True)
