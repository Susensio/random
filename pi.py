# Develop a program that has the user enter a number.
# Your program should print out Pi up to that many decimal places.
# Try to keep a limit as to how far the program will go.
import random
from math import sqrt


def calculate_pi(decimal):
    pass


def polygon(steps):
    sides = 2 ** (steps + 1)
    side_squared = 2
    for _ in range(steps - 1):
        side_squared = 2 - sqrt(4 - side_squared)
    return sides * sqrt(side_squared) / 2


def montecarlo(points):
    darts = []
    for _ in range(points):
        darts.append((random.uniform(-1, 1), random.uniform(-1, 1)))
    pi = 4 * len([_ for (x, y) in darts if sqrt(x**2 + y**2) < 1]) / len(darts)
    return pi


def series(components):
    result = 0
    for natural in range(components):
        result += 1 / (natural + 1)**2
    return sqrt(6 * result)


# Gregory-Leibniz series
def series_odd(components):
    pi = 0
    for natural in range(components):
        if natural % 2:
            pi -= 4 / (1 + natural * 2)
        else:
            pi += 4 / (1 + natural * 2)
    return pi


# print(calculate_pi(input("Decimal places of Pi to calculate: ")))
print(polygon(20))
print(montecarlo(100000))
print(series(100000))
print(series_odd(1000000))
