# Develop a program that has the user enter a number.
# Your program should print out the Fibonacci sequence to the Nth number.
# ---------------- COMPLETED ----------------


def fibonacci(number):
    sequence = []
    fibonacci_number = fibonacci_generator()
    while len(sequence) < number:
        sequence.append(next(fibonacci_number))

    return sequence


def fibonacci_generator():
    a = b = 1
    while True:
        yield a
        a, b = b, a + b


if __name__ == '__main__':
    print(fibonacci(int(input("Fibonacci sequence: "))))
