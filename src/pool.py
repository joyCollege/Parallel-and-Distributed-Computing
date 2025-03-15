from time import time
from .square import square
import multiprocessing

def pool_map_run(numlist):
    parallel_time = time()
    
    pool = multiprocessing.Pool()
    returnList = pool.map(square, numlist)
    
    pool.close()
    pool.join()
    
    parallel_time = time() - parallel_time
    print(f"{'pool_map_run:'.ljust(20)} {parallel_time:2f}s to square until {len(numlist)}. The last 3 squares {list(returnList)[-3:]}")
    return parallel_time, returnList

def pool_apply_run(numlist):
    parallel_time = time()
    
    pool = multiprocessing.Pool()
    returnList = []

    for n in numlist:
        result = pool.apply(square, (n,))
        returnList.append(result)
        
    pool.close()
    pool.join()
    
    parallel_time = time() - parallel_time
    print(f"{'pool_apply_run:'.ljust(20)} {parallel_time:2f}s to square until {len(numlist)}. The last 3 squares {list(returnList)[-3:]}")
    return parallel_time, returnList