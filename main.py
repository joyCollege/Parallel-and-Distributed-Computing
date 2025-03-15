from src.sequential import sequential_run

LIST_SIZE = 10**6

num_list = [i for i in range(1, LIST_SIZE+1)]

sequential_time, sequential_list = sequential_run(num_list)

from src.multiprocessing import multiprocessing_run
multiprocessing_time, multiprocessing_list = multiprocessing_run(num_list)

from src.pool import pool_map_run, pool_apply_run
pool_map_time, pool_map_list = pool_map_run(num_list)
pool_apply_time, pool_apply_list = pool_apply_run(num_list)

from src.pool_ex import pool_ex_run
pool_ex_time, pool_ex_list = pool_ex_run(num_list)
