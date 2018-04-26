from lesson3 import Array
from lesson45 import Matrix

from random import random
import pdb


def random_optimize(cost_function, guess, rate):
    stall = 0
    while True:
        error = cost_function(guess)
        new_guess = random_guess(guess, rate * error)
        new_error = cost_function(new_guess)
        if new_error < error:
            guess = new_guess
            error = new_error
            stall = 0
        if new_error == error:
            stall += 1

        if stall > 1000:
            return

        print(guess)


def random_guess(guess, rate):
    return [x + ((random() * 2 - 1) * rate) for x in guess]


def test_fnc(input_param):
    return (input_param[0] - 5) ** 2


def matrix_cost(M):
    def function(X):
        return sum(x**2 for row in M @ X for x in row) / (sum(x**2 for x in X)**0.5)**2
    return function


def gradient_descend(cost_function, guess, learning_rate=0.0001):
    if type(guess) is Array:
        guess = Array(guess)
    while True:
        gradient = full_gradient(cost_function, guess)
        new_guess = guess - learning_rate * gradient
        if new_guess == guess:
            break
        guess = new_guess
    return guess


def full_gradient(function, point):
    """
    >>> res = Array([4, -0.25])
    >>> res == full_gradient(lambda x: x[0]**2 - x[1]**0.5, [2, 4])
    True
    """
    return Array([partial_derivative(function, point, i)
                  for i, coord in enumerate(point)])


def partial_derivative(function, point, variable, infinitesimal=1e-6):
    """
    >>> res = partial_derivative(lambda x: x[0]**2, [2], 0)
    >>> round(res, 5)
    4.0
    >>> res = partial_derivative(lambda x: x[0]**2 - x[1]**0.5, [2, 4], 1)
    >>> round(res, 5)
    -0.25
    """
    positive = list(point)
    positive[variable] += infinitesimal
    negative = list(point)
    negative[variable] -= infinitesimal

    diference = function(positive) - function(negative)
    distance = 2 * infinitesimal
    derivative = diference / distance
    return derivative


def eigenvector(matrix, eigenvalue):
    order = matrix.shape[0]
    guess = Array([1 for _ in range(order)])
    M = matrix - eigenvalue * Matrix.identity(order)
    cost_function = matrix_cost(M)
    return gradient_descend(cost_function, guess)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # print(gradient_descend(test_fnc, [0]))
    L = 1
    A = Matrix([[2, 1], [1, 2]]) - L * Matrix.identity(2)
    guess = Array([1, 0])
    cost_function = matrix_cost(A)
    print(gradient_descend(cost_function, guess))
