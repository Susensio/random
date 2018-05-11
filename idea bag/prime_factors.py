# Develop a program that has the user enter a number and find all
# the Primer Factors (if there are any) and display them.
# ---------------- COMPLETED ----------------

import sys
sys.path.append("../")
from timer_decorator import timeit


def prime_factors(number):
    primes_list = sieve_of_eratosthenes(number // 2)
    return [n for n in factors(number) if n in primes_list]


# @timeit
def primes_upto(number):
    primes = []
    for n in range(number):
        if is_prime(int(n + 1)):
            primes.append(n + 1)
    return tuple(primes)


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


def factors(number):
    factors = []
    [factors.extend((factor, number // factor))
        for factor in range(2, int(number**0.5) + 1)
        if not number % factor]
    return tuple(sorted(set(factors)))


def factors_slow(number):
    min = 2
    max = int(number**0.5) + 1
    factors = set()
    while min <= max:
        if not number % min:
            factors.update([min, number // min])
        min += 1
    return tuple(sorted(factors))


def factors_stackoverflow(number):
    from functools import reduce
    return tuple(sorted(set(reduce(list.__add__,
                                   ([i, number // i]
                                    for i in range(2, int(number**0.5) + 1)
                                    if number % i == 0), []))))


@timeit
def is_prime_slow(number):
    return not factors(number)


# @timeit
def is_prime(number):
    if number <= 1:
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
        roof = int(number**0.5)
        factor = 5
        while factor <= roof:
            if not number % factor:
                return False
            if not number % (factor + 2):
                return False
            factor += 6
    return True


# Algorithm for finding all prime numbers up to any given limit
# VERY SLOW
@timeit
def sieve_of_eratosthenes_slow(ceil):
    primes = range(2, ceil + 1)
    for prime in primes:
        # print(list(primes))
        primes = [number for number in primes if (number % prime) or (number == prime)]
    return tuple(primes)


# Fast implementation of Sieve of Eratosthenes algorithm
# @timeit
def sieve_of_eratosthenes(ceil):
    primes = [True] * (ceil + 1)
    primes[0] = primes[1] = False
    for number in range(2, int(ceil**0.5) + 1):
        if primes[number]:
            multiple = number**2
            while multiple <= ceil:
                if primes[multiple]:
                    primes[multiple] = False
                multiple += number
    return tuple(prime for prime in range(ceil + 1) if primes[prime])


if __name__ == "__main__":
    # print(primes_upto(100))
    # print(sieve_of_eratosthenes_slow(100))
    # print(sieve_of_eratosthenes(100))
    primes_upto(10000)
    sieve_of_eratosthenes(10000)
    sieve_of_eratosthenes_slow(10000)
    # print(prime_factors(13195))

    # print(nth_prime(10001))

    # print(factors_slow(4))
    # print(factors(4))

    # from time import time
    # ts = time()
    # [factors(number) for number in range(1, 100000)]
    # te = time()
    # print("{}(): {} s\n".format("factors:", (te - ts)))
    # ts = time()
    # [factors_slow(number) for number in range(1, 100000)]
    # te = time()
    # print("{}(): {} s\n".format("factors_slow:", (te - ts)))

    # ts = time()
    # [factors_stackoverflow(number) for number in range(1, 100000)]
    # te = time()
    # print("{}(): {} s\n".format("factors_stackoverflow:", (te - ts)))
    pass
