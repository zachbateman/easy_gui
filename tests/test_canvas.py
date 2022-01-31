import unittest
import sys
sys.path.insert(1, '..')
import easy_gui


colors = [color for _ in range(100) for color in ['red', 'green', 'purple']]

class GUI(easy_gui.EasyGUI):
    def __init__(self):
        self.geometry('500x550')

        canvas = self.add_widget('canvas')
        self.canvas = canvas

        canvas.create_line(20, 20, 50, 100, tags='1234')
        canvas.create_line(30, 20, 70, 110, tags='line2')
        canvas.itemconfigure('line2', fill=colors.pop())

        canvas.create_text(50, 10, 'Test Text')
        canvas.create_text(20, 200, 'Test Text2', fontsize=15, bold=True)

        canvas.create_rectangle(100, 100, 110, 130)
        canvas.create_oval(30, 100, 40, 130)

        canvas.create_circle(150, 40, radius=25, tags='circle')
        canvas.bind_click('circle', self.change_circle_color)

        canvas.create_polygon(180, 80, 230, 100, 250, 150, tags='triangle')
        canvas.bind_click('triangle', self.change_triangle_color)

        canvas.create_arc(100, 150, 200, 250, start=0, extent=60, tags='arc1', style='pie')
        canvas.bind_click('arc1', lambda _: print(' - Arc [pie] Clicked -'))

        canvas.create_arc(50, 80, 200, 230, start=0, extent=120, width=10, tags='arc2', style='arc')
        canvas.bind_click('arc2', lambda _: print(' - Arc [arc] Clicked -'))

        self.add_widget('btn', 'Change Line Color', command_func=self.change_line_color)

        self.add_widget('canvasbutton', text='Canvas Button', form='rounded', command_func=lambda _: print(' - CanvasButton Clicked -'))
        self.add_widget('canvasbutton', text='Delete Arc2', form='angular', fontsize=8, command_func=self.delete_arc2)

    def delete_arc2(self, *args):
        self.canvas.delete('arc2')

    def change_line_color(self, *args):
        self.canvas.itemconfigure('1234', fill=colors.pop())
        self.canvas.itemconfigure('line2', fill=colors.pop())

    def change_circle_color(self, *args):
        self.canvas.itemconfigure('circle', fill=colors.pop(), outline='black')

    def change_triangle_color(self, *args):
        self.canvas.itemconfigure('triangle', fill=colors.pop(), outline='black')



class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = GUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
