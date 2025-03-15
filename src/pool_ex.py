from time import time
from .square import square
import concurrent.futures

def pool_ex_run(numlist):
    parallel_time = time()
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        returnList = list(executor.map(square, numlist))
    
    parallel_time = time() - parallel_time
    print(f"{'pool_ex_run:'.ljust(20)} {parallel_time:2f}s to square until {len(numlist)}. The last 3 squares {returnList[-3:]}")
    return parallel_time, returnList