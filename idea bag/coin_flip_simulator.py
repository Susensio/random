# Write some code that simulates flipping a single coin however many times the user decides.
# The code should record the outcomes and count the number of taisl and heads.

from random import random


def flip_coin():
    return random() < 0.5


def print_stats(flips):
    heads = len([_ for _ in flips if _])
    print("".join(["+" if _ else "-" for _ in flips]))
    max_heads = 0
    max_tails = 0
    count = 0

    prev = flips[0]

    for flip in flips:
        if flip == prev:
            count += 1
        else:
            if not flip:
                max_heads = max(count, max_heads)
            else:
                max_tails = max(count, max_tails)
            count = 1
        prev = flip
    else:
        if flip:
            max_heads = max(count, max_heads)
        else:
            max_tails = max(count, max_tails)

    print("\tTotal\tIn a row")
    print("Heads:\t{0}\t{1}\nTails:\t{2}\t{3}\n".format(heads, max_heads, toss - heads, max_tails))


if __name__ == '__main__':
    while True:
        toss = int(input("Enter number of coin toss: "))
        if toss == 0:
            break

        results = []
        for _ in range(toss):
            results.append(flip_coin())

        print_stats(results)
