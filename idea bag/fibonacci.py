# Develop a program that has the user enter a number.
# Your program should print out the Fibonacci sequence to the Nth number.
# ---------------- COMPLETED ----------------


def fibonacci(number):
    sequence = []
    a = b = 1

    while len(sequence) < number:
        sequence.append(a)
        a, b = b, a + b

    return sequence


print(fibonacci(int(input("Fibonacci sequence: "))))
