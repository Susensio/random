# Develop a program that has the user enter a number and find all the Primer Factors (if there are any) and display them.
# ---------------- COMPLETED ----------------


import math
from timer_decorator import timeit


def prime_factors(number):
    return []


@timeit
def primes_upto(number):
    primes = []
    for n in range(number):
        if is_prime(int(n + 1)):
            primes.append(n + 1)

    return primes


def factors(number):
    min = 2
    max = int(math.sqrt(number))
    factors = set()
    while min <= max:
        if not number % min:
            factors.update([min, number // min])
        min += 1

    return sorted(factors)


def is_prime(number):
    return not factors(number)


# Algorithm for finding all prime numbers up to any diven limit
@timeit
def sieve_of_eratosthenes(ceil):
    primes = range(2, ceil)
    for prime in primes:
        # print(primes)
        primes = [number for number in primes if (number % prime) or (number == prime)]
    return primes


if __name__ == "__main__":
    print(primes_upto(1000))
    print(sieve_of_eratosthenes(1000))
