from random import randint


def getMatrix() -> list:
    rows = int(input("Введите количество строк матрицы: "))
    columns = int(input("Введите количество столбцов матрицы: "))

    if rows < 1 or columns < 1:
        print("Неверные значения строк и столбцов")
        return

    print("Введите строки матрицы через пробел:")
    matrix = [input().split() for i in range(rows)]
    matrix = [[int(matrix[i][j]) for j in range(columns)] for i in range(rows)]

    if len(matrix) == rows:
        for row in matrix:
            if len(row) != columns:
                print("Матрица задана неверно")
                return
    else:
        return

    return matrix


def getRandomMatrix(rows: int, columns: int) -> list:
    if rows < 1 or columns < 1:
        print("Неверные значения строк и столбцов")
        return

    return [[randint(-100, 100) for j in range(columns)] for i in range(rows)]


def printMatrix(matrix: list) -> None:
    for row in matrix:
        for el in row:
            print("{:5d}".format(el), end=" ")
        print()
    print()