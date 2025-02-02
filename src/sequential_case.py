import time
from .add_random_numbers import add_random_numbers
from .join_random_letters import join_random_letters

def sequential_case(n):
    total_start_time = time.time()
    join_random_letters(n)
    add_random_numbers(n)
    total_end_time = time.time()
    
    total_time = (total_end_time - total_start_time) * 1000
    print(f"Serial case taken: {total_time} milliseconds")
    return total_time