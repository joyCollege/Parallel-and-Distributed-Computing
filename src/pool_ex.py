from time import time
from .square import square
import concurrent.futures

def pool_ex_run(numlist, chunk_size=10000):
    parallel_time = time()
    
    returnList = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for chunk in np.array_split(numlist, max(1, len(numlist) // chunk_size)):
            returnList.extend(executor.map(square, chunk))
    
    parallel_time = time() - parallel_time
    print(f"{'pool_ex_run:'.ljust(20)} {parallel_time:.2f}s to square until {len(numlist)}. The last 3 squares {returnList[-3:]}")
    return parallel_time, returnList