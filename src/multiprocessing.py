from time import time
from .square import square
import multiprocessing

def worker(n, returnList):
    result = square(n)
    returnList[n-1] = result

def multiprocessing_run(numlist):
    parallel_time = time()
    
    manager = multiprocessing.Manager()
    returnList = manager.list([None] * len(numlist))
    processes = []
    
    # A process for each number
    for n in numlist:
        p = multiprocessing.Process(target=worker, args=(n, returnList))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
        
    parallel_time = time() - parallel_time
    
    print(f"{'multiprocessing_run:'.ljust(20)} {parallel_time:2f}s to square until {len(numlist)}. The last 3 squares {list(returnList)[-3:]}")
    return parallel_time, list(returnList)