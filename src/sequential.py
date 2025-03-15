from time import time
from .square import square

def sequential_run(numlist):
    sequential_time = time()

    returnList = []
    for n in numlist:
        returnList.append(square(n))

    sequential_time = time() - sequential_time

    print(f"{'sequential_run:'.ljust(20)} {sequential_time:2f}s to square until {len(numlist)}. The last 3 squares {returnList[-3:]}")
    return sequential_time, returnList