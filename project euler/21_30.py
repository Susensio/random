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
    # Python library approach
    # from itertools import permutations
    # perms = list(permutations('0123456789'))[1000000-1]
    # return ''.join(perms)

    # BRUTE FORCE approach
    import sys
    sys.path.append("../chess/")
    from util import memoize

    @memoize
    def permute(digits):
        if len(list(digits)) == 1:
            return digits
        else:
            # perms = []
            # for digit in digits:
            #     new_digits = tuple(d for d in digits if d != digit)
            #     for perm in permute(new_digits):
            #         perms.append(digit * 10**(len(digits) - 1) + perm)
            # return perms
            return [digit * 10**(len(digits) - 1) + perm
                    for digit in digits
                    for perm in permute(tuple(d for d in digits if d != digit))]

    perms = permute(range(10))
    return perms[1000000 - 1]


def p25():
    """ 1000-digit Fibonacci number
    The Fibonacci sequence is defined by the recurrence relation:
    Fn = Fn−1 + Fn−2, where F1 = 1 and F2 = 1.
    Hence the first 12 terms will be:
     1  2  3  4  5  6   7   8   9  10  11   12
    (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144)
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
    import decimal
    import re

    decimal.getcontext().prec = 10000
    pattern = re.compile(r"([\d]+?)\1\1")

    def recurring_cycle(denominator):
        number = str(decimal.Decimal(1) / decimal.Decimal(denominator))
        search = pattern.search(number)
        if search:
            return len(search.group(1))
        else:
            return 0

    results = [(number, recurring_cycle(number)) for number in range(1, 1000)]
    # from pprint import pprint
    # pprint(sorted(results, key=lambda x: x[1]))

    return "1/d \td={} \tcycle={}".format(*max(results, key=lambda x: x[1]))


def p27():
    """ Quadratic primes
    Euler discovered the remarkable quadratic formula:
    n²+n+41
    It turns out that the formula will produce 40 primes for the consecutive 
    integer values 0≤n≤39. However, when n=40, 40²+40+41 = 40(40+1)+41 is divisible by 41, 
    and certainly when n=41, 41²+41+41 is clearly divisible by 41.

    The incredible formula n²−79n+1601 was discovered, which produces 80 primes 
    for the consecutive values 0≤n≤79. The product of the coefficients, −79 and 1601, is −126479.

    Considering quadratics of the form
    n²+an+b, where |a|<1000 and |b|≤1000

    Find the product of the coefficients, a and b, for the quadratic expression that produces 
    the maximum number of primes for consecutive values of n, starting with n=0.
    """
    # BRUTE FORCE
    import sys
    sys.path.append("../idea bag/")
    from prime_factors import is_prime

    def quadratic(a, b, n):
        return n * n + a * n + b

    ab_values = [(a, b) for a in range(-1000, 1000) for b in range(-1000, 1000)]
    n = 0
    while True:
        # print(n, len(ab_values))
        # new_ab_values = []
        # for ab in ab_values:
        #     if len(ab_values) <= 1:
        #         (a, b) = ab
        #         return n, 'n²{:+}n{:+}={}'.format(*ab, quadratic(*ab, n)), 'a*b={}'.format(a * b)
        #     if is_prime(quadratic(*ab, n)):
        #         new_ab_values.append(ab)
        # ab_values = new_ab_values

        # OPTIMIZED
        ab_values = [ab for ab in ab_values if is_prime(quadratic(*ab, n))]

        if len(ab_values) <= 1:
            (a, b) = ab_values[0]
            return ('Consecutive primes:{}'.format(n),
                    'n²{:+}n{:+}={}'.format(a, b, quadratic(a, b, n)),
                    'a*b={}'.format(a * b))
        n += 1


def p28():
    """ Number spiral diagonals
    Starting with the number 1 and moving to the right in a clockwise direction 
    a 5 by 5 spiral is formed as follows:

       [21] 22  23  24 [25]
        20  [7]  8  [9] 10
        19   6  [1]  2  11
        18  [5]  4  [3] 12
       [17] 16  15  14 [13]

    It can be verified that the sum of the numbers on the diagonals is 101.
    What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral formed in the same way?
    """
    side = 1001

    def is_diagonal(x, y):
        return x == y or side - 1 - x == y or side - 1 - y == x

    def can_turn(spiral, x, y, xdir, ydir):
        xdir, ydir = next_dir(xdir, ydir)
        return not spiral[x + xdir][y + ydir]

    def next_dir(x, y):
        """ Clockwise """
        if (x, y) == (1, 0):
            return (0, -1)
        if (x, y) == (0, -1):
            return (-1, 0)
        if (x, y) == (-1, 0):
            return (0, 1)
        if (x, y) == (0, 1):
            return (1, 0)

    spiral = [[None for x in range(side)] for y in range(side)]

    x = y = side // 2
    # Its unimportant the initial direction
    xdir, ydir = -1, 0

    for n in range(side * side):
        spiral[x][y] = n + 1
        if can_turn(spiral, x, y, xdir, ydir):
            xdir, ydir = next_dir(xdir, ydir)
        x += xdir
        y += ydir

    return sum([spiral[x][y] for x in range(side) for y in range(side) if is_diagonal(x, y)])


def p29():
    """ Distinct powers
    Consider all integer combinations of a^b for 2 ≤ a ≤ 5 and 2 ≤ b ≤ 5:

    2^2=4, 2^3=8, 2^4=16, 2^5=32
    3^2=9, 3^3=27, 3^4=81, 3^5=243
    4^2=16, 4^3=64, 4^4=256, 4^5=1024
    5^2=25, 5^3=125, 5^4=625, 5^5=3125
    If they are then placed in numerical order, with any repeats removed, 
    we get the following sequence of 15 distinct terms:

    4, 8, 9, 16, 25, 27, 32, 64, 81, 125, 243, 256, 625, 1024, 3125

    How many distinct terms are in the sequence generated by ab for 2 ≤ a ≤ 100 and 2 ≤ b ≤ 100?
    """
    a_max = 100
    b_max = 100

    return len(set(a**b for a in range(2, a_max + 1) for b in range(2, b_max + 1)))


def p30():
    """ Digit fifth powers
    Surprisingly there are only three numbers that can be written as the sum of fourth powers of their digits:

    1634 = 1^4 + 6^4 + 3^4 + 4^4
    8208 = 8^4 + 2^4 + 0^4 + 8^4
    9474 = 9^4 + 4^4 + 7^4 + 4^4
    As 1 = 1^4 is not a sum it is not included.

    The sum of these numbers is 1634 + 8208 + 9474 = 19316.

    Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.
    """
    power = 5

    n = 1
    while True:
        """ Solve inequation n*9^5 < 10^(n+1) ===> n > X """
        n += 0.1
        if n * 9**power < 10**(n + 1):
            break
    limit = int(10**(n + 1)) + 1

    powers = {str(n): n**power for n in range(10)}

    def sum_of_digits_powered(number, power):
        number = str(number)
        return sum([powers[n] for n in number])

    numbers = [number for number in range(10, limit) if number == sum_of_digits_powered(number, power)]

    return "sum={}\tnumbers:{}".format(sum(numbers), numbers)


if __name__ == '__main__':

    functions = (p21, p22, p23, p24, p25, p26, p27, p28, p29, p30)

    for func in functions:
        ts = time()
        print(func())
        te = time()
        print("{}(): {} s\n".format(func.__name__, (te - ts)))

    # func = p30

    # ts = time()
    # print(func())
    # # [func() for _ in range(1000)]
    # te = time()
    # print("{}(): {} s\n".format(func.__name__, (te - ts)))
