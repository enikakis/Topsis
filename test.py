from classes.topsis import Topsis
import numpy as np

# above are some tests to see if topsis and group topsis method works correctly

# test values for the tospis method
value_matrix = [[250, 16, 12, 5], [200, 16, 8, 3],
                [300, 32, 16, 4], [275, 32, 8, 4], [225, 16, 16, 2]]
weight_array = [0.25, 0.25, 0.25, 0.25]
better_max = [False, True, True, True]
euclirian_best_group = [[61.93852,
                         65.51017,
                         71.43093,
                         63.07548,
                         95.25852
                         ], [93.70986,
                             113.24435,
                             95.34438,
                             95.83915,
                             64.17273], [95.07816,
                                         104.09410,
                                         97.03846,
                                         94.62981,
                                         58.77063
                                         ]]
euclirian_worst_group = [[79.43579,
                          76.60597,
                          71.05542,
                          78.62259,
                          32.76913
                          ], [73.18474,
                              36.75669,
                              71.28725,
                              70.64053,
                              100.26446
                              ], [56.03748,
                                  37.02839,
                                  52.71964,
                                  57.02503,
                                  93.47633
                                  ]]

# Correct result values
result_values_topsis = np.array([0.53427686, 0.30836777,
                                 0.69163223, 0.53473658, 0.40104612], dtype=float)
result_values_group_topsis = np.array(
    [0.45618862, 0.33906669, 0.42505495, 0.4508903,  0.48693559], dtype=float)

# The test


def test():
    print("topsis method test starts")
    my_topsis = Topsis(value_matrix, weight_array, better_max)
    if my_topsis.performance_score.all() == result_values_topsis.all():
        print("Topsis method works fine!")
    else:
        print("Wrond in the method!")
    print("----------")
    print("Check-GroupTopsis")
    results = my_topsis.topsis_group_method(
        euclirian_best_group, euclirian_worst_group)
    if results.all() == result_values_group_topsis.all():
        print("Group Topsis method works fine!")
    else:
        print("Wrond in the Group Topsis method!")


test()
