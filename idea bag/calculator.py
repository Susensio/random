# Your program will accept a mathematical expression as a string,
# parse it and output the answer of the expression.
# For example, "2*3+2-(4+5)" will output -1.


# MINIMALISM
# from math import *
# while True:
#     print(eval(input("Enter expression: ")))


# TOKENIZER
Token = namedTuple('Token', ['type', 'value'])


def is_digit(ch):
    return ch in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'}


def is_letter(ch):
    return all(not func(ch) for func in (is_digit, is_operator, is_left_parenthesis, is_right_parenthesis))


def is_operator(ch):
    return ch in {'+', '-', '*', '/', }


def is_left_parenthesis(ch):
    return ch == '('


def is_right_parenthesis(ch):
    return ch == ')'


def calculate(text):
    exp = tokenize(text)
    while len(exp) > 1:
        pass
    return exp


def tokenize(text):
    exp = []
    number_buffer = []
    letter_buffer = []
    for c in text:
        if is_digit(c):
            number_buffer.append(c)
    return exp


expression = input("Enter expression: ")
print(calculate(expression))
