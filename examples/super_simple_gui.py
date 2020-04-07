'''
Example super simple easy_gui application.
'''
import sys; sys.path.insert(1, '..')  # Just enables below import of dev library as if normally installed
import easy_gui
  
class GUI(easy_gui.EasyGUI):
    def __init__(self):
        section = self.add_section('example')
        section.add_widget(type='label', text='Example Label')
        section.add_widget(type='button', text='Button', command_func=lambda x: print('TEST'))
  
application = GUI()
