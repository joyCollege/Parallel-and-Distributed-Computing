from time import time
from .square import square
import multiprocessing

def pool_map_async_run(numlist):
    """
    Asynchronously computes the square of numbers using multiprocessing's map_async.

    This function:
    - Uses `map_async()` to distribute work across CPU cores without blocking execution.
    - Collects the results asynchronously using `.get()`.
    - Closes and joins the pool after computation.
    
    Similar to `pool_map_run()`, but allows non-blocking execution.

    Args:
        numlist (list): List of numbers to be squared.

    Returns:
        tuple: Execution time (float) and list of squared values.
    """
    parallel_time = time()
    
    pool = multiprocessing.Pool()
    returnList = pool.map_async(square, numlist).get()
    
    pool.close()
    pool.join()
    
    parallel_time = time() - parallel_time
    print(f"{'pool_map_async_run:'.ljust(22)} {parallel_time:2f}s to square until {len(numlist)}. The last 3 squares {list(returnList)[-3:]}")
    return parallel_time, returnList

def pool_apply_async_run(numlist):
    """
    Asynchronously computes the square of numbers using multiprocessing's apply_async.

    This function:
    - Uses `apply_async()` to submit tasks individually and retrieve results asynchronously.
    - Calls `.get()` on each async result to collect final outputs.
    - Closes and joins the pool after computation.

    Similar to `pool_apply_run()`, but processes tasks asynchronously.

    Args:
        numlist (list): List of numbers to be squared.

    Returns:
        tuple: Execution time (float) and list of squared values.
    """
    parallel_time = time()
    
    pool = multiprocessing.Pool()
    async_results = [pool.apply_async(square, (n,)) for n in numlist]
    returnList = [res.get() for res in async_results] 
   
    pool.close()
    pool.join()
    
    parallel_time = time() - parallel_time
    print(f"{'pool_apply_async_run:'.ljust(22)} {parallel_time:2f}s to square until {len(numlist)}. The last 3 squares {list(returnList)[-3:]}")
    return parallel_time, returnList