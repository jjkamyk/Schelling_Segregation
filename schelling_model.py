from lattice_draw import LatticeDraw
import numpy as np
import random
import itertools
import matplotlib.patches as patch


# We have implemented the Schelling model using the following class.
# It is strongly based on our previous implementations,
# i.e. we are using the secondary class LatticeDraw in graphical purposes.


class SchellingModel:

    def __init__(self, L, N, number_of_types=2, save_graphics_flag=False):
        self.size = L
        self.each_type_agents_number = N  # N = number of agents of each type (!)
        self.number_of_types = number_of_types  # number of classes of agents (2-10)
        self.save_graphics_flag = save_graphics_flag
        self.cell_states = {}
        for x in range(self.size):
            for y in range(self.size):
                self.cell_states[
                    (x, y)] = -1  # creating the lattice, setting all cells as empty (value -1 means empty cell)
        indices = np.random.choice(L ** 2, N * number_of_types,
                                   replace=False)  # generating random indexes on lattice for agents
        for i in range(number_of_types):
            sub_indices = indices[i * N:N * (i + 1)]  # indexes for each class
            for index in sub_indices:
                x, y = np.unravel_index(index, (L, L))  # 'reshaping' the 1D index into point on lattice
                self.cell_states[(x, y)] = i  # setting the state of cell as type of agent who lives there
        self.cycles = 0  # attribute of class: number of full iterations in simulation
        self.segregation_index = 0  # attribute of class: segregation_index of whole model
        # (which is calculated by method segregate_index_calculate())
        self.shifts = []  # this will be used for searching cell's neighbors
        self.neighbor_cells = {}  # as above
        if save_graphics_flag:  # graphical procedures (creating the object LatticeDraw),
            # activates only if the appropriate flag is set True
            self.drawing_machine = LatticeDraw(L)
            self.color_list = ['tab:blue', 'tab:red', 'tab:green', 'tab:orange', 'tab:purple', 'tab:brown', 'tab:pink',
                               'tab:gray', 'tab:olive', 'tab:cyan']

    def get_states(self):  # obtaining a list of lists of cells in subsequent states (with empty cells as first sublist)
        states = [[] for i in range(self.number_of_types + 1)]
        for cell, state in self.cell_states.items():
            states[state + 1].append(cell)
        return states

    def save_neighbor_cells(self,
                            neighborhood_layers):  # finding the neighbor cells for each cell
        # and saving it in dictionary
        # for performance purposes - not to find them for each iteration (because of large number of iterations)
        # building for each cell a 'square' of its neighbors
        # (its size depends on given neighborhood_layers in simulation)
        vector = np.array(np.arange(-neighborhood_layers, neighborhood_layers + 1))
        shifts = list(itertools.product(vector, repeat=2))
        shifts.remove((0, 0))  # removing the given cell from this 'square' (because it is not its neighbor)
        for cell in self.cell_states.keys():
            self.neighbor_cells[cell] = [((shift[0] + cell[0]) % self.size, (shift[1] + cell[1]) % self.size) for shift
                                         # periodic (toroidal) boundary conditions obtained using modulo
                                         in shifts]

    def get_neighbors_ratio(self, cell, cell_type, neighborhood_layers,
                            alone_happy):  # getting proportion of neighbors which are of the same type as given cell
        numerator = 0
        denominator = (1 + neighborhood_layers * 2) ** 2 - 1  # maximal denominator (number of all neighbors)
        possible_neighbors = self.neighbor_cells[cell]
        for neighbor in possible_neighbors:
            if self.cell_states[neighbor] == cell_type:
                # adding one to ratio's numerator if we find neighbor of the same type
                numerator += 1
            elif self.cell_states[neighbor] == -1:
                denominator -= 1  # we are subtracting 1 from ratio's denominator for each empty neighborcell found
        if denominator == 0:  # two approaches for alone agents treatment: happy or unhappy
            if alone_happy:
                neighbor_ratio = 1
            else:
                neighbor_ratio = 0
        else:
            neighbor_ratio = numerator / denominator
        return neighbor_ratio

    def simulation(self, max_iter, parameters_to_stay, neighborhood_layers=1,
                   alone_happy=True):  # main method of class: simulation of Schelling model
        # arguments: max_iter - maximal number of iterations,
        #           parameters_to_stay - list (of length=number_of_types) of j-parameters:
        #               minimal neighbor ratio that allows cell to stay for each class
        #           neighborhood_layers - number of layers of neighborhood, 
        #           alone_happy - flag: if True, alone agents are treated as happy, if False: as unhappy
        self.setup_pictures(parameters_to_stay=parameters_to_stay,
                            neighborhood_layers=neighborhood_layers, alone_happy=alone_happy)
        states = self.get_states()
        empty_cells = states[0]
        nonempty_cells = states[1:]
        if self.save_graphics_flag:
            self.update_pictures(nonempty_cells, self.cycles)
        self.save_neighbor_cells(neighborhood_layers)
        empty_cells_number = self.size ** 2 - self.each_type_agents_number * self.number_of_types
        loop_continue_flag = True
        while loop_continue_flag:
            cells_to_check = sum(nonempty_cells, [])  # 'unnest' list of lists of agents of each type
            random.shuffle(cells_to_check)
            loop_continue_flag = False  # setting loop flag to False - if no one is unhappy: break
            for cell in cells_to_check:
                cell_type = self.cell_states[cell]
                neighbors_ratio = self.get_neighbors_ratio(cell, cell_type, neighborhood_layers, alone_happy)
                if neighbors_ratio < parameters_to_stay[cell_type]:  # if ratio < j: move the agent
                    U = np.random.randint(0, empty_cells_number)  # drawing random index to obtain random empty cell
                    new_cell = empty_cells.pop(U)  # removing the obtained empty cell from empties
                    empty_cells.append(cell)  # adding the old agent's cell to empties
                    self.cell_states[cell] = -1
                    self.cell_states[new_cell] = cell_type
                    loop_continue_flag = True  # agent is moved, so the lattice changed: next iteration is activated
            self.cycles += 1
            states = self.get_states()
            empty_cells = states[0]
            nonempty_cells = states[1:]
            if self.save_graphics_flag:
                self.update_pictures(nonempty_cells, self.cycles)  # updating plot of lattice (if exists)
            if loop_continue_flag:
                loop_continue_flag = self.cycles < max_iter  # if max_iter exceeded: break
        if self.save_graphics_flag:
            self.drawing_machine.gif()
        self.segregation_index_calculate(alone_happy)  # at the end of simulation: calculate segregation index

    def setup_pictures(self, parameters_to_stay, neighborhood_layers, alone_happy):  # method for graphical purposes
        if self.save_graphics_flag:
            self.drawing_machine.create_directory()
            self.drawing_machine.draw_lines()
            self.drawing_machine.ax.set_xlabel('j={0}, nbhd_layer={1}, alone_happy={2}'.format(parameters_to_stay,
                                                                                               neighborhood_layers,
                                                                                               alone_happy))
            self.drawing_machine.ax.get_xaxis().set_ticks([])
            self.drawing_machine.ax.get_yaxis().set_ticks([])
            custom_lines = [patch.Rectangle((0, 0), 1, 1, linewidth=0, edgecolor='none', facecolor=color) for color in
                            self.color_list]
            self.drawing_machine.fig.legend(custom_lines,
                                            ['Type {0}'.format(1 + i) for i in range(self.number_of_types)],
                                            'center right')
            self.drawing_machine.fig.subplots_adjust(left=0.05, right=0.75, top=0.90, bottom=0.1)

    def update_pictures(self, nonempty_cells, t):  # method for graphical purposes
        if self.save_graphics_flag:
            self.drawing_machine.remove_squares()
            self.drawing_machine.ax.set_title(
                'Schelling Model with L={0}, N={1}, step={2}'.format(self.size, self.each_type_agents_number, t))
            for i in range(self.number_of_types):
                self.drawing_machine.color_squares(nonempty_cells[i], self.color_list[i])
            self.drawing_machine.save()

    def segregation_index_calculate(self,
                                    alone_happy):  # calculating average similar neighbor index: proportion of
        # nearest neighbors (8-neighborhood!) that has the same type
        # very similar method to get_neighbors_ratio, but for neighborhood_layer set to 1
        shifts = list(itertools.product([-1, 0, 1], repeat=2))
        shifts.remove((0, 0))
        states = self.get_states()
        nonempty_cells = states[1:]
        numerator = 0
        for i in range(self.number_of_types):
            for cell in nonempty_cells[i]:
                num = 0
                den = 8
                nearest_neighbor_cells = [((shift[0] + cell[0]) % self.size, (shift[1] + cell[1]) % self.size) for shift
                                          in
                                          shifts]
                for neighbor in nearest_neighbor_cells:
                    if self.cell_states[neighbor] == i:  # neighbor of the same type
                        num += 1
                    elif self.cell_states[neighbor] == -1:  # empty cell
                        den -= 1
                if den == 0:
                    if alone_happy:
                        neighbor_ratio = 1
                    else:
                        neighbor_ratio = 0
                else:
                    neighbor_ratio = num / den
                numerator += neighbor_ratio
        self.segregation_index = numerator / sum(len(sublist) for sublist in nonempty_cells)


# how to use this class - example
if __name__ == '__main__':
    my_schelling_model = SchellingModel(L=20, N=100, number_of_types=3, save_graphics_flag=False)
    my_schelling_model.simulation(max_iter=100, parameters_to_stay=[0.4] * 3, neighborhood_layers=1, alone_happy=True)
    print(my_schelling_model.cell_states)
    print(my_schelling_model.cycles)
    print(my_schelling_model.segregation_index)