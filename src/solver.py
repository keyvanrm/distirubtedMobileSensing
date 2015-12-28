import map
import radomWalkPathGen as rw
import randomField as rf
import pathInfoMapping as pi
import numpy as np
import postProcess as pps
import math
import greedySolver as gs
from array import array
import operator

x_grid_max = 50
y_grid_max = 30

# city_map = map.Map(0, 0, 0, 0, 0)
# my_field = rf.RandomField(x_grid_max, y_grid_max)
# my_field.generate_field_structure()
# my_field.save_field_structure()
# my_field.load_field_structure()
# my_field.generate_covariance()
# my_field.generate_samples()
# my_field.realization_heat_map()

traffic = rw.TrafficInit(120, 50, 30)
# traffic.traffic_gen()
traffic.traffic_plot()
# traffic.map_traffic()

# path_info = pi.PathInfoMap()
# path_info.path_info_cal()
# path_info.test()
# print np.load('ground_set_info.npy')
# path_info.save_cell_info()
# print path_info.cell_shared_info

# solution = gs.GreedySolver(x_grid_max, y_grid_max)
# solution.solve()
# solution.test()
# print solution.g
# print solution.g_amount
# print solution.g_index

# pp = pps.PostProcess(x_grid_max, y_grid_max)
# pp.plot_revealed_info(30)
# pp.plot_trend()
# pp.plot()

# it1 = np.load('cell_revealed_info_itr_1.npy')
# it2 = np.load('cell_revealed_info_itr_10.npy')
# it3 = np.load('cell_revealed_info_itr_30.npy')
# print it1
# print it2
# print it3