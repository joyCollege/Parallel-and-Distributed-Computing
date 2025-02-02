import random

def add_random_numbers(n=1000):
    numbers = [random.randint(1, 1000) for _ in range(n)]
    total_sum = sum(numbers)
    return total_sum