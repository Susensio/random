# Your program will accept a mathematical expression as a string,
# parse it and output the answer of the expression.
# For example, "2*3+2-(4+5)" will output -1.


# MINIMALISM
# from math import *
# while True:
#     print(eval(input("Enter expression: ")))


# TOKENIZER
class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "{}\t{}".format(self.value, self.type)

    def __repr__(self):
        return "Token({},'{}')".format(self.type, self.value)


def is_digit(ch):
    return ch in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'}


def is_letter(ch):
    return all(not func(ch) for func
               in (is_digit, is_operator, is_left_parenthesis, is_right_parenthesis))


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


def simple_token(c):
    if is_operator(c):
        return Token('operator', c)
    elif is_left_parenthesis(c):
        return Token('left', c)
    else:
        return Token('right', c)


def tokenize(text):
    exp = []
    number_buffer = []
    letter_buffer = []
    for c in text:
        if len(number_buffer):
            if is_digit(c):
                number_buffer.append(c)
            else:
                exp.append(Token('literal', ''.join(number_buffer)))
                number_buffer.clear()
                if is_letter(c):
                    exp.append(Token('operator', '*'))
                    letter_buffer.append(c)
                else:
                    exp.append(simple_token(c))

        elif len(letter_buffer):
            if is_letter(c):
                letter_buffer.append(c)
            else:
                if len(letter_buffer) == 1:
                    exp.append(Token('variable', ''.join(letter_buffer)))
                else:
                    exp.append(Token('function', ''.join(letter_buffer)))
                letter_buffer.clear()

                if is_digit(c):
                    number_buffer.append(c)
                else:
                    exp.append(simple_token(c))
        else:
            if is_digit(c):
                number_buffer.append(c)
            elif is_letter(c):
                letter_buffer.append(c)
            else:
                exp.append(simple_token(c))

    if len(number_buffer):
        exp.append(Token('literal', ''.join(number_buffer)))
    elif len(letter_buffer):
        exp.append(Token('variable', ''.join(letter_buffer)))

    return exp


# expression = input("Enter expression: ")
# print(calculate(expression))
expresion = '56.1+6sen(a)'
from pprint import pprint
pprint(tokenize(expresion))
