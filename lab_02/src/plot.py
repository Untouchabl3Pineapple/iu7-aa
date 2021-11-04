import time
import matplotlib.pyplot as plt
from typing import Callable

from myio import getRandomMatrix


def benchmark(mul_func: Callable, sizes: list) -> list:
    res_times = []
    temp_times = []
    const_measures = 2

    for i in range(len(sizes)):
        left_matrix = getRandomMatrix(sizes[i], sizes[i])
        right_matrix = getRandomMatrix(sizes[i], sizes[i])
        for j in range(const_measures):
            start_time = time.time()
            mul_func(left_matrix, right_matrix)
            end_time = time.time() - start_time

            temp_times.append(end_time)

        res_times.append(sum(temp_times) / const_measures)
        temp_times.clear()

    print(res_times)

    return res_times


def plot_graph(mul_funcs: list, sizes: list) -> None:
    # General settings
    plt.title("Сложность алгоритмов умножения матриц")
    plt.xlabel("Размер")
    plt.ylabel("Время, сек")
    plt.grid()

    # Collecting values
    for mul_func in mul_funcs:
        times = benchmark(mul_func, sizes)
        mul_name = str(mul_func).split()[1]
        if mul_name == "defaultMatrixMul":
            mul_name = "Простой"
        elif mul_name == "vinMatrixMul":
            mul_name = "Виноград"
        elif mul_name == "optimizedVinMatrixMul":
            mul_name = "Виноград с оптимизациями"
        plt.plot(sizes, times, label=mul_name)

    # Image of the results obtained
    plt.legend()
    plt.show()