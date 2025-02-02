import time
from add_random_numbers import add_random_numbers
from join_random_letters import join_random_letters

def sequential_case():
    total_start_time = time.time()
    join_random_letters()
    add_random_numbers()
    total_end_time = time.time()
    print(f"Serial case time taken:  {total_end_time - total_start_time} seconds")