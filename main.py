import time
from src.sequential_case import sequential_case
from src.threading_case import threading_case
from src.multiprocessing_case import multiprocessing_case
from src.print_analysis import print_analysis

def lab3_1():
    n = 1000000
    print(f"\n**************** Running {n} times ****************")
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
lab3_1()