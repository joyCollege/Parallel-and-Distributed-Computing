import time
from .add_random_numbers import add_random_numbers

def sequential_case(num_numbers=1000):
    print(f"\nStarting the sequential case...")

    total_start_time = time.time()
    result = add_random_numbers(0, num_numbers)
    print(f">> Sum of random numbers: {result}")
    total_end_time = time.time()
    
    total_time = (total_end_time - total_start_time) * 1000
    print(f">> Time taken: {total_time} milliseconds")
    return total_time