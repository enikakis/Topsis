import numpy as np

# This class emplements the Topsis and Group-Topsis Method


class Topsis:
    euclidean_dist_best = []
    euclidean_dist_worst = []
    performance_score = []
    __nrml_dec_matrix = []
# For group topsis to work:
# group_topsis_mode=true and weight_array must have at least 2 dimensions

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
        self.performance_score = self.topsis_group_method(
            self.euclidean_dist_best, self.euclidean_dist_worst)
# group topsis function

    def topsis_group_method(self, my_dist_best, my_dist_worst):
        length = len(my_dist_best)
        dist_best = np.array(my_dist_best, dtype=float)
        dist_worst = np.array(my_dist_worst, dtype=float)
        gr_pos = np.zeros(len(dist_best[0]))
        gr_neg = np.zeros(len(dist_best[0]))
        elements = len(dist_best[0])
        dms = length
        for i in range(elements):
            pos = 1
            neg = 1
            for a in range(dms):
                pos = pos * dist_best[a][i]
                neg = neg * dist_worst[a][i]

            gr_pos[i] = pow(pos, 1/dms)
            gr_neg[i] = pow(neg, 1/dms)
        return (gr_neg) / (
            gr_pos + gr_neg)

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
