from time import time


def p31():
    """ Coin sums
    In England the currency is made up of pound, £, and pence, p, and there are eight coins
    in general circulation:

    1p, 2p, 5p, 10p, 20p, 50p, £1 (100p) and £2 (200p).
    It is possible to make £2 in the following way:

    1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p
    How many different ways can £2 be made using any number of coins?
    """
    quantity = 200
    # RECURSION => VERY SLOW for quantity > 200
    # import sys
    # sys.path.append("../chess/")
    # from util import memoize

    # coins = (200, 100, 50, 20, 10, 5, 2, 1)

    # @memoize
    # def change(amount, coins):
    #     if coins[0] == 1:
    #         return [[amount]]
    #     else:
    #         return [[count, *perm]
    #                 for count in range(amount // coins[0] + 1)
    #                 for perm in change(amount - count * coins[0], tuple(coins[1:]))]
    # return len(change(quantity, coins))

    # Try DINAMYC PROGRAMMING => WOW! 100x faster
    coins = (1, 2, 5, 10, 20, 50, 100, 200)
    combinations = [[0 for _ in range(8)] for _ in range(quantity + 1)]

    for amount in range(quantity + 1):
        for i, coin in enumerate(coins):
            if coin == 1:
                combinations[amount][i] = 1
            else:
                combinations[amount][i] = (sum([combinations[amount - count * coin][i - 1]
                                                for count in range(amount // coin)])
                                           + combinations[amount % coin][i - 1])
    # from pprint import pprint
    # pprint(combinations)

    return combinations[quantity][7]


def p32():
    """ Pandigital products
    We shall say that an n-digit number is pandigital if it makes use of all the digits 1
    to n exactly once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.
    The product 7254 is unusual, as the identity, 39 × 186 = 7254, containing multiplicand,
    multiplier, and product is 1 through 9 pandigital.

    Find the sum of all products whose multiplicand/multiplier/product identity can be written
    as a 1 through 9 pandigital.
    HINT: Some products can be obtained in more than one way so be sure to only include it once
    in your sum.
    """
    from itertools import permutations
    perms = permutations('123456789')
    products = []

    for perm in perms:
        m1 = int(perm[0])
        m2 = int(''.join(perm[1:5]))
        p = int(''.join(perm[5:]))
        if m1 * m2 == p:
            products.append((m1, m2, p))

        m1 = int(perm[0]) * 10 + int(perm[1])
        m2 = int(''.join(perm[2:5]))
        p = int(''.join(perm[5:]))
        if m1 * m2 == p:
            products.append((m1, m2, p))

    return sum(set(p[2] for p in products))


def p33():
    """ Digit cancelling fractions
    The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting
    to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by
    cancelling the 9s. We shall consider fractions like, 30/50 = 3/5, to be trivial examples.
    There are exactly four non-trivial examples of this type of fraction, less than one in value,
    and containing two digits in the numerator and denominator.

    If the product of these four fractions is given in its lowest common terms, find the value of 
    the denominator.
    """
    from functools import reduce

    fractions = []

    for cancel in range(1, 10):
        for num in range(1, 10):
            for den in range(num + 1, 10):
                div = num / den

                numerator = num * 10 + cancel
                denominator = cancel * 10 + den
                if numerator / denominator == div:
                    fractions.append((numerator, denominator))

                numerator = cancel * 10 + num
                denominator = den * 10 + cancel
                if numerator / denominator == div:
                    fractions.append((numerator, denominator))

    def gcd(a, b):
        """ Return the greatest common divisor of the given integers
        Euclidean algorithm 
        """
        if b == 0:
            return a
        else:
            return gcd(b, a % b)

    product = reduce(lambda x, y: (x[0] * y[0], x[1] * y[1]), fractions)
    product_simplified = list(map(lambda x: x // gcd(*product), product))

    return "Fraction: {numerator}/{denominator} = {num}/{den}\nDenominator: {den}".format(
        numerator=product[0],
        denominator=product[1],
        num=product_simplified[0],
        den=product_simplified[1])


def p34():
    """ Digit factorials
    145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.
    Find the sum of all numbers which are equal to the sum of the factorial of their digits.
    Note: as 1! = 1 and 2! = 2 are not sums they are not included.
    """
    from math import factorial

    n = 1
    while True:
        """ Upper bound: Solve inequation n*9! < 10^(n+1) ===> n > X """
        n += 0.1
        if n * factorial(9) < 10**(n + 1):
            break
    limit = int(10**(n + 1)) + 1

    def sum_fact_digits(number):
        return sum(factorial(int(number)) for number in str(number))

    numbers = [n for n in range(3, limit) if n == sum_fact_digits(n)]

    return "Numbers: {}\nSum: {}".format(numbers, sum(numbers))


def p35():
    """ Circular primes
    The number, 197, is called a circular prime because all rotations of the digits: 
    197, 971, and 719, are themselves prime.
    There are thirteen such primes below 100: 
    2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

    How many circular primes are there below one million?
    """
    import sys
    sys.path.append("../idea bag/")
    from prime_factors import is_prime

    def rotations(number):
        number = str(number)
        digits = len(number)
        return tuple(int(number[i:] + number[:i]) for i in range(digits))

    return len([None for number in range(1000000) if all(is_prime(n) for n in rotations(number))])


def p36():
    """ Double-base palindromes
    The decimal number, 585 = 10010010012 (binary), is palindromic in both bases.
    Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.
    (Please note that the palindromic number, in either base, may not include leading zeros.)
    """
    def is_palindromic(num):
        number = str(num)
        return all([number[index] == number[-1 - index] for index in range(0, len(number) // 2)])

    def is_binary_palindromic(num):
        number = '{0:b}'.format(num)
        return all([number[index] == number[-1 - index] for index in range(0, len(number) // 2)])

    def is_double_base_palindrome(num):
        return is_palindromic(num) and is_binary_palindromic(num)

    return sum(num for num in range(1000000) if is_double_base_palindrome(num))


def p37():
    """ Truncatable primes
    The number 3797 has an interesting property. Being prime itself, it is possible to continuously 
    remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. 
    Similarly we can work from right to left: 3797, 379, 37, and 3.
    Find the sum of the only eleven primes that are both truncatable from left to right and right 
    to left. NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
    """
    import sys
    sys.path.append("../idea bag/")
    from prime_factors import is_prime

    def truncatable_prime(number):
        if number < 10:
            return False
        number = str(number)
        length = len(number)
        for i in range(length):
            if not is_prime(int(number[i:])) or not is_prime(int(number[:length - i])):
                return False
        return True

    truncatables = []
    n = 11
    while len(truncatables) < 11:
        if truncatable_prime(n):
            truncatables.append(n)
        n += 2

    return "Truncatables: {}\nSum: {}".format(truncatables, sum(truncatables))


def p38():
    """ Pandigital multiples
    Take the number 192 and multiply it by each of 1, 2, and 3:

    192 × 1 = 192
    192 × 2 = 384
    192 × 3 = 576
    By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576
    the concatenated product of 192 and (1,2,3)

    The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the
    pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

    What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated
    product of an integer with (1,2, ... , n) where n > 1?
    """
    one_to_nine = {str(n) for n in range(1, 10)}

    def concatenated_product(number, factors):
        products = [number * factor for factor in factors]
        return int(''.join(str(digit) for digit in products))

    def is_pandigital(number):
        number = str(number)
        return len(number) == 9 and all(d in number for d in one_to_nine)

    max_pandigital = 0

    number = 1
    while True:
        n = 3

        while True:
            product = concatenated_product(number, range(1, n))
            if is_pandigital(product):
                if product > max_pandigital:
                    max_pandigital = product
            if product > (10 ** 10):
                break
            n += 1

        number += 1
        # Limit to half number of digits
        if number > (10**5):
            break

    return max_pandigital


def p39():
    """ Integer right triangles
    If p is the perimeter of a right angle triangle with integral length sides,
    {a,b,c}, there are exactly three solutions for p = 120.
    {20,48,52}, {24,45,51}, {30,40,50}
    For which value of p ≤ 1000, is the number of solutions maximised?
    """
    # # BRUTE FORCE very slow (84s!!!)
    # max_count = 0
    # max_value = 0
    # for p in range(1, 1001):
    #     count = 0
    #     for c in range(p // 2, p):
    #         for a in range(1, int(p * 2**-0.5)):
    #             if (p - c - a)**2 == c**2 - a**2:
    #                 count += 1
    #     if count > max_count:
    #         max_count = count
    #         max_value = p
    #     print(p, count)
    # return max_value, max_count

    # With Pythagorean triples
    from collections import Counter

    def pythagorean_triple_perimeter(m, n, k):
        # a = k*(m*m - n*n)
        # b = k*(2*m * n)
        # c = k*(m*m + n*n)
        # p = a+b+c = k*(2*m*m + 2*m*n)
        return k * (2 * m * m + 2 * m * n)

    def coprimes(a, b):
        def gcd(a, b):
            return a if b == 0 else gcd(b, a % b)

        return gcd(a, b) == 1

    cnt = Counter()

    m_max = int(500**0.5)  # 2*m*m < 1000

    for m in range(1, m_max + 1):
        for n in range(1, m):
            k = 1
            if coprimes(m, n) and not (m % 2 and n % 2):  # Not both odd
                while True:
                    p = pythagorean_triple_perimeter(m, n, k)
                    if p >= 1000:
                        break
                    cnt.update({p: 1})
                    k += 1

    return "p = {}\t\tsolutions = {}".format(*cnt.most_common(1)[0])


def p40():
    """ Champernowne's constant
    An irrational decimal fraction is created by concatenating the positive integers:
    0.12345678910'11'12131415161718192021...
    It can be seen that the 12th digit of the fractional part is 1.
    If dn represents the nth digit of the fractional part, find the value of
    the following expression.
    d1 × d10 × d100 × d1000 × d10000 × d100000 × d1000000
    """
    def champernowne():
        count = 0
        while True:
            for digit in str(count):
                yield int(digit)
            count += 1

    champernowne_generator = champernowne()

    nths = {1, 10, 100, 1000, 10000, 100000, 1000000}

    values = []
    for n in range(1000001):
        digit = next(champernowne_generator)
        if n in nths:
            values.append(digit)

    from functools import reduce
    return "Digits: {}\nResult: {}".format(values, reduce(lambda x, y: x * y, values))


if __name__ == '__main__':

    functions = (p31, p32, p33, p34, p35, p36, p37, p38, p39, p40)

    tsg = time()
    for func in functions:
        ts = time()
        print(func())
        te = time()
        print("{}(): {} s\n".format(func.__name__, (te - ts)))
    teg = time()

    print("\nTotal time: {} s".format(teg - tsg))

    # func = p35

    # ts = time()
    # print(func())
    # # [func() for _ in range(1000)]
    # te = time()
    # print("{}(): {} s\n".format(func.__name__, (te - ts)))
