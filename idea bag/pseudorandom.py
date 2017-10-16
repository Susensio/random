# A pseudorandom number genrator (PRNG), also known as a deterministic random bit generator (DRBG)
# is an algorithm for generating a sequence of numbers whose properties approximate he properties of sequences of random numbers.
# The PRNG-generated sequence is not truly random, because it is completely determined
# by a relatively small set of initial values, called de PRNG's seeds (which may include truly random values).
# Make your own (pseudo) random number generator. Accept input from the user specifying the number of
# random numbers to generate and the PRNG seed. Output a list of pseudo-random numbers.
from time import time


def middle_squared_method(seed=67524858, check=True):
    """ It is not a good method, since its period is usually very short (no longer than 8^digits)
    and it has some severe weaknesses, such as the output sequence almost always converging to zero.
    """
    previous = set()
    digits = len(str(seed))
    maximun = 10**digits
    seed = int(seed)
    while True:
        if check:
            if not seed or seed in previous:
                break
            previous.add(seed)
        seed = (seed**2 // (10**(digits // 2))) % 10**digits
        yield seed / maximun


def linear_congruential_generator(seed=0, modulus=2**32, multiplier=1664525, increment=1013904223):
    seed = int(seed)
    while True:
        seed = (multiplier * seed + increment) % modulus
        yield seed / modulus


def linear_congruential_generator_bit(seed=0, modulus=2**32, multiplier=1664525, increment=1013904223):
    """ Slightly faster """
    seed = int(seed)
    while True:
        seed = (multiplier * seed + increment) & 0xFFFFFFFF
        yield seed / modulus


if __name__ == '__main__':
    # random_gen = middle_squared_method()
    # nums = [next(random_gen) for _ in range(1000)]
    # print('Max: ', max(nums))
    # print('Min: ', min(nums))
    # print('Mean: ', sum(nums) / len(nums))

    # import matplotlib.pyplot as plt
    # plt.hist(nums)
    # plt.show()

    iterations = 10000000
    random = linear_congruential_generator()
    ts = time()
    [next(random) for _ in range(iterations)]
    print("Modulus: {}s".format(time() - ts))

    random_bit = linear_congruential_generator_bit()
    ts = time()
    [next(random_bit) for _ in range(iterations)]
    print("Bit: {}s".format(time() - ts))
