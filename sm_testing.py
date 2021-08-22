from schelling_model import SchellingModel
import numpy as np
import matplotlib.pyplot as plt


# ------------- exemplary animation -------------
# function generates an example of gif
# see: simulation.gif in Results directory

def gif_example():
    L = 20
    N = 100
    no_of_types = 2
    save_graphics = True
    max_iter = 100
    js = [0.5] * no_of_types
    nbhd_layers = 3
    SM = SchellingModel(L=L, N=N, number_of_types=no_of_types, save_graphics_flag=save_graphics)
    SM.simulation(max_iter=max_iter, parameters_to_stay=js, neighborhood_layers=nbhd_layers)


# ------------- exercise 3 -------------
# function generates plot of number of iterations with respect to number of agents of each type
# see: Plot_N_iterations.png

def plot_no_iter_no_agents():
    L = 100
    Ns = [x * 250 for x in range(1, 17)]
    number_of_types = 2
    neighborhood_layer = 1
    max_iter = 10000
    J = [0.5] * number_of_types
    cycles_alone_happy = []
    cycles_alone_unhappy = []
    for N in Ns:
        SM = SchellingModel(L, N, number_of_types)
        SM.simulation(max_iter, J, neighborhood_layer, alone_happy=True)
        cycles_alone_happy.append(SM.cycles)
        SM = SchellingModel(L, N, number_of_types)
        SM.simulation(max_iter, J, neighborhood_layer, alone_happy=False)
        cycles_alone_unhappy.append(SM.cycles)

    plt.figure()
    plt.plot(Ns, cycles_alone_happy, label='alone agent: happy', color='b')
    plt.plot(Ns, cycles_alone_unhappy, label='alone agent: unhappy', color='r')
    plt.plot(Ns, cycles_alone_happy, '.', color='b')
    plt.plot(Ns, cycles_alone_unhappy, '.', color='r')
    plt.legend()
    plt.xlabel('number of agents of each type')
    plt.ylabel('number of iterations')
    plt.title(
        'L = {0}, j = {1}, nbhd_layer = {2}, no. of types = {3}'.format(L, J, neighborhood_layer, number_of_types))


# ------------- exercise 4 -------------
# function generates plot of segregation index with respect to to-stay parameter
# see: Plot_j_segindex.png (notice the significant drop from j=0.75 to 0.8)

def plot_segr_indx_j():
    L = 100
    N = 4500
    max_iter = 10000
    number_of_types = 2
    js = np.linspace(0.1, 0.9, 17)
    neighborhood_layer = 1
    segregation_indices = []
    for j in js:
        SM = SchellingModel(L, N, number_of_types)
        SM.simulation(max_iter, [j] * number_of_types, neighborhood_layer)
        segregation_indices.append(SM.segregation_index)
    #
    plt.figure()
    plt.plot(js, segregation_indices, color='blue')
    plt.plot(js, segregation_indices, '.', color='blue')
    plt.xlabel('to-stay parameter j')
    plt.ylabel('segregation index')
    plt.title('L = {0}, N = {1}, max_iter = {2}, nbhd_layer = {3}, number_of_types = {4}'.format(L, N, max_iter,
                                                                                                 neighborhood_layer,
                                                                                                 number_of_types))


# ------------- exercise 5 -------------
# function generate plot of segregation index with respect to neighborhood layer
# see: Plot_neighborhoodlayer_segindex.png

def plot_segr_indx_nbhd_lay():
    L = 100
    N = 4500
    nei_layers = [1, 2, 3, 4, 5]
    max_iter = 1000
    number_of_types = 2
    J = [0.5] * number_of_types
    segregation_indices = []
    for nl in nei_layers:
        SM = SchellingModel(L, N, number_of_types)
        SM.simulation(max_iter, J, nl)
        segregation_indices.append(SM.segregation_index)

    plt.figure()
    plt.plot(nei_layers, segregation_indices)
    plt.plot(nei_layers, segregation_indices, '.')
    plt.xlabel('neighborhood layer')
    plt.ylabel('segregation index')
    plt.title(
        'L = {0}, N = {1}, max_iter = {2}, j = {3}, number_of_types = {4}'.format(L, N, max_iter, J, number_of_types))
    plt.xticks(nei_layers)


# ------------- plot no. of iterations with respect to j -------------
# function generates plot of number of cycles with respect to to-stay parameter
# see: plot_no_iter_j.png

def plot_no_cycles_j():
    L = 100
    N = 4500
    max_iter = 1000
    js = np.linspace(0.1, 0.9, 17)
    neighborhood_layer = 1
    cycles_numbers = []
    for j in js:
        SM = SchellingModel(L, N, save_graphics_flag=False)
        SM.simulation(max_iter, [j, j], neighborhood_layer)
        cycles_numbers.append(SM.cycles)

    plt.figure()
    plt.plot(js, cycles_numbers)
    plt.plot(np.linspace(0, 1, 17), np.array([max_iter for i in range(len(cycles_numbers))]), 'r--')
    plt.xlim(0, 1)
    plt.xlabel('to-stay parameter j')
    plt.ylabel('number of cycles')
    plt.title('L = {0}, N = {1}, max_iter = {2}, nbhd_layer = {3}'.format(L, N, max_iter, neighborhood_layer))


if __name__ == '__main__':
    gif_example()
