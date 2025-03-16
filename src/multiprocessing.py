from time import time
from .square import square
import multiprocessing

def worker(n, returnList):
    """
    Worker function to compute the square of a given number.

    Parameters:
    n (int or float): The number to be squared.
    returnList (multiprocessing.Manager().list): A shared list to store the squared result.

    Returns:
    None: The result is stored in the shared list.
    """
    result = square(n)
    returnList[n-1] = result

def multiprocessing_run(numlist):
    """
    Computes the square of each number in the given list using multiprocessing.

    **Warning:** The number of processes (i.e., numbers to be squared) must be limited, 
    as creating too many processes can lead to a memory error due to insufficient space.

    Parameters:
    numlist (list of int or float): A list of numbers to be squared.

    Returns:
    tuple: (execution time in seconds, list of squared numbers)
    """
    parallel_time = time()
    
    manager = multiprocessing.Manager()
    returnList = manager.list([None] * len(numlist))
    processes = []
    
    # A process for each number
    for n in numlist:
        process = multiprocessing.Process(target=worker, args=(n, returnList))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
        
    parallel_time = time() - parallel_time
    
    print(f"{'multiprocessing_run:'.ljust(20)} {parallel_time:2f}s to square until {len(numlist)}. The last 3 squares {list(returnList)[-3:]}")
    return parallel_time, list(returnList)