__author__ = 'keyvan'
import randomField as rf
import numpy as np
import scipy as sp
import scipy.sparse as sparse
import math
#import map

class PathInfoMap:

    def __init__(self):
        self.cov = rf.RandomField.load_sparse_csc("covariance_mat_50_30.npz").todense()
        self.traffic = np.load('mapped_traffic.npy')
        self.traffic_num = len(self.traffic)
        self.x_grid_max = 50  # my_map.x_grid
        self.y_grid_max = 30  # my_map.y_grid
        self.grid_max = self.x_grid_max * self.y_grid_max
        self.ground_set = range(self.grid_max)
        self.ground_set_info = 0
        # self.ground_set_size = PathInfoMap.cal_info(self.cov)
        # self.ground_set_size = 1/2*math.log(2*math.pi*np.linalg.det(self.cov), 2)
        self.number_of_cars = len(self.traffic)
        # self.cell_info = [PathInfoMap.cal_info([self.cov.item((i, i))]) for i in range(self.grid_max)]
        self.cell_shared_info = [0 for i in range(self.grid_max)]
        self.vehicle_info = [0 for i in range(self.number_of_cars)]
        self.path_cell_intersect = [[0 for j in range(self.grid_max)] for i in range(self.number_of_cars)]
        # print self.cell_info[5]
        # print self.ground_set_size

    def test(self):
        s1 = (0, 5, 6, 7, 109)
        s2 = (0, 5, 6, 7, 114)
        # print self.cal_mutual_info([1], [71, 51, 31, 21])
        # print self.cal_mutual_info_2([1], self.ground_set)

    def cal_mutual_info(self, set1, set2):
        set1 = list(set1)
        set2 = list(set2)
        set1.sort()
        set2.sort()
        #set2 gievn set1
        # set2 = set2 - set1
        # set_t = set1 | set2
        cov11 = self.cov[np.ix_(set1, set1)]
        cov12 = self.cov[np.ix_(set1, set2)]
        cov21 = self.cov[np.ix_(set2, set1)]
        cov22 = self.cov[np.ix_(set2, set2)]
        #covariance 2 given covariance 1
        # print sp.linalg.inv(cov11)
        # print cov11
        cov2_1 = cov22 - cov21*sp.linalg.inv(cov11)*cov12
        h2_1 = PathInfoMap.cal_info(cov2_1) # h(2|1)
        h2 = PathInfoMap.cal_info(cov22)    # h(2)
        # print h2
        # print h2_1
        c = h2-h2_1
        # print c
        return c    #I(1,2)

    def cal_mutual_info_2(self, set1, set2):
        set1 = set(set1)
        set2 = set(set2)
        set_t = set1 | set2
        set1 = list(set1)
        set2 = list(set2)
        set_t = list(set_t)
        set1.sort()
        set2.sort()
        set_t.sort()
        cov_1 = self.cov[np.ix_(set1, set1)]
        cov_2 = self.cov[np.ix_(set2, set2)]
        cov_12 = self.cov[np.ix_(set_t, set_t)]

        h1 = PathInfoMap.cal_info(cov_1)
        h2 = PathInfoMap.cal_info(cov_2)
        h12 = PathInfoMap.cal_info(cov_12)

        return [h12-h1, h12-h2, h1+h2-h12]

    @staticmethod
    def cal_info(cov):
        n = len(cov)
        # print cov
        if n == 1:
            r = 0.5*(math.log(2*math.pi*cov[0]))/math.log(2)
        else:
            (s, logdet) = np.linalg.slogdet(2*math.pi*cov)
            r = 0.5*(logdet+(n-1)*math.log(2*math.pi))/math.log(2)
        return r

    def path_info_cal(self):
        for i in range(self.traffic_num):
            temp = self.cal_mutual_info(set(self.traffic[i]), self.ground_set)
            if temp == float('inf'):
                temp = -1000
            self.vehicle_info[i] = temp
        np.save('vehicle_info', self.vehicle_info)
        self.ground_set_info = self.cal_mutual_info(self.ground_set, self.ground_set)
        np.save('ground_set_info', self.ground_set_info)








        # for i in range(self.grid_max):
            # ground_condition_cell =
    #
    # def cal_path_info(self):
    #
    # def cal_cell_path_info_intersect(self):
    #
    # def cal_cell_set_info_intersect(self, set):
    #
    # def cal_set_set_info_intersect(self, set1, set2):
    #

    def save_cell_info(self):
        for i in range(self.grid_max):
            ttt = range(self.grid_max)
            ttt.remove(i)
            temp = self.cal_mutual_info([i], ttt)
            if temp == float('inf'):
                temp == 1000
                print i
            self.cell_shared_info[i] = temp
            print temp
        np.save('cell_info', self.cell_shared_info)

