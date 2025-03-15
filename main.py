from src.sequential import sequential_run

LIST_SIZE = 10**6

num_list = [i for i in range(1, LIST_SIZE+1)]

sequential_time, sequential_list = sequential_run(num_list)

