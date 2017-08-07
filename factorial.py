# The Factorial of a positive integer, n, is defined as the product of the sequence n, n-1, n-2, ...1.
# Also the factorial of zero, 0, is defined as being 1.
# Develop a program that solves the factorial of any user given number, using both loops and recursion.
# ---------------- COMPLETED ----------------


def factorial(number):
    if number == 0:
        return 1
    else:
        return number * factorial(number - 1)


if __name__ == '__main__':
    num = input("Calculate factorial of: ")
    res = factorial(int(num))
    print("{}! = {}".format(num, res))
