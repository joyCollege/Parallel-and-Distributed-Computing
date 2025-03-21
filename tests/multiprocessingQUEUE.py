import multiprocessing as mp
from time import time
from .square import square

def worker(task_queue, result_queue):
    """Worker process: Fetches tasks from queue and computes squares."""
    while True:
        n = task_queue.get()
        if n is None:  # Sentinel to signal termination
            break
        result_queue.put((n, square(n)))

def multiprocessing_run(numlist, num_workers=mp.cpu_count()):
    start_time = time()

    # Create queues
    task_queue = mp.Queue(maxsize=1000)  # Limit queued tasks to prevent memory overload
    result_queue = mp.Queue()

    # Start worker processes (bounded to num_workers)
    workers = []
    for _ in range(num_workers):
        p = mp.Process(target=worker, args=(task_queue, result_queue))
        p.start()
        workers.append(p)

    # Feed tasks into the task queue
    for n in numlist:
        task_queue.put(n)

    # Add sentinels (None) to tell workers to exit
    for _ in range(num_workers):
        task_queue.put(None)

    # Collect results dynamically to avoid memory spikes
    return_list = []
    for _ in numlist:
        return_list.append(result_queue.get())

    # Ensure all worker processes finish
    for p in workers:
        p.join()

    return_list.sort()  # Sort since Queue doesn't preserve order

    elapsed_time = time() - start_time
    print(f"{'parallel_run:'.ljust(20)} {elapsed_time:.2f}s to square until {len(numlist)}. The last 3 squares {return_list[-3:]}")
    return elapsed_time, return_list
