import threading
import time

def worker(start, end, result_list):
    """Function to calculate sum for a specific range."""
    partial_sum = sum(range(start, end))
    result_list.append(partial_sum)
    print(f"Thread processing range {start}-{end} finished with sum {partial_sum}")

def parallel_sum(num_threads=4, n=1000):
    """Function to calculate the sum of numbers from 1 to n using multiple threads."""
    print(f"Starting parallel sum with {num_threads} threads...")

    total_start_time = time.time()
    task_divided = n // num_threads
    threads = []
    results = []

    for i in range(num_threads):
        start = i * task_divided + 1
        end = start + task_divided
        if i == num_threads - 1:  # Handle the remaining numbers in the last thread
            end = n + 1

        thread = threading.Thread(target=worker, args=(start, end, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(results)
    print(f"Total sum calculated by threads: {total_sum}")

    total_end_time = time.time()
    total_time = (total_end_time - total_start_time) * 1000  # Convert to milliseconds
    print(f"Parallel execution time: {total_time} milliseconds")

    return total_sum, total_time


def sequential_sum(n=1000):
    """Function to calculate sum of numbers from 1 to n sequentially."""
    total_start_time = time.time()
    total_sum = sum(range(1, n + 1))
    total_end_time = time.time()
    total_time = (total_end_time - total_start_time) * 1000  # Convert to milliseconds
    print(f"Sequential execution time: {total_time} milliseconds")
    return total_sum, total_time


# Example Usage
n = 1000
num_threads = 4

# Run parallel summation
parallel_total, parallel_time = parallel_sum(num_threads, n)

# Run sequential summation for comparison
sequential_total, sequential_time = sequential_sum(n)

# Compare results
print(f"\nComparison:")
print(f"Sequential Total: {sequential_total}, Parallel Total: {parallel_total}")
print(f"Speedup: {sequential_time / parallel_time:.2f}x")
