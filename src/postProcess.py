import numpy as np
import scipy as sp
import pathInfoMapping as pim
from pylab import *
import matplotlib.pyplot as plt

class PostProcess:

    def __init__(self, x_grid_max, y_grid_max):
        self.c_seq = np.load('c_seq.npy')
        self.g_sec = np.load('g_seq.npy')
        self.ind_seq = np.load('ind_seq.npy')
        self.mapped_traffic = np.load('mapped_traffic.npy')
        self.target_itterations = [1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 60]
        self.x_grid_max = x_grid_max
        self.y_grid_max = y_grid_max
        self.grid_max = x_grid_max*y_grid_max
        self.cell_revealed_info = [0 for i in range(self.grid_max)]
        self.pi = pim.PathInfoMap()
        self.ground_set = range(self.grid_max)
        # print len(self.g_sec), len(self.c_seq)

    def save_revealed_info(self, itteration):

        g = set([])
        for i in range(itteration):
            g = g | set(self.mapped_traffic[self.ind_seq[i]])
        for i in range(self.grid_max):
            print('target itr: ', itteration, '    cell: ', i)
            if i in g:
                self.cell_revealed_info[i] = 0.9
            else:
                self.cell_revealed_info[i] = self.pi.cal_mutual_info(set([i]), g)/0.3

        name = 'cell_revealed_info_itr_%d' % itteration
        np.save(name, self.cell_revealed_info)

    def run(self):
        for i in self.target_itterations:
            self.save_revealed_info(i)

        # for i in self.ground_set:
        #     print 'cell_shared_info:  ', i
        #     this = set([i])
        #     temp = set(range(self.grid_max))- this
        #     self.cell_revealed_info[i] = self.pi.cal_mutual_info(this, temp)
        # np.save('cell_shared_info', self.cell_revealed_info)

    def plot_revealed_info(self, itr):
        name = 'cell_revealed_info_itr_%d.npy' % itr
        figname_pdf = 'cell_revealed_info_itr_%d.pdf' % itr
        figname_png = 'cell_revealed_info_itr_%d.png' % itr
        info = np.load(name)
        info = info.reshape(self.y_grid_max, self.x_grid_max)
        c = pcolor(info)
        set_cmap('gray')
        colorbar()
        # c = pcolor(info, edgecolors='w', linewidths=1)
        axis([0, 50, 0, 30])
        savefig(figname_pdf)
        savefig(figname_png)
        close()

    def plot_trend(self):
        # plt.figure(1)
        # plt.plot(self.g_sec)
        # plt.ylabel('bits of information')
        # plt.xlabel('number of vehicles chosen')
        # plt.title('Delta Gain')
        # plt.grid()
        # plt.savefig('delta_gain.png')
        # plt.savefig('delta_gain.pdf')
        #
        # plt.figure(2)
        # plt.plot(self.c_seq)
        # plt.ylabel('bits of information')
        # plt.xlabel('number of vehicles chosen')
        # plt.title('Delta Cost')
        # plt.grid()
        # plt.savefig('delta_cost.png')
        # plt.savefig('delta_cost.pdf')
        #
        # plt.figure(3)
        # temp = [log(self.g_sec[i]/(self.c_seq[i]+0.01)) for i in range(len(self.c_seq))]
        # plt.plot(temp)
        # plt.ylabel('log dg/dc')
        # plt.xlabel('number of vehicles chosen')
        # plt.title('Delta Gain over Delta Cost')
        # plt.grid()
        # plt.savefig('dg_over_dc.png')
        # plt.savefig('dg_over_dc.pdf')
        # #
        g_t = np.cumsum(self.g_sec)
        c_t = np.cumsum(self.c_seq)
        # #
        # plt.figure(4)
        # plt.plot(g_t)
        # plt.ylabel('Bits of information')
        # plt.xlabel('number of vehicles chosen')
        # plt.title('Information gained')
        # plt.grid()
        # plt.savefig('Gain.png')
        # plt.savefig('Gain.pdf')
        #
        # plt.figure(5)
        # plt.plot(c_t)
        # plt.ylabel('Bits of information')
        # plt.xlabel('number of vehicles chosen')
        # plt.title('Cost')
        # plt.grid()
        # plt.savefig('cost.png')
        # plt.savefig('cost.pdf')
        #
        # #
        g_new = np.transpose(g_t[1:])
        c_new = np.transpose(c_t[:])
        # # print g_new
        # # print c_new
        # plt.figure(6)
        # plt.plot(c_new+0.000001, g_new)
        # plt.ylabel('Bits of information')
        # plt.xlabel('Bits of information')
        # plt.title('Information gained vs cost incurred')
        # plt.grid()
        # # plt.show()
        # plt.savefig('Information gained vs cost incurred.png')
        # plt.savefig('Information gained vs cost incurred.pdf')

        plt.figure(7)
        plt.plot(log(g_new/(c_new+0.01)))
        plt.ylabel('log relative size')
        plt.xlabel('Number of cars picked')
        plt.title('Information gained over cost incurred')
        plt.grid()
        # plt.show()
        plt.savefig('g_over_c.png')
        plt.savefig('g_over_c.pdf')



    def plot(self):
        for i in self.target_itterations:
            self.plot_revealed_info(i)





