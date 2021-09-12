# easy_gui

easy_gui is a high-level Python library designed to simplify the process of creating GUI applications by wrapping tkinter.  Solving problems is tricky enough... using our solutions should be EASY!


# Features

  - Quickly and easily build a GUI by subclassing easy_gui.EasyGUI
  - Add easy_gui Widget objects (check out widgets.py for details on each):
    - Button, Label, Entry, LabelEntry, CheckBox, DropDown, ListBox, Table, Tree, MatplotlibPlot, ProgressBar, ScrolledText, StdOutBox, DatePicker
  - Create one or more Sections (including nested Sections) to help organize GUI elements
  - CSS Grid-style layouts
  - Simply create a popup window using EasyGUI.popup()
  - Multithreading for GUI responsiveness (set "separate_thread=True" when creating a Button Widget)
  - Easy to install with few dependancies - just matplotlib (but you want to make plots anyway, right?!)


# Quickstart

  - Installing easy_gui is easy enough.  Simply use pip:
  ```
  pip install easy_gui
  ```

  - To create an application with easy_gui, subclass the easy_gui.EasyGUI class and add elements in the init method.

  - Here is the most simple example:
  ```
  import easy_gui

  class GUI(easy_gui.EasyGUI):
      def __init__(self):
          self.add_widget(type='label', text='Example Label')
          self.add_widget(type='button', text='Button', command_func=lambda x: print('TEST'))

  application = GUI()
  ```
  <img src="examples/super_simple_gui.png" width="200px">


  - Now for a more substantial example that also shows CSS-style layout capabilities.  See the script examples/simple_gui.py for this code with additional explanatory comments:
  ```
  import easy_gui

  class GUI(easy_gui.EasyGUI):
      def __init__(self):
          self.title('Animal Diet Generator')
          self.geometry("425x170")

          section = self.add_section('example_section')
          section.configure_grid(['title             title         output',
                                  'label1            entry1        output',
                                  'label2            entry2        output',
                                  'run_button      run_button      output'])
          section.add_widget(type='label', text='Animal Diet Generator!', grid_area='title')
          section.add_widget(type='label', text='Animal:', grid_area='label1')
          self.animal = section.add_widget(type='entry', grid_area='entry1')
          section.add_widget(type='label', text='Food:', grid_area='label2')
          self.food = section.add_widget(type='entry', grid_area='entry2')
          section.add_widget(type='stdout', grid_area='output')
          section.add_widget(type='button', text='Generate Diet!', grid_area='run_button', command_func=self.diet)

      def diet(self, event):
          print(f'The {self.animal.get()} likes to eat {self.food.get()}!')

  application = GUI()
  ```
  <img src="examples/simple_gui.png" width="425px">


# More Firepower

The toy examples above show the basics for getting started.  Below is a more robust example for what a simple tool could look like.
This example highlights a number of powerful features such as:
  - CSS-style grid layouts (literally make a picture of what you want to see with a list of strings)
  - Flexible, high-level Widgets that are quick to add or manipulate
  - Quick and easy popup window using `with self.popup() as popup:`

  <img src="examples/moderate_gui.png" width="800px">

  ```
    import easy_gui
    import random
    from matplotlib.figure import Figure


    class GUI(easy_gui.EasyGUI):
        def __init__(self):
            self.title('Data Generator')
            self.geometry("800x550")

            self.configure_grid(['check   data_gen   info',
                                       'tree       tree        data',
                                       'tree       tree        plot'])

            self.parabolic = self.add_widget('checkbox', 'Parabolic Data', grid_area='check')
            self.add_widget('btn', 'Generate New Data', grid_area='data_gen', use_ttk=True, command_func=self.generate_data)
            self.add_key_trigger('new', self.generate_data)
            print('Also can generate new data by simply typing "new"!')

            info = self.add_section(grid_area='info')
            info.configure_grid([' .        title     . ',
                                       'mean   min  max'])
            info.add_widget('lbl', 'Data Information', underline=True, bold=True, grid_area='title')
            self.mean = info.add_widget('lbl', 'Mean:', grid_area='mean')
            self.min = info.add_widget('lbl', 'Minimum:', grid_area='min')
            self.max = info.add_widget('lbl', 'Maximum:', grid_area='max')

            self.tree = self.add_widget('tree', grid_area='tree', height=10)
            self.tree.bind_select(self.refresh_display)

            self.table = self.add_widget('table', rows=2, columns=11, border=True, grid_area='data')
            self.table[1, 1] = 'X Values'
            self.table[2, 1] = 'Y Values'

            self.plot = self.add_widget('matplotlib', grid_area='plot')

            self.add_menu(commands={}, cascades={'Data': {'Save Data to CSV': self.save_data}})

            self.data_sets = []  # store all generated datasets in this list
            self.generate_data()  # start with one initial dataset


        def current_data(self):
            name, x_vals, y_vals = [tup for tup in self.data_sets if tup[0] == self.tree.current_row['text']][0]
            return name, x_vals, y_vals

        def refresh_tree(self, *args):
            self.tree.clear()
            for name, x_vals, y_vals in self.data_sets:
                self.tree.insert_row(name)
            self.tree.select_first_row()
            self.refresh_display()

        def refresh_display(self, *args):
            name, x_vals, y_vals = self.current_data()

            # Update summary info at top
            self.mean.set(f'Mean: {round(sum(y_vals) / len(y_vals), 1)}')
            self.min.set(f'Minimum: {min(y_vals)}')
            self.max.set(f'Maximum: {max(y_vals)}')

            # Update table with current data
            for index, (x, y) in enumerate(zip(x_vals, y_vals)):
                self.table[1, index+2] = x
                self.table[2, index+2] = y

            # Update the plot
            fig = Figure(figsize=(5, 3), dpi=100)
            ax = fig.add_subplot(111)
            ax.set_title('Plot of X and Y Values')
            ax.scatter(x_vals, y_vals)
            self.plot.draw_plot(mpl_figure=fig)

        def generate_data(self, *args):
            x_vals = list(range(1, 11))
            if not self.parabolic.get():
                y_vals = [round(x + random.random() * 2, 1) for x in x_vals]
            else:
                y_vals = [round((x - 5 + random.random()) ** 2, 1) for x in x_vals]
            self.data_sets.append((f'Dataset {len(self.data_sets)+1}' + (' (Parabolic)' if self.parabolic.get() else ''), x_vals, y_vals))
            self.refresh_tree()

            with self.popup() as popup:
                popup.geometry('200x80')
                popup.add_widget('lbl', 'New data generated!', bold=True)

        def save_data(self, *args):
            with open('Moderate GUI Data.csv', 'w') as f:
                f.write('Dataset,X_Values,Y_Values\n')
                for name, x_vals, y_vals in self.data_sets:
                    for x, y in zip(x_vals, y_vals):
                        f.write(f'{name},{x},{y}\n')
            print('Data saved to CSV file!')



    if __name__ == '__main__':
        GUI()
  ```



License
----
MIT
