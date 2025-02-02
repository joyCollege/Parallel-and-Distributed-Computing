import time
import threading
from .add_random_numbers import add_random_numbers
from .join_random_letters import join_random_letters

def threading_case(n):
    thread_letters = threading.Thread(target=join_random_letters, args=(n,))
    thread_numbers = threading.Thread(target=add_random_numbers, args=(n,))

    total_start_time = time.time()
    thread_letters.start()
    thread_numbers.start()
    thread_letters.join()
    thread_numbers.join()
    total_end_time = time.time()

    total_time = (total_end_time - total_start_time) * 1000
    print(f"Threading case taken: {total_time} milliseconds")
    return total_time