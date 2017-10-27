from time import time


def p41():
    """ Pandigital prime
    We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n
    exactly once. For example, 2143 is a 4-digit pandigital and is also prime.
    What is the largest n-digit pandigital prime that exists?
    """
    import sys
    sys.path.append("../idea bag/")
    from prime_factors import is_prime
    from itertools import permutations

    # EVERY 9 and 8 digit pandigital number is divisible by 3 as the sum of its digits is 45 and 36
    # Thus the search starts with 7 digits
    result = 0
    # Generate all posible permutations of [1..n] for n in [7..1]
    for digits in range(7, 1, -1):
        perms = permutations(str(d) for d in range(1, digits + 1))
        # Reverse sort perms and check for primes
        for perm in sorted(perms, reverse=True):
            if is_prime(int(''.join(perm))):
                result = int(''.join(perm))
                break
        else:
            continue  # executed if the loop ended normally (no break)
        break  # executed if 'continue' was skipped (break)

    return "Largest pandigital prime: {}".format(result)


def p42():
    """ Coded triangle numbers
    The nth term of the sequence of triangle numbers is given by, tn = 0.5n(n+1); so the first ten
    triangle numbers are:
    1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

    By converting each letter in a word to a number corresponding to its alphabetical position and
    adding these values we form a word value. For example, the word value for SKY is
    19 + 11 + 25 = 55 = t10. If the word value is a triangle number then we shall call the word
    a triangle word.
    Using words.txt, a 16K text file containing nearly two-thousand common English words, how many
    are triangle words?
    """
    import csv

    def letter_to_num(letter):
        return ord(letter.upper()) - 64  # 64 = ord('A') - 1

    triangular_nums = {n * (n + 1) // 2 for n in range(50)}

    def is_triangular(word):
        value = sum(letter_to_num(letter) for letter in word)
        return value in triangular_nums

    with open('words.txt') as file:
        reader = csv.reader(file, delimiter=',')
        words = list(reader)[0]

    return "Triangular words: {}".format(len([word for word in words if is_triangular(word)]))


if __name__ == '__main__':

    # functions = (p41, p42, p43, p44, p45, p46, p47, p48, p49, p50)

    # for func in functions:
    #     ts = time()
    #     print(func())
    #     te = time()
    #     print("{}(): {} s\n".format(func.__name__, (te - ts)))

    func = p42

    ts = time()
    print(func())
    # [func() for _ in range(1000)]
    te = time()
    print("{}(): {} s\n".format(func.__name__, (te - ts)))
