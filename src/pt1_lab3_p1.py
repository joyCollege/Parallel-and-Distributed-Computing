import time
from pt1_sequential_case import sequential_case
from src.pt1_threading_case import threading_case
from pt1_multiprocessing_case import multiprocessing_case
from calc_print_analysis import print_analysis

def lab3_1():
    """
    Runs performance tests for different parallelization strategies (sequential, threading, and multiprocessing) 
    over a specified number of iterations (1 million).

    The function:
    1. Executes a sequential case to measure the baseline execution time.
    2. Iterates over a range of thread/process counts (2 to 5) to evaluate the performance of threading and multiprocessing.
    3. Measures and compares the execution times for the threaded and multiprocessing approaches.
    4. Prints analysis of the performance, showing the portion of parallelization achieved in each case.
    
    Args:
        None
    
    Prints:
        Performance analysis for each threading and multiprocessing case, comparing their parallelized portion 
        and execution time relative to the non-parallelized baseline.
    """

    n = 1000000
    print("*"*70)
    print("*"*20, 'Part 1: Adding {n} numbers', "*"*20)
    print("*"*70, "\n")

    ts = sequential_case(num_numbers=n)
    for i in [2, 3, 4, 5]:
        non_parallelized_time = time.time()

        threading_case_parallelized_time = time.time()
        threading_case_time= threading_case(num_threads=i, num_numbers=n)
        threading_case_parallelized_time = (time.time() - threading_case_parallelized_time) 

        
        multiprocessing_case_parallelized_time = time.time()
        multiprocessing_case_time= multiprocessing_case(num_processes=i, num_numbers=n)
        multiprocessing_case_parallelized_time = (time.time() - multiprocessing_case_parallelized_time) 

        non_parallelized_time = (time.time() - non_parallelized_time) 

        print_analysis(num_actions=i, serial_time=ts, 
                parallel_time=threading_case_time, 
                parallelized_portion=threading_case_parallelized_time/(non_parallelized_time-multiprocessing_case_parallelized_time), 
                title=f"Threading {i}")
        print_analysis(num_actions=i, 
                serial_time=ts, 
                parallel_time=multiprocessing_case_time, 
                parallelized_portion=multiprocessing_case_parallelized_time/(non_parallelized_time-threading_case_parallelized_time), 
                title=f"Multiprocessing {i}")
