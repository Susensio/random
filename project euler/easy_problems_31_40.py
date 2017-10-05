from time import time


def p31():
    """ Coin sums
    In England the currency is made up of pound, £, and pence, p, and there are eight coins in general circulation:

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

    Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.
    HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.
    """
    pass


def p33():
    """ Digit cancelling fractions
    The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting
    to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.
    We shall consider fractions like, 30/50 = 3/5, to be trivial examples.
    There are exactly four non-trivial examples of this type of fraction, less than one in value,
    and containing two digits in the numerator and denominator.

    If the product of these four fractions is given in its lowest common terms, find the value of the denominator.
    """
    pass


def p34():
    pass


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


if __name__ == '__main__':

    # functions = (p31, p32, p33, p34, p35, p36, p37, p38, p39, p40)

    # for func in functions:
    #     ts = time()
    #     print(func())
    #     te = time()
    #     print("{}(): {} s\n".format(func.__name__, (te - ts)))

    func = p35

    ts = time()
    print(func())
    # [func() for _ in range(1000)]
    te = time()
    print("{}(): {} s\n".format(func.__name__, (te - ts)))
