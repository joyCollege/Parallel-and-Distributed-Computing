from src.sequential_case import sequential_case
from src.threading_case import threading_case
from src.multiprocessing_case import multiprocessing_case

n = 1000
sequential_case(n)
threading_case(n)
multiprocessing_case(n)
