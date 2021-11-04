"""
Getting generated lists to evaluate the complexity of sorting
"""

from random import randint


def get_random_list(size: int, start_pos: int, end_pos: int) -> list:
    return [randint(start_pos, end_pos) for i in range(size)]


def get_sorted_list(size: int, *args: None) -> list:
    return [i for i in range(size)]


def get_back_sorted_list(size: int, *args: None) -> list:
    return [i for i in range(size, 0, -1)]