def recLevenshtain(left_str: str, right_str: str) -> int:
    if left_str == "" or right_str == "":
        return abs(len(left_str) - len(right_str))

    if left_str[-1] == right_str[-1]:
        c = 0
    else:
        c = 1

    return min(
        recLevenshtain(left_str, right_str[:-1]) + 1,
        recLevenshtain(left_str[:-1], right_str) + 1,
        recLevenshtain(left_str[:-1], right_str[:-1]) + c,
    )


def cacheLevenshtain(left_str: str, right_str: str) -> int:
    left_str_len = len(left_str) + 1
    right_str_len = len(right_str) + 1
    matrix = [[i + j for j in range(right_str_len)] for i in range(left_str_len)]

    for i in range(1, left_str_len):
        for j in range(1, right_str_len):
            if left_str[i - 1] == right_str[j - 1]:
                c = 0
            else:
                c = 1

            matrix[i][j] = min(
                matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + c
            )

    return matrix[-1][-1]


def recDamerayLevenshtain(left_str: str, right_str: str) -> int:
    if left_str == "" or right_str == "":
        return abs(len(left_str) - len(right_str))
        
    if left_str[-1] == right_str[-1]:
        c = 0
    else:
        c = 1

    result = min(
        recDamerayLevenshtain(left_str, right_str[:-1]) + 1,
        recDamerayLevenshtain(left_str[:-1], right_str) + 1,
        recDamerayLevenshtain(left_str[:-1], right_str[:-1]) + c,
    )

    if (
        len(left_str) >= 2
        and len(right_str) >= 2
        and left_str[-1] == right_str[-2]
        and left_str[-2] == right_str[-1]
    ):
        result = min(result, recDamerayLevenshtain(left_str[:-2], right_str[:-2]) + 1)

    return result


def cacheDamerayLevenshtain(left_str: str, right_str: str) -> int:
    left_str_len = len(left_str) + 1
    right_str_len = len(right_str) + 1
    matrix = [[i + j for j in range(right_str_len)] for i in range(left_str_len)]

    for i in range(1, left_str_len):
        for j in range(1, right_str_len):
            if left_str[i - 1] == right_str[j - 1]:
                c = 0
            else:
                c = 1

            matrix[i][j] = min(
                matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + c
            )

            if (
                (i > 1 and j > 1)
                and left_str[i - 1] == right_str[j - 2]
                and left_str[i - 2] == right_str[j - 1]
            ):
                matrix[i][j] = min(matrix[i][j], matrix[i - 2][j - 2] + 1)

    return matrix[-1][-1]
