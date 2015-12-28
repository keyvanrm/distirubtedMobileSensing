__author__ = 'keyvan'
import numpy as np
import pathInfoMapping as pim
import operator

class GreedySolver:
    def __init__(self, x_grid_max, y_grid_max):

        self.g = set([])
        self.c = []
        self.x_grid_max = x_grid_max
        self.y_grid_max = y_grid_max
        self.traffic_mapped = np.load('mapped_traffic.npy')
        self.traffic_num = len(self.traffic_mapped)
        self.g_index = []
        self.g_amount = [0]

        self.ground_cov = np.load('covariance_mat_50_30.npz')
        self.ground_set = range(self.x_grid_max*self.y_grid_max)
        self.pi = pim.PathInfoMap()
        self.ground_set_info = np.load('ground_set_info.npy')
        self.vehicle_info = np.load('vehicle_info.npy')
        self.vehicles_not_chosen = [i for i in range(self.traffic_num)]

    def test(self):
        # print self.ground_set_info
        # self.traffic_mapped[1] = set(self.traffic_mapped[119])
        print self.pi.cal_mutual_info(set(self.traffic_mapped[0]), self.ground_set)
        # print self.pi.cell_info[2]

    def solve(self):
        for i in range(90):
            self.find_next()
        print self.g_amount
        print self.g_index
        print self.c
        np.save('g_seq', self.g_amount)
        np.save('c_seq', self.c)
        np.save('ind_seq', self.g_index)

    def find_next(self):
        q_max = -1000
        chosen_index = -1
        c = -1
        if len(self.g) == 0:
            chosen_index, maximum_info = max(enumerate(self.vehicle_info), key=operator.itemgetter(1))
            self.vehicles_not_chosen.remove(chosen_index)
            self.g = self.g | set(self.traffic_mapped[chosen_index])
            self.g_amount.append(maximum_info)
            self.c.append(0)
            self.g_index.append(chosen_index)
        else:
            for i in self.vehicles_not_chosen:
                # print i
                gi = self.vehicle_info[i]
                ci = self.pi.cal_mutual_info(set(self.traffic_mapped[i]), self.g)
                if ci == float('inf'):
                    ci = 1000
                    print 'inf cost encountered at vehicle:'
                    print i
                q = (gi-ci)/(ci+0.01)
                if (q > q_max):
                    chosen_index = i
                    c = ci
                    q_max = q
            self.vehicles_not_chosen.remove(chosen_index)
            self.g = self.g | set(self.traffic_mapped[chosen_index])
            self.g_amount.append((self.vehicle_info[chosen_index]-c))
            self.c.append(c)
            self.g_index.append(chosen_index)











