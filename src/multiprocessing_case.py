import time
import multiprocessing
from .worker import worker

def multiprocessing_case(num_processes=2, num_numbers=1000):
    print(f"\nStarting all {num_processes} processes...")

    total_start_time = time.time()
    task_divided = num_numbers // num_processes
    processes = []
    
    # Create a Manager to share results between processes
    with multiprocessing.Manager() as manager:
        results = manager.list()  # Shared list to store partial sums

        for i in range(num_processes):
            start = i * task_divided + 1
            end = start + task_divided
            if i == num_processes - 1:
                end = num_numbers + 1  # Handle the remaining numbers in the last process

            # Create and start the process
            process = multiprocessing.Process(target=worker, args=(start, end, results))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        total_sum = sum(results)
        print(f">> Final sum: {total_sum}")

        total_end_time = time.time()  # Capture the time after all processes have finished
        total_time = (total_end_time - total_start_time) * 1000  # Convert to milliseconds
        print(f">> Time taken: {total_time} milliseconds")

    return total_time
