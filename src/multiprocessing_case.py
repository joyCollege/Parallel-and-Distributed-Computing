import time
import multiprocessing
from .add_random_numbers import add_random_numbers
from .join_random_letters import join_random_letters

def multiprocessing_case():
    process_letters = multiprocessing.Process(target=join_random_letters)
    process_numbers = multiprocessing.Process(target=add_random_numbers)

    total_start_time = time.time()
    process_letters.start()
    process_numbers.start()
    process_letters.join()
    process_numbers.join()
    total_end_time = time.time()

    print(f"Multiprocessing case time taken:  {total_end_time - total_start_time} seconds")
