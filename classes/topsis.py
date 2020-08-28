import numpy as np


class Topsis:
    euclidean_dist_best = []
    euclidean_dist_worst = []
    performance_score = []
    __nrml_dec_matrix = []

    def __init__(self, value_matrix, weight_array, better_max, group_topsis_mode=False):
        value_matrix = np.array(value_matrix, dtype=float)
        weight_array = np.array(weight_array, dtype=float)
        if group_topsis_mode == False:
            self.__topsis_method(value_matrix, weight_array, better_max)
        else:
            self.__group_topsis(value_matrix, weight_array, better_max)

    def __group_topsis(self, matrix, weight_array, better_max):
        for i in range(len(weight_array)):
            self.__topsis_method(
                matrix, weight_array[i], better_max)
        length = len(self.euclidean_dist_best)
        print(self.euclidean_dist_best)
        print(length)
        gr_pos = np.zeros(len(self.euclidean_dist_best[0]))
        gr_neg = np.zeros(len(self.euclidean_dist_best[0]))
        for i in range(len(self.euclidean_dist_best[0])):
            pos = 1
            neg = 1
            for a in range(length):
                pos = pos * self.euclidean_dist_best[a][i]
                neg = neg * self.euclidean_dist_worst[a][i]

            gr_pos[i] = pow(pos, 1/length)
            gr_neg[i] = pow(neg, 1 / length)
        print(gr_pos, gr_neg)
        self.performance_score = self.__get_performance_score(gr_pos, gr_neg)

    def __topsis_method(self, value_matrix, weight_array, better_max):
        if self.__nrml_dec_matrix == []:
            self.__nrml_dec_matrix = self.__get_normalize_dec_matrix(
                value_matrix)
        wght_nrml_dec_matrix = self.__get_weighted_normalize_dec_matrix(
            self.__nrml_dec_matrix, weight_array)
        ideal_best_and_worst = self.__get_ideal_best_and_worst(
            wght_nrml_dec_matrix, better_max)
        ideal_best = ideal_best_and_worst[0]
        ideal_worst = ideal_best_and_worst[1]
        euclidean_dist_best = self.__get_euclidean_distances(
            wght_nrml_dec_matrix, ideal_best)
        euclidean_dist_worst = self.__get_euclidean_distances(
            wght_nrml_dec_matrix, ideal_worst)
        performance_score = self.__get_performance_score(
            euclidean_dist_best, euclidean_dist_worst)
        if self.euclidean_dist_best == []:
            self.euclidean_dist_best = [0]
            self.euclidean_dist_worst = [0]
            self.euclidean_dist_best[0] = euclidean_dist_best
            self.euclidean_dist_worst[0] = euclidean_dist_worst
            self.performance_score = performance_score
        else:
            self.euclidean_dist_worst.append(euclidean_dist_worst)
            self.euclidean_dist_best.append(euclidean_dist_best)

    def __get_normalize_dec_matrix(self, matrix):
        power_matrix = np.power(matrix, 2)
        sum_array = np.sum(power_matrix, axis=0)
        sqrt_array = np.sqrt(sum_array)
        return matrix / sqrt_array

    def __get_weighted_normalize_dec_matrix(self, nrml_dec_matrix, weight_array):
        return nrml_dec_matrix * weight_array

    def __get_ideal_best_and_worst(self, weight_nrml_dec_matrix, better_max):
        max_array = weight_nrml_dec_matrix.max(0)
        min_array = weight_nrml_dec_matrix.min(0)
        for i in range(len(better_max)):
            if better_max[i] == False:
                value = max_array[i]
                max_array[i] = min_array[i]
                min_array[i] = value
        return [max_array, min_array]

    def __get_euclidean_distances(self, matrix, ideal_array):
        value = matrix - ideal_array
        power_value = np.power(value, 2)
        sum_value = np.sum(power_value, axis=(1))
        sqrt_value = np.sqrt(sum_value)
        return sqrt_value

    def __get_performance_score(self, euclidean_dist_best, euclidean_dist_worst):
        return (euclidean_dist_worst) / (
            euclidean_dist_best + euclidean_dist_worst)

    # get index values to help me with sort
    def get_sort_indexes(self):
        array = np.array([])
        sort_array = -np.sort(-self.performance_score)
        for i in range(len(sort_array)):
            a = np.where(self.performance_score == sort_array[i])
            if len(a[0]) == 1:
                array = np.append(array, a[0])
            else:
                a = a[0]
                array = np.append(array, a[0])
        return array
