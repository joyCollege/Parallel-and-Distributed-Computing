import time
import threading
from .add_random_numbers import add_random_numbers
from .join_random_letters import join_random_letters

def advanced_threading_case(n):
    """
    Executes tasks in parallel using threading.

    This function runs `join_random_letters` and `add_random_numbers` in 
    four separate threads, each handling half of the workload. It measures 
    the total execution time and prints the duration in milliseconds.

    Parameters:
    n (int): The number of iterations, split among threads.

    Returns:
    float: The total execution time in milliseconds.
    """
    thread_letters1 = threading.Thread(target=join_random_letters, args=(n//2,))
    thread_letters2 = threading.Thread(target=join_random_letters, args=(n//2,))

    thread_numbers1 = threading.Thread(target=add_random_numbers, args=(n//2,))
    thread_numbers2 = threading.Thread(target=add_random_numbers, args=(n//2,))

    total_start_time = time.time()
    thread_letters1.start()
    thread_letters2.start()
    thread_numbers1.start()
    thread_numbers2.start()

    thread_letters1.join()
    thread_letters2.join()
    thread_numbers1.join()
    thread_numbers2.join()
    total_end_time = time.time()

    total_time = (total_end_time - total_start_time) * 1000
    print(f"Advanced Threading case taken: {total_time} milliseconds")
    return total_time