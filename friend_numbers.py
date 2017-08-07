from math import sqrt


def sum_factors(num):
    min = 2
    max = sqrt(num)
    factors = [1]
    while min < max:
        if not num % min:
            factors.extend([min, num // min])
        min += 1
    return sum(factors)


def friends(max):
    friends = []
    sums = {}
    for num in range(max + 1):
        current_sum = sum_factors(num)
        if sums.get(current_sum) == num:  # Friend founded!
            friends.append((num, current_sum))
        sums[num] = current_sum
    return friends


print(friends(10000))
