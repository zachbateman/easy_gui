import unittest
import sys
sys.path.insert(1, '..')
import easy_gui



class GUI(easy_gui.EasyGUI):
    def __init__(self):
        self.geometry('300x300')
        self.date = self.add_widget('date')
        self.add_widget(type='button', text='Print Date', command_func=self.print_date)
        
    def print_date(self, *args):
        print(self.date.get())



class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = GUI()


if __name__ == '__main__':
    unittest.main() #buffer=True)
