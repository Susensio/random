from time import time


def p21():
    """ Amicable numbers
    Let d(n) be defined as the sum of proper divisors of n
    (numbers less than n which divide evenly into n).
    If d(a) = b and d(b) = a, where a ≠ b, then a and b are an amicable pair
    and each of a and b are called amicable numbers.
    For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110;
    therefore d(220) = 284. The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.
    Evaluate the sum of all the amicable numbers under 10000.
    """
    from math import sqrt

    def sum_factors(num):
        min = 2
        max = sqrt(num)
        factors = [1]
        while min < max:
            if not num % min:
                factors.extend([min, num // min])
            min += 1
        return sum(factors)

    def friends(max):
        friends = []
        sums = {}
        for num in range(max + 1):
            current_sum = sum_factors(num)
            if sums.get(current_sum) == num:  # Friend founded!
                friends.append((num, current_sum))
            sums[num] = current_sum
        return friends
    return sum([friend for couple in friends(10000) for friend in couple])


def p22():
    """ Names scores
    Using names.txt (right click and 'Save Link/Target As...'),
    a 46K text file containing over five-thousand first names,
    begin by sorting it into alphabetical order. Then working out
    the alphabetical value for each name, multiply this value
    by its alphabetical position in the list to obtain a name score.
    For example, when the list is sorted into alphabetical order,
    COLIN, which is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name
    in the list. So, COLIN would obtain a score of 938 × 53 = 49714.

    What is the total of all the name scores in the file?
    """
    import csv
    from functools import reduce

    def alpha_value(name):
        # return reduce(lambda a, i: a + ord(i) - 64, name, 0)
        return sum([ord(i) - 64 for i in name])

    score = 0
    with open('names.txt') as file:
        reader = csv.reader(file, delimiter=',')
        names = list(reader)[0]
        names.sort()
        # score = reduce(lambda a, i: a + (i[0] + 1) * alpha_value(i[1]), enumerate(names), 0)
        score = sum([i * alpha_value(name) for i, name in enumerate(names)])

    return score
    # 20% faster with comprehensions


def p23():
    """ Non-abundant sums
    A perfect number is a number for which the sum of its proper divisors is exactly equal to the number.
    For example, the sum of the proper divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28,
    which means that 28 is a perfect number.
    A number n is called deficient if the sum of its proper divisors is less than n
    and it is called abundant if this sum exceeds n.
    As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16,
    the smallest number that can be written as the sum of two abundant numbers is 24.
    By mathematical analysis, it can be shown that all integers greater than 28123 can be written
    as the sum of two abundant numbers. However, this upper limit cannot be reduced any further
    by analysis even though it is known that the greatest number that cannot be expressed
    as the sum of two abundant numbers is less than this limit.

    Find the sum of all the positive integers which CANNOT be written as the sum of two abundant numbers.
    """
    import sys
    sys.path.append("../idea bag/")
    from prime_factors import factors

    def is_abundant(number):
        return number <= sum(factors(number))

    def abundant_numbers_upto(limit):
        return (number for number in range(1, limit) if is_abundant(number))

    abundants = set(abundant_numbers_upto(28123))

    def is_sum_of_two_abundants(number):
        for abundant in abundants:
            if abundant > number:
                return False
            if number - abundant in abundants:
                return True

    return sum((number for number in range(28124) if not is_sum_of_two_abundants(number)))


def p24():
    """ Lexicographic permutations
    A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation of
    the digits 1, 2, 3 and 4. If all of the permutations are listed numerically or alphabetically,
    we call it lexicographic order.
    The lexicographic permutations of 0, 1 and 2 are:
    012   021   102   120   201   210

    What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?
    """
    # BRUTE FORCE approach
    import sys
    sys.path.append("../chess/")
    from util import memoize

    @memoize
    def permute(digits):
        if len(digits) == 1:
            return digits[0]
        else:
            return []

    perms = list(permute(tuple(range(2))))
    # assert(perms[0] == 123456789)
    return perms


def p25():
    """ 1000-digit Fibonacci number
    The Fibonacci sequence is defined by the recurrence relation:
    Fn = Fn−1 + Fn−2, where F1 = 1 and F2 = 1.
    Hence the first 12 terms will be:
    F1 = 1
    F2 = 1
    F3 = 2
    F4 = 3
    F5 = 5
    F6 = 8
    F7 = 13
    F8 = 21
    F9 = 34
    F10 = 55
    F11 = 89
    F12 = 144
    The 12th term, F12, is the first term to contain three digits.

    What is the index of the first term in the Fibonacci sequence to contain 1000 digits?
    """
    import sys
    sys.path.append("../idea bag/")
    from fibonacci import fibonacci_generator

    index = 0
    number = 0
    fibonacci_number = fibonacci_generator()
    while len(str(number)) < 1000:
        number = next(fibonacci_number)
        index += 1

    return index


def p26():
    """ Reciprocal cycles
    A unit fraction contains 1 in the numerator. The decimal representation
    of the unit fractions with denominators 2 to 10 are given:
    1/2 =   0.5
    1/3 =   0.(3)
    1/4 =   0.25
    1/5 =   0.2
    1/6 =   0.1(6)
    1/7 =   0.(142857)
    1/8 =   0.125
    1/9 =   0.(1)
    1/10    =   0.1
    Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. 
    It can be seen that 1/7 has a 6-digit recurring cycle.

    Find the value of d < 1000 for which 1/d contains 
    the longest recurring cycle in its decimal fraction part.
    """
    def recurring_cycle(denominator):
        number = str(1 / denominator)
        return number

    pass


if __name__ == '__main__':

    # functions = (p21, p22, p23, p24, p25, p26, p27, p28, p29, p30)

    # for func in functions:
    #     ts = time()
    #     print(func())
    #     te = time()
    #     print("{}(): {} s\n".format(func.__name__, (te - ts)))

    func = p24

    ts = time()
    print(func())
    # [func() for _ in range(1000)]
    te = time()
    print("{}(): {} s\n".format(func.__name__, (te - ts)))
