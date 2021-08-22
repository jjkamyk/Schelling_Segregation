Joanna Kamyk (230027), Wojciech ¯u³awiñski (230022)
Agent-based modelling: List 4 (Schelling model)

Files:
1. 'schelling_model.py': main file of model's implementation (with exemplary execution)
2. 'lattice_draw.py': secondary class for graphical purposes (taken from our previous implementations)
3. 'sm_testing.py': functions for executing gifs and plots that were needed

Notes: 
1. In gifs for j=0.75 for one class and j=0.375 for second class the max_iter parameter is equal to 100, 
because of the fact that for greater values of N grid's behaviour after several iterations becomes "periodic": 
the second-class agents stay on their cells (because of lower j) and only some first-class agents move 
in each iteration because their to-stay ratio (j) is too large for the remaining cells.

2. In Plot_j_segindex (segregation index vs to-stay parameter) notice the huge drop from value for j=0.75 to value for j=0.8.

3. The additional plots and gifs were also attached:
- plot number-of-iterations vs to-stay ratio
- gif for 3 classes
- gif for neighborhood_layers=3
- gifs for alternative treatment of alone agents:unhappy (in default we treat them as happy)
