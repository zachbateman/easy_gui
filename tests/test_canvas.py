import unittest
import sys
sys.path.insert(1, '..')
import easy_gui


colors = [color for _ in range(100) for color in ['red', 'green', 'purple']]

class GUI(easy_gui.EasyGUI):
    def __init__(self):
        self.geometry('400x340')

        canvas = self.add_widget('canvas')
        canvas.create_line(20, 20, 50, 100)
        canvas.create_line(30, 20, 70, 110, tags='line2')
        canvas.itemconfigure('line2', fill=colors.pop())
        canvas.create_text(50, 10, 'Test Text')
        self.canvas = canvas

        self.add_widget('btn', 'Change Line Color', command_func=self.change_line_color)

    def change_line_color(self, *args):
        self.canvas.itemconfigure('line2', fill=colors.pop())


class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = GUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
