from classes.topsis import Topsis
import numpy as np
import eel

# main start app


def main():
    eel.init("ui")
    eel.start("index.html")

# function comunicate with the ui
@eel.expose
def topsis_capulate(matrix, weight, better_max, group):
    top = Topsis(matrix, weight, better_max, group)
    sortNumbers = top.get_sort_indexes()
    print(sortNumbers)
    return top.performance_score.tolist(), sortNumbers.tolist()


if __name__ == '__main__':
    main()
