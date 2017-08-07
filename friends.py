# A happy number is defined by the following process. Starting with any positive integer, replace the number
# by the sum of the squares of its digits, and repeat the process until the number equals 1 (where it will stay),
# or it loops endlessly in a cycle which dos not include 1. Those numbers for which this process ends in 1 are happy number,
# while those that do not end in 1 are unhappy numbers. Find the first 8 happy numbers.
# ---------------- COMPLETED ----------------


def is_happy(number):
    sequence = [number]

    while True:
        next_number = next(number)
        if next_number == 1:
            # print(sequence)
            return True
        elif next_number in sequence:
            return False
        number = next_number
        sequence.append(number)


def next(number):
    return sum([int(n)**2 for n in str(number)])


happy_numbers = []
number = 1

while len(happy_numbers) < 143:
    if is_happy(number):
        happy_numbers.append(number)
    number += 1


print(happy_numbers)
