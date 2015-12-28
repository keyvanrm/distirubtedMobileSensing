__author__ = 'keyvan'
import numpy as np
import matplotlib.pyplot as plt


class TrafficInit:

    def __init__(self, car_number, x_grid_max, y_grid_max):
        self.car_number = car_number
        self.car = [] #list of commuter objects
        self.traffic = []
        self.x_grid_max = x_grid_max
        self.y_grid_max = y_grid_max
        self.traffic_num = car_number
        self.traffic_mapped = [[] for i in range(self.traffic_num)]

    def traffic_gen(self):
        for i in range(self.car_number):
            speed = np.random.uniform(0.5, 0.99)
            self.car.append(RandomWalkGen(self.x_grid_max, self.y_grid_max, i, speed))
        for k in range(self.car_number):
            self.traffic.append(self.car[k].path_list)
        # cars = np.asarray(cars)
        np.save('traffic', self.traffic)

    def traffic_plot(self):
        cars = np.load('traffic.npy')
        plt.figure(figsize=(10, 6))
        plt.axis([0, 50, 0, 30])
        for k in range(self.car_number):
            x = [i[0] for i in cars[k]]
            y = [i[1] for i in cars[k]]
            plt.plot(x, y)
        plt.grid()
        # plt.show()
        plt.savefig('traffic_map.pdf', bbox_inches='tight')

    def map_traffic(self):
        self.traffic = np.load('traffic.npy')
        for i in range(self.traffic_num):
            for j in self.traffic[i]:
                self.traffic_mapped[i].append(j[0] + j[1]*self.x_grid_max)
            self.traffic[i] = set(self.traffic[i]) #? not tested yet
        np.save('mapped_traffic', self.traffic_mapped)


class RandomWalkGen:

    def __init__(self, x_grid_max, y_grid_max, car_id, speed):
        self.x_grid_max = x_grid_max
        self.y_grid_max = y_grid_max
        self.x0 = 0
        self.y0 = 0
        self.walk_length = 0
        self.walk_length_min = 20
        self.walk_length_max = 90
        self.path_list = []
        self.car_id = car_id
        self.speed = speed
        self.rw_gen()

    def rw_gen(self):
        self.x0 = x = np.random.random_integers(0, self.x_grid_max-1)
        self.y0 = y = np.random.random_integers(0, self.y_grid_max-1)
        self.walk_length = np.random.random_integers(self.walk_length_min, self.walk_length_max)
        self.path_list.append([x, y])
        for i in range(self.walk_length):
            p = np.random.uniform(0, 1)
            temp = 0
            if p < self.speed:
                temp = 2*np.random.randint(0, 2)-1
                direc = np.random.randint(0, 2)

            if temp != 0:
                x += direc*temp
                y += (1-direc)*temp
                if (-1 < x < self.x_grid_max) & (-1 < y < self.y_grid_max):
                    self.path_list.append([x, y])


