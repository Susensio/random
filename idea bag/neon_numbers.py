# A number is said to be a Neon Number if the sum of the digits of the square of the number is equal tu the number itself.
# Example- 9 is a Neon Number. 9*9=81 and 8+1 = 9. Hence it is a Neon Number.
# The user is propted to input a range eh 1-90. Yout program should print out the neon numbers in tha range.
# ---------------- COMPLETED ---------------- 
# There are only 3 neon numbers: 0, 1, 9

def check_neon_number(num):
    squared = num ** 2
    sum_digits = sum([int(digit) for digit in str(squared)])
    return num == sum_digits

def search_neon_numbers(start, end):
    res = []
    for n in range(start, end+1):
        if check_neon_number(n):
            res.append(n)
    return res

print(search_neon_numbers(1,10000))