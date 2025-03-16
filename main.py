from src.calc_print_analysis import calc_print_analysis
from src.sequential import sequential_run
from time import time

from src.connectionPool import ConnectionPool, access_database
from multiprocessing import Process

LIST_SIZE = 10**7
NUM_PROCESSES = 700

if __name__ == '__main__':
    """
    Main script to compare different multiprocessing approaches for squaring numbers and simulating database operations.

    The script:
    1. Generates a list of numbers up to LIST_SIZE.
    2. Runs different multiprocessing techniques to square numbers, including:
    - Sequential processing
    - Multiprocessing with direct process creation
    - Multiprocessing with Pool methods (map, apply, async)
    - Multiprocessing with an Executor-based approach
    3. Measures and compares execution times across these methods.
    4. Simulates a database connection pool using semaphores, where multiple processes request and release connections.

    Constants:
        LIST_SIZE (int): The size of the list of numbers to be squared.
        NUM_PROCESSES (int): The number of processes simulating database access.

    Outputs:
        - Execution times for each method.
        - Last three squared numbers for validation.
        - Performance analysis comparing different parallelization methods.
        - Simulated database access log.

    Note:
        Creating too many processes (e.g., LIST_SIZE number of processes) may lead to memory errors.
    """
    print(
"""
====================================================================================
SQUARE PROGRAMS USING MULTIPROCESSING AND CONCURRENT FUTURES
====================================================================================
"""
    )
    num_list = [i for i in range(1, LIST_SIZE+1)]

    sequential_time, sequential_list = sequential_run(num_list)

    from src.multiprocessing import multiprocessing_run

    # multiprocessing_totalTime = time()
    # multiprocessing_time, multiprocessing_list = multiprocessing_run(num_list)
    # multiprocessing_totalTime = time() - multiprocessing_totalTime
    # multiprocessing_successful = True

    print(f"********* multiprocessing_run couldn't make {LIST_SIZE} processes *********")
    multiprocessing_successful = False

        

    from src.pool import pool_map_run, pool_apply_run
    pool_map_totalTime = time()
    pool_map_time, pool_map_list = pool_map_run(num_list)
    pool_map_totalTime = time() - pool_map_totalTime

    pool_apply_totalTime = time()
    pool_apply_time, pool_apply_list = pool_apply_run(num_list)
    pool_apply_totalTime = time() - pool_apply_totalTime

    from src.pool_async import pool_map_async_run, pool_apply_async_run
    pool_map_async_totalTime = time()
    pool_map_async_time, pool_map_async_list = pool_map_async_run(num_list)
    pool_map_async_totalTime = time() - pool_map_async_totalTime

    pool_apply_async_totalTime = time()
    pool_apply_async_time, pool_apply_async_list = pool_apply_async_run(num_list)
    pool_apply_async_totalTime = time() - pool_apply_async_totalTime

    from src.pool_ex import pool_ex_run
    pool_ex_totalTime = time()
    pool_ex_time, pool_ex_list = pool_ex_run(num_list)
    pool_ex_totalTime = time() - pool_ex_totalTime

    if multiprocessing_successful: calc_print_analysis(sequential_time, multiprocessing_time, multiprocessing_time/(multiprocessing_totalTime), "multiprocessing_run")
    calc_print_analysis(sequential_time, pool_map_time, pool_map_time/(pool_map_totalTime), "pool_map_run")
    calc_print_analysis(sequential_time, pool_apply_time, pool_apply_time/(pool_apply_totalTime), "pool_apply_run")
    calc_print_analysis(sequential_time, pool_ex_time, pool_ex_time/(pool_ex_totalTime), "pool_ex_run")
    calc_print_analysis(sequential_time, pool_map_async_time, pool_map_async_time/(pool_map_async_totalTime), "pool_map_async_run")
    calc_print_analysis(sequential_time, pool_apply_async_time, pool_apply_async_time/(pool_apply_async_totalTime), "pool_apply_async_run")

    print(
"""
====================================================================================
SIMULATED DATABASE OPERATION WITH SEMAPHORES
====================================================================================
"""
    )

    pool = ConnectionPool(max_connections=6)
    processes = []
    
    for i in range(NUM_PROCESSES):
        process = Process(target=access_database, args=(pool,), name=f"Process-{i+1}")
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()