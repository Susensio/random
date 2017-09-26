# Develop a program that has the user enter a number.
# Your program should print out Euler number up to that many decimal places.
# Try to keep a limit as to how far the program will go.
import math


# Newton's Series Expansion for e
# e = ∑(n=0→∞) 1/n!
def euler_newton(steps):
    euler = 0
    for n in range(steps):
        euler += 1/math.factorial(n)
    return euler

# Brothers' Formulae for e
# e = ∑(n=0→∞) (2n+2)/(2n+1)!
def euler_brothers(steps):
    euler = 0
    for n in range(steps):
        euler += (2*n+2)/math.factorial(2*n+1)
    return euler


if __name__ == '__main__':
    print("e = {}".format(math.e))

    e_newton = euler_newton(12)
    print("Newton's Series:\t{}\t Precision: {}".format(e_newton, abs(e_newton-math.e)))

    e_brothers = euler_brothers(6)
    print("Brothers' Formulae:\t{}\t Precision: {}".format(e_brothers, abs(e_brothers-math.e)))