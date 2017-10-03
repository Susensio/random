from time import time


def p31():

    pass


if __name__ == '__main__':

    # functions = (p31, p32, p33, p34, p35, p36, p37, p38, p39, p40)

    # for func in functions:
    #     ts = time()
    #     print(func())
    #     te = time()
    #     print("{}(): {} s\n".format(func.__name__, (te - ts)))

    func = p20

    ts = time()
    print(func())
    # [func() for _ in range(1000)]
    te = time()
    print("{}(): {} s\n".format(func.__name__, (te - ts)))
