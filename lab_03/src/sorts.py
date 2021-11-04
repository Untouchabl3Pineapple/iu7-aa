"""
Sorting to evaluate the complexity of sorting
! A copy of the array is returned, the original array is not touched
"""


def bubble(a: list) -> list:
    l = len(a)
    ret_a = a.copy()

    for i in range(l - 1):
        for j in range(i + 1, l):
            if ret_a[i] > ret_a[j]:
                ret_a[i], ret_a[j] = ret_a[j], ret_a[i]

    return ret_a


def selection(a: list) -> list:
    l = len(a)
    ret_a = a.copy()

    for i in range(l):
        minIdx = i

        for j in range(i, l):
            if ret_a[j] < ret_a[minIdx]:
                minIdx = j

        ret_a[minIdx], ret_a[i] = ret_a[i], ret_a[minIdx]

    return ret_a


def insertion(a: list) -> list:
    l = len(a)
    ret_a = a.copy()

    for i in range(l):
        x = ret_a[i]
        j = i

        while j > 0 and ret_a[j - 1] > x:
            ret_a[j] = ret_a[j - 1]
            j -= 1

        ret_a[j] = x

    return ret_a