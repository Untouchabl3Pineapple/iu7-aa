import time
import matplotlib.pyplot as plt
from typing import Callable

from myio import getRandomString


def benchmark(edit_dist_func: Callable, sizes: list) -> list:
    res_times = []
    temp_times = []
    const_measures = 10

    for i in range(len(sizes)):
        left_string = getRandomString(sizes[i])
        right_string = getRandomString(sizes[i])
        for j in range(const_measures):
            start_time = time.time()
            edit_dist_func(left_string, right_string)
            end_time = time.time() - start_time

            temp_times.append(end_time)

        res_times.append(sum(temp_times) / const_measures)
        temp_times.clear()

    print(res_times)

    return res_times


def plot_graph(edit_dist_funcs: list, sizes: list) -> None:
    # General settings
    plt.title("Сложность алгоритмов нахождения редакционного расстояния")
    plt.xlabel("Размер")
    plt.ylabel("Время, сек")
    plt.grid()

    # Collecting values
    for edit_dist_func in edit_dist_funcs:
        times = benchmark(edit_dist_func, sizes)
        edit_dist_name = str(edit_dist_func).split()[1]
        if edit_dist_name == "recLevenshtain":
            edit_dist_name = "Рекурсивный Левенштейн"
        elif edit_dist_name == "cacheLevenshtain":
            edit_dist_name = "Кэшированный Левенштейн"
        elif edit_dist_name == "recDamerayLevenshtain":
            edit_dist_name = "Рекурсивный Дамерау — Левенштейн"
        elif edit_dist_name == "cacheDamerayLevenshtain":
            edit_dist_name = "Кешированный Дамерау — Левенштейн"
        plt.plot(sizes, times, label=edit_dist_name)

    # Image of the results obtained
    plt.legend()
    plt.show()