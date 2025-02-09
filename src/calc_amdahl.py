def calc_amdahl(n, part_parallelized):
     return 1 / ((1 - part_parallelized) + (part_parallelized / n))