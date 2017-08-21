# Develop a program that has the user enter a number.
# Your program should print out Pi up to that many decimal places.
# Try to keep a limit as to how far the program will go.
import random
from math import sqrt
from timer_decorator import timeit
import math


@timeit
def calculate_pi(decimal):
    decimal = 10.0**-int(decimal)
    pi_gen = pi_generator()
    pi_prev = next(pi_gen)
    pi_now = next(pi_gen)
    while pi_prev//decimal != pi_now//decimal:
        pi_prev, pi_now = pi_now, next(pi_gen)
    return pi_now


def polygon(steps):
    sides = 2 ** (steps + 1)
    side_squared = 2
    for _ in range(steps - 1):
        print(4 - side_squared)
        side_squared = 2 - sqrt(4 - side_squared)
        print(side_squared)
    return sides * sqrt(side_squared) / 2


def montecarlo(points):
    darts = []
    for _ in range(points):
        darts.append((random.uniform(-1, 1), random.uniform(-1, 1)))
    pi = 4 * len([_ for (x, y) in darts if sqrt(x**2 + y**2) < 1]) / len(darts)
    return pi


@timeit
def series(components):
    result = 0
    for natural in range(components):
        result += 1 / (natural + 1)**2
    return sqrt(6 * result)


# Gregory-Leibniz formula
@timeit
def series_odd(components):
    pi = 0
    for natural in range(components):
        if natural % 2:
            pi -= 4 / (1 + natural * 2)
        else:
            pi += 4 / (1 + natural * 2)
    return pi


def pi_generator():
    pi = 0
    natural = 0
    while True:
        if natural % 2:
            pi -= 4 / (1 + natural * 2)
        else:
            pi += 4 / (1 + natural * 2)
        yield pi
        natural += 1


print(calculate_pi(input("Decimal places of Pi to calculate: ")))

# print("polygon: {}".format(polygon(20)))
# print("montecarlo: {}".format(montecarlo(100000)))
# print("series: {}".format(series(1000000)))
# print("series_odd: {}".format(series_odd(1000000)))

# print("series: {}".format(series(1000000) - math.pi))
# print("series_odd: {}".format(series_odd(1000000) - math.pi))
