import time


def timeit(method):

    def inner(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()

        print("{} ({}, {}) {:0.6f} ms".format(method.__name__, args, kwargs, (te - ts) * 1000))
        return result

    return inner


@timeit
def sum_comprehension(number):
    for n in range(number):
        _ = sum(int(digit) for digit in str(n))


@timeit
def sum_maping(number):
    for n in range(number):
        _ = sum(map(int, str(number)))


@timeit
def sum_while(number):
    for n in range(number):
        s = 0
        while n:
            s += n % 10
            n //= 10


@timeit
def sum_divmod(number):
    for n in range(number):
        s = 0
        while n:
            n, remainder = divmod(n, 10)
            s += remainder


if __name__ == '__main__':
    number = 1000000

    sum_while(number)
    sum_divmod(number)
    sum_maping(number)
    sum_comprehension(number)
