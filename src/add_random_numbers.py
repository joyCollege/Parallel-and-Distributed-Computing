import random
def add_random_numbers():
    numbers = [random.randint(1, 1000) for _ in range(1000000)]
    total_sum = sum(numbers)
    return total_sum