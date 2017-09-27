# Develop a program that has the user enter a number and find all the Primer Factors (if there are any) and display them.
# ---------------- COMPLETED ----------------

import sys
sys.path.append("../")
import math
from timer_decorator import timeit


def prime_factors(number):
    primes_list = primes_upto(number // 2)
    return [n for n in factors(number) if n in primes_list]


@timeit
def primes_upto(number):
    primes = []
    for n in range(number):
        if is_prime(int(n + 1)):
            primes.append(n + 1)
    return primes


def nth_prime(n):
    primes = prime_generator()
    for _ in range(n):
        prime = next(primes)
    return prime


def prime_generator():
    number = 2
    while True:
        if is_prime(number):
            yield number
        number += 1


# @timeit
def factors(number):
    min = 2
    max = int(math.sqrt(number))
    factors = set()
    while min <= max:
        if not number % min:
            factors.update([min, number // min])
        min += 1

    return sorted(factors)


@timeit
def is_prime_slow(number):
    return not factors(number)


@timeit
def is_prime(number):
    if number == 1:
        return False
    elif number < 4:
        return True
    elif not number % 2:
        return False
    elif number < 9:
        return True
    elif not number % 3:
        return False
    else:
        roof = int(math.sqrt(number))
        factor = 5
        while factor <= roof:
            if not number % factor:
                return False
            if not number % (factor + 2):
                return False
            factor += 6
    return True


# Algorithm for finding all prime numbers up to any given limit
@timeit
def sieve_of_eratosthenes(ceil):
    primes = range(2, ceil)
    for prime in primes:
        # print(primes)
        primes = [number for number in primes if (number % prime) or (number == prime)]
    return primes


if __name__ == "__main__":
    # primes_upto(1000)
    # sieve_of_eratosthenes(1000)
    # print(prime_factors(13195))

    # print(nth_prime(10001))
