import random

numbers = {
    1: "ichi",
    2: "ni",
    3: "san",
    4: "shi",
    5: "go",
    6: "roku",
    7: "shichi",
    8: "hachi",
    9: "kyu",
    10: "ju"}

print("Japanese numbers\n")

answer = ''
while answer != 'exit':
    test = random.randint(-10, 10)
    if test:
        if test > 0:
            while answer != numbers.get(test):
                answer = input(str(test) + ": ")
        else:
            while numbers.get(answer) != numbers.get(-test):
                answer = int(input(numbers[-test] + ": "))
    else:
        print("\nFull sequence!")
        answer = ''
        for num in range(1, 11):
            while answer != numbers[num]:
                answer = input(str(num) + ": ")
        print("Done!\n")
