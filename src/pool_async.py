from time import time
from .square import square
import multiprocessing

def pool_map_async_run(numlist):
    parallel_time = time()
    
    pool = multiprocessing.Pool()
    returnList = pool.map_async(square, numlist).get()
    
    pool.close()
    pool.join()
    
    parallel_time = time() - parallel_time
    print(f"{'pool_map_async_run:'.ljust(20)} {parallel_time:2f}s to square until {len(numlist)}. The last 3 squares {list(returnList)[-3:]}")
    return parallel_time, returnList

def pool_apply_async_run(numlist):
    parallel_time = time()
    
    pool = multiprocessing.Pool()
    async_results = [pool.apply_async(square, (n,)) for n in numlist]
    returnList = [res.get() for res in async_results] 
   
    pool.close()
    pool.join()
    
    parallel_time = time() - parallel_time
    print(f"{'pool_apply_async_run:'.ljust(20)} {parallel_time:2f}s to square until {len(numlist)}. The last 3 squares {list(returnList)[-3:]}")
    return parallel_time, returnList