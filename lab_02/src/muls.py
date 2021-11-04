def defaultMatrixMul(left_matrix: list, right_matrix: list) -> list:
    if len(left_matrix) == 0 or len(right_matrix) == 0:
        print("Матрицы пустые")
    elif len(left_matrix[0]) != len(right_matrix):
        print("Матрицы не могут быть перемножены")
    else:
        res_matrix = [
            [0 for _ in range(len(right_matrix[i]))] for i in \
            range(len(left_matrix))
        ]

        for i in range(len(left_matrix)):
            for j in range(len(right_matrix[i])):
                for k in range(len(left_matrix[i])):
                    res_matrix[i][j] += left_matrix[i][k] * \
                                        right_matrix[k][j]

        return res_matrix
    return


def vinMatrixMul(left_matrix: list, right_matrix: list) -> list:
    if len(left_matrix) == 0 or len(right_matrix) == 0:
        print("Матрицы пустые")
    elif len(left_matrix[0]) != len(right_matrix):
        print("Матрицы не могут быть перемножены")
    else:
        left_matrix_rows = len(left_matrix)
        left_matrix_columns = len(left_matrix[0])
        right_matrix_columns = len(right_matrix[0])

        res_matrix = [
            [0 for _ in range(right_matrix_columns)] for _ in \
                                      range(left_matrix_rows)
        ]

        row_factor = [0 for _ in range(left_matrix_rows)]
        for i in range(left_matrix_rows):
            for j in range(left_matrix_columns // 2):
                row_factor[i] += left_matrix[i][2 * j] * \
                                 left_matrix[i][2 * j + 1]

        column_factor = [0 for _ in range(right_matrix_columns)]
        for i in range(right_matrix_columns):
            for j in range(left_matrix_columns // 2):
                column_factor[i] += right_matrix[2 * j][i] * \
                                    right_matrix[2 * j + 1][i]

        for i in range(left_matrix_rows):
            for j in range(right_matrix_columns):
                res_matrix[i][j] = -row_factor[i] - column_factor[j]
                for u in range(left_matrix_columns // 2):
                    res_matrix[i][j] += (
                        left_matrix[i][2 * u + 1] + right_matrix[2 * u][j]
                    ) * (left_matrix[i][2 * u] + \
                        right_matrix[2 * u + 1][j])

        if left_matrix_columns % 2 == 1:
            for i in range(left_matrix_rows):
                for j in range(right_matrix_columns):
                    res_matrix[i][j] += (
                        left_matrix[i][left_matrix_columns - 1]
                        * right_matrix[left_matrix_columns - 1][j]
                    )

        return res_matrix
    return


def optimizedVinMatrixMul(left_matrix: list, right_matrix: list) -> list:
    if len(left_matrix) == 0 or len(right_matrix) == 0:
        print("Матрицы пустые")
    elif len(left_matrix[0]) != len(right_matrix):
        print("Матрицы не могут быть перемножены")
    else:
        left_matrix_rows = len(left_matrix)
        left_matrix_columns = len(left_matrix[0])
        right_matrix_columns = len(right_matrix[0])

        res_matrix = [
            [0 for _ in range(right_matrix_columns)] for _ in \
                                        range(left_matrix_rows)
        ]

        row_factor = [0 for _ in range(left_matrix_rows)]
        for i in range(left_matrix_rows):
            for j in range(1, left_matrix_columns, 2):
                row_factor[i] += left_matrix[i][j] * left_matrix[i][j - 1]

        column_factor = [0 for _ in range(right_matrix_columns)]
        for i in range(right_matrix_columns):
            for j in range(1, left_matrix_columns, 2):
                column_factor[i] += right_matrix[j][i] * \
                                    right_matrix[j - 1][i]

        flag = left_matrix_rows % 2
        for i in range(left_matrix_rows):
            for j in range(right_matrix_columns):
                res_matrix[i][j] = -(row_factor[i] + column_factor[j])
                for u in range(1, left_matrix_columns, 2):
                    res_matrix[i][j] += (left_matrix[i][u - 1] + \
                                           right_matrix[u][j]) * (
                        left_matrix[i][u] + right_matrix[u - 1][j]
                    )
                if flag:
                    res_matrix[i][j] += (
                        left_matrix[i][left_matrix_columns - 1]
                        * right_matrix[left_matrix_columns - 1][j]
                    )

        return res_matrix
    return