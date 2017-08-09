# Develop a program that accepts an integer and outputs the Roman Number equivalent of that number.
#
# Symbols:
# I = 1
# V = 5
# X = 10
# L = 50
# C = 100
# D = 500
# M = 1000
#
# 1 to 10:
# I, II, III, IV, V, VI, VII, VIII, IX, X.
# ---------------- COMPLETED ----------------

import re

symbols = {'I' : 1, 'V' : 5, 'X' : 10, 'L' : 50, 'C' : 100, 'D' : 500, 'M' : 1000}

def roman_to_integer(num):
    regex = "^[IVXLCDM]*$"
    if not re.fullmatch(regex,num):
        raise ValueError("Argument is not a valid Roman number")

    result = 0
    for i, c in enumerate(num):
        if i == len(num)-1:
            result += symbols[c]
            return result

        if symbols[c] < symbols[num[i+1]]:
            result -= symbols[c]
        else:
            result += symbols[c]

    return result


def integer_to_roman(num):
    if not isinstance(num, int):
        raise TypeError("expected integer, got {}".format(str(type(num))))
    if not 0 < num < 4000:
        raise ValueError("Argument must be between 1 and 3999")

    mils=num // 1000
    cens=num % 1000 // 100
    decs=num % 100 // 10
    unit=num % 10

    M="M" * mils
    if cens == 9:
        D=""
        C="CM"
    elif cens == 4:
        D=""
        C="CD"
    else:
        D="D" * (cens // 5)
        C="C" * (cens % 5)

    if decs == 9:
        L=""
        X="XC"
    elif decs == 4:
        L=""
        X="XL"
    else:
        L="L" * (decs // 5)
        X="X" * (decs % 5)

    if unit == 9:
        V=""
        I="IX"
    elif unit == 4:
        V=""
        I="IV"
    else:
        V="V" * (unit // 5)
        I="I" * (unit % 5)

    return "{}{}{}{}{}{}{}".format(M, D, C, L, X, V, I)


print(integer_to_roman(2896))

print(roman_to_integer("MMDCCCXCVI"))
