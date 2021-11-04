from plot import plot_graph
from myio import getMatrix, printMatrix
from muls import defaultMatrixMul, vinMatrixMul, optimizedVinMatrixMul


def menu() -> None:
    print("\n_____________Меню_____________\n")
    print("Выбрать действие:")
    print("1. Протестировать умножение матриц")
    print("2. Рассчитать сложность алгоритмов умножения матриц")
    print("0. Выход\n")


def menu_loop() -> None:
    while True:
        menu()
        action = input("Введите действие: ")

        if action == "0":
            break

        elif action == "1":
            left_matrix = getMatrix()
            right_matrix = getMatrix()

            print("\nОбычное умножение:")
            printMatrix(defaultMatrixMul(left_matrix, right_matrix))
            print("Алгоритм Винограда:")
            printMatrix(vinMatrixMul(left_matrix, right_matrix))
            print("Алгоритм Винограда с оптимизациями:")
            printMatrix(optimizedVinMatrixMul(left_matrix, right_matrix))

        elif action == "2":
            temp = input("Введите массив размеров (через пробел): ").split()
            try:
                a = [int(i) for i in temp]
            except:
                print("Массив размеров должен состоять из чисел типа int")
                continue

            plot_graph(
                [defaultMatrixMul, vinMatrixMul, optimizedVinMatrixMul],
                a,
            )

        else:
            print("Неправильный пункт меню")