from plot import plot_graph
from edit_dist import (
    recLevenshtain,
    cacheLevenshtain,
    recDamerayLevenshtain,
    cacheDamerayLevenshtain,
)


def menu() -> None:
    print("\n_____________Меню_____________\n")
    print("Выбрать действие:")
    print("1. Протестировать нахождение редакционного расстояния")
    print(
        "2. Рассчитать сложность кэшируемых алгоритмов Левенштейна и Дамерау — Левенштейна"
    )
    print(
        "3. Рассчитать сложность алгоритмов рекурсивного и кэшируемого Левенштейна"
    )
    print("0. Выход\n")


def menu_loop() -> None:
    while True:
        menu()
        action = input("Введите действие: ")

        if action == "0":
            break

        elif action == "1":
            left_string = input("Введите левую строку: ")
            right_string = input("Введите правую строку: ")

            print(
                "\nРекурсиный алгоритм Левенштейна:",
                recLevenshtain(left_string, right_string),
            )
            print(
                "Кэшированный алгоритм Левенштейна:",
                cacheLevenshtain(left_string, right_string),
            )

            print(
                "Рекурсиный алгоритм Дамерау — Левенштейна:",
                recDamerayLevenshtain(left_string, right_string),
            )
            print(
                "Кэшированный алгоритм Дамерау — Левенштейна:",
                cacheDamerayLevenshtain(left_string, right_string),
            )
        elif action == "2":
            temp = input("Введите массив размеров (через пробел): ").split()
            try:
                sizes = [int(i) for i in temp]
            except:
                print("Массив размеров должен состоять из чисел типа int")
                continue

            plot_graph([cacheLevenshtain, cacheDamerayLevenshtain], sizes)

        elif action == "3":
            temp = input("Введите массив размеров (через пробел): ").split()
            try:
                sizes = [int(i) for i in temp]
            except:
                print("Массив размеров должен состоять из чисел типа int")
                continue

            plot_graph([recLevenshtain, cacheLevenshtain], sizes)
        else:
            print("Неправильный пункт меню")