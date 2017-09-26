# Gray code, so named after discoverer Frank Gray, is a binary numeral system
# where two successive values differ in only one bit (binary digit).
# The reflected binary code was originally designed to prevent spurious output
# from electromechanical switches. Today, Gray code is widely used to facilitate
# error correction in digital communications such as digital terrestrial television
# and some cable TV systems.
# Write a program that can generate a Gray code sequence of a decimal the user inputs.


def grey_code_sequence(digits):
    sequence = []
    number = 0
    while number not in sequence:
        sequence.append(number)
        for index in range(digits):
            selector = 1 << index
            number_next = number ^ selector
            if number_next not in sequence:
                number = number_next
                break

    return sequence

bits = 6
for number in grey_code_sequence(bits):
    print("{0:b}".format(number).zfill(bits))
