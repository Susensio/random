# Your program will accept a mathematical expression as a string,
# parse it and output the answer of the expression.
# For example, "2*3+2-(4+5)" will output -1.


# MINIMALISM
from math import *
while True:
    print(eval(input("Enter expression: ")))