'''
Example easy_gui application
'''
import sys
sys.path.insert(1, '..')
import easy_gui


class GUI(easy_gui.EasyGUI):  # Our application class inherits easy_gui.EasyGUI
    def __init__(self):  # All layout code is specified in the __init__ method
        self.title('Animal Diet Generator')  # title of GUI window
        self.geometry("600x200")  # size of GUI window

        section = self.add_section('test_section', return_section=True)
        section.configure_grid(['title               title           output',
                                         'label1           entry1         output',
                                         'label2           entry2         output',
                                         'run_button   run_button    output'])

        section.add_widget(type='label', text='Animal Diet Generator!', grid_area='title')
        section.add_widget(type='label', text='Animal:', grid_area='label1')
        self.animal = section.add_widget(type='entry', grid_area='entry1', return_widget=True)
        section.add_widget(type='label', text='Food:', grid_area='label2')
        self.food = section.add_widget(type='entry', grid_area='entry2', return_widget=True)
        section.add_widget(type='stdout', grid_area='output')
        section.add_widget(type='button', text='Generate Diet!', grid_area='run_button', command_func=self.diet)

    def diet(self, *args):
        print(f'The {self.animal.get()} likes to eat {self.food.get()}!')



if __name__ == '__main__':
    application = GUI()
