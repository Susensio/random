# Develop a program that starting at any number the user inputs, generates the next prime number.
# Ask the user for confirmation to keep going. If it is grantesd print the next prime number again otherwise quit the program.
# ---------------- COMPLETED ----------------


from prime_factors import *


def next_prime(number):
    prime = number + 1
    while not is_prime(prime):
        prime += 1

    return prime


if __name__ == '__main__':
    prime = next_prime(int(input("Input a number to generate next prime: ")))
    print(prime)

    while input("Keep going? (Y/N): ").upper() == 'Y':
        prime = next_prime(prime)
        print(prime)
