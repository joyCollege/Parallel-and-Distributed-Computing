import time
import threading
from .add_random_numbers import add_random_numbers
from .join_random_letters import join_random_letters

def threading_case():
    thread_letters = threading.Thread(target=join_random_letters)
    thread_numbers = threading.Thread(target=add_random_numbers)

    total_start_time = time.time()
    thread_letters.start()
    thread_numbers.start()
    thread_letters.join()
    thread_numbers.join()
    total_end_time = time.time()

    print(f"Threading case time taken:  {total_end_time - total_start_time} seconds")
