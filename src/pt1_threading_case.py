import time
import threading
from .pt2_worker import worker

def threading_case(num_threads=2, num_numbers=1000):
    """
    Executes a multi-threaded summation of random numbers.

    Args:
        num_threads (int, optional): The number of threads to use (default is 2).
        num_numbers (int, optional): The total count of numbers to sum (default is 1000).

    Returns:
        float: The total execution time in milliseconds.

    The function divides the task among multiple threads, each summing a portion of the numbers.
    It records the start and end time to measure execution duration.
    """

    print(f"\nStarting all {num_threads} threads...")

    total_start_time = time.time()
    task_divided = num_numbers // num_threads
    threads = []
    results = []

    for i in range(num_threads):
        start = i * task_divided + 1
        end = start + task_divided
        if i == num_threads - 1:
            end = num_numbers + 1  # Handle the remaining numbers in the last thread

        thread = threading.Thread(target=worker, args=(start, end, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(results)
    print(f">> Final sum: {total_sum}")

    total_end_time = time.time()  # Capture the time after all threads have finished
    total_time = (total_end_time - total_start_time) * 1000  # Convert to milliseconds
    print(f">> Time taken: {total_time} milliseconds")

    return total_time
