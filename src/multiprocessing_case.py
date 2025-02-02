import time
import multiprocessing
from .add_random_numbers import add_random_numbers
from .join_random_letters import join_random_letters

def multiprocessing_case(n):
    process_letters = multiprocessing.Process(target=join_random_letters, args=(n,))
    process_numbers = multiprocessing.Process(target=add_random_numbers, args=(n,))

    total_start_time = time.time()
    process_letters.start()
    process_numbers.start()
    process_letters.join()
    process_numbers.join()
    total_end_time = time.time()

    total_time = (total_end_time - total_start_time) * 1000
    print(f"Multiprocessing case taken: {total_time} milliseconds")
    return total_time