'''
Example easy_gui application.
'''
import sys; sys.path.insert(1, '..')  # Just enables below import of dev library as if normally installed
import easy_gui


class GUI(easy_gui.EasyGUI):  # Our application class inherits easy_gui.EasyGUI
    def __init__(self):  # All layout code is specified in the __init__ method
        self.title('Animal Diet Generator')  # title of GUI window
        self.geometry("425x170")  # size of GUI window

        # A Section can contain individual GUI elements or other Section objects
        section = self.add_section('example_section', return_section=True)
        # If desired, use .configure_grid() to use CSS-style grid layout design!
        # ...Widgets (or Sections) are then given a grid_area for their position in the GUI
        section.configure_grid(['title                title          output',
                                         'label1            entry1        output',
                                         'label2            entry2        output',
                                         'run_button   run_button    output'])
        # The .add_widget method is used for adding all individual GUI components
        section.add_widget(type='label', text='Animal Diet Generator!', grid_area='title')
        section.add_widget(type='label', text='Animal:', grid_area='label1')
        # Widgets can be stored as an attribute by specifying return_widget=True
        self.animal = section.add_widget(type='entry', grid_area='entry1', return_widget=True)
        section.add_widget(type='label', text='Food:', grid_area='label2')
        self.food = section.add_widget(type='entry', grid_area='entry2', return_widget=True)
        section.add_widget(type='stdout', grid_area='output')
        # A button can be assigned a function/method with the "command_func" kwarg
        section.add_widget(type='button', text='Generate Diet!', grid_area='run_button', command_func=self.diet)

    def diet(self, event):
        print(f'The {self.animal.get()} likes to eat {self.food.get()}!')



if __name__ == '__main__':
    # Simply create an instance of the application class ("GUI" here) to create and run the application
    application = GUI()
