import math


def floor_n(x: float, n: int):
    n = 10 ** n
    return math.floor(x * n) / n
