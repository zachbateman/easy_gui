import unittest
import sys
sys.path.insert(1, '..')
import easy_gui
import time



class GUI(easy_gui.EasyGUI):
    def __init__(self):
        s = self.add_section('test_section')
        s.add_widget(type='button', text='Button1', command_func=self.update_progress, separate_thread=True)
        s.add_widget(type='label', text='Click the button for a progress bar!')
        self.progressbar = s.add_widget(type='progressbar')

    def update_progress(self, *args):
        self.progressbar.set(0)
        for _ in range(100):
            time.sleep(0.01)
            self.progressbar.progress_handler()
            print(self.progressbar.get())



class TestEasyGUI(unittest.TestCase):
    def test_gui_creation(self):
        gui = GUI()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main() #buffer=True)
