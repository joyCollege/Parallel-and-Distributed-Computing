from time import time
from .square import square
import concurrent.futures
import numpy as np

def pool_ex_run(numlist, chunk_size=10000):
    """
    Uses ProcessPoolExecutor to apply the square function in parallel using chunks.

    Parameters:
    numlist (list): List of numbers to be squared.
    chunk_size (int): Size of each chunk to process in parallel (default is 10,000).

    Returns:
    tuple: Execution time and list of squared numbers.

    Note:
    - Splitting into chunks helps prevent excessive memory usage.
    - ProcessPoolExecutor manages worker processes efficiently.
    - Number of processes should be limited to avoid memory errors.
    """
    parallel_time = time()
    
    returnList = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for chunk in np.array_split(numlist, max(1, len(numlist) // chunk_size)):
            returnList.extend(executor.map(square, chunk))
    
    parallel_time = time() - parallel_time
    print(f"{'pool_ex_run:'.ljust(22)} {parallel_time:.2f}s to square until {len(numlist)}. The last 3 squares {returnList[-3:]}")
    return parallel_time, returnList