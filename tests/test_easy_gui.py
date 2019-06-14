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
        self.gui.mainloop()
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main(buffer=True)
