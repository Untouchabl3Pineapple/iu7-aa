import time
import matplotlib.pyplot as plt
from typing import Callable


def benchmark(
    sort_func: Callable, form_func: Callable, sizes: list, start_pos: int, end_pos: int
) -> list:
    res_times = []
    temp_times = []
    const_measures = 30

    for i in range(len(sizes)):
        arr = form_func(sizes[i], start_pos, end_pos)
        for j in range(const_measures):
            start_time = time.time()
            sort_func(arr)
            end_time = time.time() - start_time

            temp_times.append(end_time)

        res_times.append(sum(temp_times) / const_measures)
        temp_times.clear()
    
    print(res_times)

    return res_times


def plot_graph(
    sort_funcs: list, form_func: Callable, sizes: list, start_pos=-1000, end_pos=1000
) -> None:
    # General settings
    plt.title("Сложность сортировок")
    plt.xlabel("Размер")
    plt.ylabel("Время, сек")
    plt.grid()

    # Collecting values
    for sort_func in sort_funcs:
        times = benchmark(sort_func, form_func, sizes, start_pos, end_pos)
        sort_name = str(sort_func).split()[1]
        if sort_name == "bubble": sort_name = "Пузырьком"
        elif sort_name == "insertion": sort_name = "Вставками"
        elif sort_name == "selection": sort_name = "Выбором"
        plt.plot(sizes, times, label=sort_name)

    # Image of the results obtained
    plt.legend()
    plt.show()