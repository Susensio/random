# Develop a program that has the user enter a number and find all the Primer Factors (if there are any) and display them.
# ---------------- COMPLETED ----------------


import math


def prime_factors(number):
    return []


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


if __name__ == "__main__":
    print(primes_upto(100))
