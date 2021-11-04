from plot import plot_graph
from list_form import get_random_list, get_sorted_list, get_back_sorted_list
import sorts


def menu() -> None:
    print("\n_____________Меню_____________\n")
    print("Выбрать действие:")
    print("1. Протестировать сортировки")
    print("2. Рассчитать сложность сортировки с рандомными значениями")
    print("3. Рассчитать сложность сортировки с отсортированными значениями")
    print("4. Рассчитать сложность сортировки с обратно отсортированными значениями")
    print("0. Выход\n")


def menu_loop() -> None:
    while True:
        menu()
        action = input("Введите действие: ")

        if action == "0":
            break

        elif action == "1":
            temp = input("Введите массив значений (через пробел): ").split()
            try:
                a = [int(i) for i in temp]
            except:
                print("The array must consist of integers")
                continue

            print("Bubble sort:    ", sorts.bubble(a))
            print("Selection sort: ", sorts.selection(a))
            print("Insertion Sort: ", sorts.insertion(a))

        elif action == "2" or action == "3" or action == "4":
            temp = input("Введите массив размеров (через пробел): ").split()
            try:
                a = [int(i) for i in temp]
            except:
                print("Массив размеров должен состоять из чисел типа int")
                continue

            if action == "2":
                start_pos = int(input("Введите левую границу интервала значений: "))
                end_pos = int(input("Введите правую границу интервала значений: "))

                plot_graph(
                    [sorts.bubble, sorts.insertion, sorts.selection],
                    get_random_list,
                    a,
                    start_pos,
                    end_pos,
                )

            elif action == "3":
                plot_graph(
                    [sorts.bubble, sorts.insertion, sorts.selection],
                    get_sorted_list,
                    a,
                )

            elif action == "4":
                plot_graph(
                    [sorts.bubble, sorts.insertion, sorts.selection],
                    get_back_sorted_list,
                    a,
                )

        else:
            print("Неправильный пункт меню")