import math


def floor_n(x: float, n: int):
    n = 10 ** n
    return math.floor(x * n) / n


def subtract_nth_decimal(x: float, n: int):
    return floor_n(x - 10 ** -n, n)
