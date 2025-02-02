from src.sequential_case import sequential_case
from src.threading_case import threading_case
from src.multiprocessing_case import multiprocessing_case
from src.calc_speadup import calc_speadup
from src.calc_efficiency import calc_efficiency
from src.calc_amdahl import calc_amdahl
from src.calc_gustafson import calc_gustafson

# if __name__ == '__main__':
n = 1000
ts = sequential_case(n)

p_threading=2
tp_threading = threading_case(n)
s_threading = calc_speadup(ts, tp_threading)
e_threading = calc_efficiency(s_threading, p_threading)
amdahl_threading = calc_amdahl(s_threading, tp_threading)
gustafson_threading = calc_gustafson(p_threading, s_threading)

p_multiprocessing=2
tp_multiprocessing = multiprocessing_case(n)
# ...

# threading  
# print (f"The speed up for threading case is: {s_threading}.")
# print (f"The efficiency up for threading case is: {e_threading}.")


# # multiprocessing
# print (f"The speed up for multiprocessing case is: {calc_speadup(ts, tp_multiprocessing)}.")


