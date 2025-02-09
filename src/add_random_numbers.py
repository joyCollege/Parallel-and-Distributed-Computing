import random

def add_random_numbers(start=0, end=1000):
    total_sum = 0
    for _ in range(start, end):
        total_sum += random.randint(1, 1000)
    return total_sum

