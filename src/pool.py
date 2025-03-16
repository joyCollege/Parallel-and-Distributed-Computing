from time import time
from .square import square
import multiprocessing

def pool_map_run(numlist):
    """
    Uses multiprocessing's Pool.map() to apply the square function to each number in numlist.

    Parameters:
    numlist (list): List of numbers to be squared.

    Returns:
    tuple: Execution time and list of squared numbers.

    Note:
    - Pool.map() efficiently applies the function to all elements in parallel.
    - Number of processes should be limited to avoid excessive memory usage.
    """
    parallel_time = time()
    
    pool = multiprocessing.Pool()
    returnList = pool.map(square, numlist)
    
    pool.close()
    pool.join()
    
    parallel_time = time() - parallel_time
    print(f"{'pool_map_run:'.ljust(22)} {parallel_time:2f}s to square until {len(numlist)}. The last 3 squares {list(returnList)[-3:]}")
    return parallel_time, returnList

def pool_apply_run(numlist):
    """
    Uses multiprocessing's Pool.apply() to apply the square function to each number in numlist.

    Parameters:
    numlist (list): List of numbers to be squared.

    Returns:
    tuple: Execution time and list of squared numbers.

    Note:
    - Pool.apply() runs the function in a single worker process at a time, making it less efficient than Pool.map().
    - Number of processes should be limited to prevent memory errors.
    """
    parallel_time = time()
    
    pool = multiprocessing.Pool()
    returnList = []

    for n in numlist:
        result = pool.apply(square, (n,))
        returnList.append(result)
        
    pool.close()
    pool.join()
    
    parallel_time = time() - parallel_time
    print(f"{'pool_apply_run:'.ljust(22)} {parallel_time:2f}s to square until {len(numlist)}. The last 3 squares {list(returnList)[-3:]}")
    return parallel_time, returnList