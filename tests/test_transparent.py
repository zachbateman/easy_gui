import unittest
import sys
sys.path.insert(1, '..')
import easy_gui
from easy_gui import EasyGUI, styles
from matplotlib.figure import Figure
from pprint import pprint as pp


EasyGUI.style = styles.TransparentStyle()


data = [(1, 1), (2, 3), (3, 5), (4, 4), (5, 7), (6, 7)]




class PlotterGUI(easy_gui.EasyGUI):
    def __init__(self):
        self.geometry('500x500')
        self.transparent = True
        controls = self.add_section('controls')
        controls.add_widget(type='button', text='Scatter Plot', command_func=self.draw_scatter)
        controls.add_widget(type='button', text='Line Plot', command_func=self.draw_line)

        self.display = self.add_section('display')
        self.plot = self.sections['display'].add_widget(type='matplotlib')


    def draw_scatter(self, *args):
        fig = Figure(figsize=(4,3), dpi=100)
        ax = fig.add_subplot(111)
        ax.scatter([t[1] for t in data], [t[0] for t in data])
        self.plot.draw_plot(mpl_figure=fig)

    def draw_line(self, *args):
        fig = Figure(figsize=(4,3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot([t[1] for t in data], [t[0] for t in data])
        self.plot.draw_plot(mpl_figure=fig)



class TestPlotterGUI(unittest.TestCase):
    def test_gui(self):
        gui = PlotterGUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
