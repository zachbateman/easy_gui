'''
Example easy_gui application.
'''
import sys; sys.path.insert(1, '..')  # Just enables below import of dev library as if normally installed
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
