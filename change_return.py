# Develop a program that has the user enter the cost of an item and then the amount the user paid for the item.
# Your program should figuera out the change and the number of coins needed for the change.
from pprint import pprint

euros_values = (500, 200, 100, 50, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01)


def change_return(cost, paid):
    change = []
    difference = cost-paid
    assert difference > 0, "The paid amount must be less than the cost"

    for value in euros_values:
        change.append(int(difference//value))
        difference = difference%value

    return change


change_calculated = change_return(50, 0.01)
pprint({k: v for k, v in zip(euros_values, change_calculated)})
