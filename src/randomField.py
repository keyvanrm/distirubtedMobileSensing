import math
import random
import scipy.sparse.linalg
import scipy.sparse as sparse
import numpy as np
import matplotlib.pyplot as plt

class RandomField:

    indep_thr = 5  #Farther than this will have zero dependency
    scale = 1   #The cell dependency will scale by this factor

    def __init__(self, x_grid, y_grid):
        self.x_grid_max = x_grid
        self.y_grid_max = y_grid
        self.grid_max = x_grid * y_grid
        self.c = [[0 for i in range(self.grid_max)] for j in range(self.grid_max)]
        self.cov_mat = [[0 for i in range(self.grid_max)] for j in range(self.grid_max)]

    def generate_field_structure(self):
        for k in range(self.grid_max):
            temp = 0
            for l in range(k, self.grid_max):
                i1 = k % self.x_grid_max
                i2 = l % self.x_grid_max
                j1 = math.trunc(k / self.x_grid_max)
                j2 = math.trunc(l / self.x_grid_max)
                distance = math.sqrt((i1-i2)**2 + (j1-j2)**2)
                if distance > RandomField.indep_thr or distance == 0.0:
                    self.c[k][l] = 0.0
                    self.c[l][k] = 0.0
                else:
                    self.c[k][l] = -math.sqrt(1.0/distance)*(random.random()+0.5)
                    self.c[l][k] = self.c[k][l]

        for i in range(self.grid_max):
            temp = 0
            for j in range(self.grid_max):
                temp += abs(self.c[i][j])
            self.c[i][i] = temp + 0.1#random.random()
        (s, logdet) = np.linalg.slogdet(self.c)
        print logdet

    def save_field_structure(self):
        my_file = open("./c_structure.txt", 'w')
        for line in self.c:
            for element in line:
                my_file.write("%.4f " % element)
            my_file.write("\n")
        my_file.close()

    def load_field_structure(self):
        my_file = open("./c_structure.txt", 'r')
        self.c = [map(float, line.split()) for line in my_file]

    def generate_covariance(self):
        c_array = np.array(self.c)
        c_sparse = sparse.csc_matrix(c_array)
        self.cov_mat = scipy.sparse.linalg.inv(c_sparse)
        self.save_sparse_csc("covariance_mat_50_30", self.cov_mat)
        self.field_mean = np.random.uniform(0.5, 2, self.grid_max) #generate a random mean for the field
        np.save("field_mean_50_30", self.field_mean)

    def generate_samples(self):
        self.cov_mat = self.load_sparse_csc("covariance_mat_50_30.npz")
        c = scipy.sparse.linalg.inv(self.cov_mat).todense()
        print np.linalg.det(c)
        self.cov_mat_dense = self.cov_mat.todense()
        self.field_mean = np.load("field_mean_50_30.npy")
        print scipy.linalg.det(self.cov_mat_dense)
        self.field_realization = np.random.multivariate_normal(self.field_mean, self.cov_mat_dense)
        # np.save("field_realization_50_30", self.field_realization)

    def realization_heat_map(self):
        field_realization = np.load('field_realization_50_30.npy')
        field_realization = field_realization.reshape(30, 50)
        fig = plt.figure(figsize=(10, 6))

        ax = fig.add_subplot(111)
        ax.set_title('Field Realization Color Map')
        plt.imshow(field_realization)
        ax.set_aspect('equal')

        cax = fig.add_axes([0.15, 0.11, 0.9, 0.77])
        cax.get_xaxis().set_visible(False)
        cax.get_yaxis().set_visible(False)
        cax.patch.set_alpha(0)
        cax.set_frame_on(False)
        plt.colorbar(orientation='vertical')
        # plt.show()
        plt.savefig('heatmap.pdf', bbox_inches='tight')

    def save_sparse_csc(self, filename, array):
        np.savez(filename, data=array.data, indices=array.indices,
                 indptr=array.indptr, shape=array.shape)

    @staticmethod
    def load_sparse_csc(filename):
        loader = np.load(filename)
        return sparse.csc_matrix((loader['data'],
                                  loader['indices'], loader['indptr']), shape=loader['shape'])


