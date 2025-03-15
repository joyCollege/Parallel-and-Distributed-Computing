from src.calc_print_analysis import calc_print_analysis
from src.sequential import sequential_run
from time import time

LIST_SIZE = 10**6
num_list = [i for i in range(1, LIST_SIZE+1)]

sequential_time, sequential_list = sequential_run(num_list)

from src.multiprocessing import multiprocessing_run
multiprocessing_totalTime = time()
multiprocessing_time, multiprocessing_list = multiprocessing_run(num_list)
multiprocessing_totalTime = time() - multiprocessing_totalTime

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

calc_print_analysis(sequential_time, multiprocessing_time, multiprocessing_time/(multiprocessing_totalTime), "multiprocessing_run")
calc_print_analysis(sequential_time, pool_map_time, pool_map_time/(pool_map_totalTime), "pool_map_run")
calc_print_analysis(sequential_time, pool_apply_time, pool_apply_time/(pool_apply_totalTime), "pool_apply_run")
calc_print_analysis(sequential_time, pool_ex_time, pool_ex_time/(pool_ex_totalTime), "pool_ex_run")
calc_print_analysis(sequential_time, pool_map_async_time, pool_map_async_time/(pool_map_async_totalTime), "pool_map_async_run")
calc_print_analysis(sequential_time, pool_apply_async_time, pool_apply_async_time/(pool_apply_async_totalTime), "pool_apply_async_run")
