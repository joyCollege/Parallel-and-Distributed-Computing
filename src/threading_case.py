import time
import threading
from .add_random_numbers import add_random_numbers

def wrapper_add_random_numbers(start, end, result_list):
        result_list.append(add_random_numbers(start, end))

def threading_case(num_threads=2, num_numbers=1000):
    print(f"\nStarting all {num_threads} threads...")
    total_start_time = time.time()

    chunk_size = num_numbers // num_threads
    threads = []
    results = []  

    for i in range(0, num_threads):
        print("i:",  i)
        start = i * chunk_size
        end = start + chunk_size
        print("start:",  start)
        print("end:",  end)
        if i == num_threads - 1:  end = num_numbers # Handle everything remaining in the last thread

        thread = threading.Thread(target=wrapper_add_random_numbers, args=(start, end, results))
        threads.append(thread)
        thread.start()
        print(f">> Starting {thread.name}")

    for thread in threads:
        thread.join()

    # Calculate the total sum
    total_sum = sum(results)
    print(f">> Sum of random numbers: {total_sum}")

    total_end_time = time.time()
    total_time = (total_end_time - total_start_time) * 1000
    print(f">> Time taken: {total_time} milliseconds")

    return total_time
