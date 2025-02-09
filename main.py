from src.sequential_case import sequential_case
from src.threading_case import threading_case
from src.advanced_threading_case import advanced_threading_case
from src.multiprocessing_case import multiprocessing_case
from src.advanced_multiprocessing_case import advanced_multiprocessing_case
from src.calc_speadup import calc_speadup
from src.calc_efficiency import calc_efficiency
from src.calc_amdahl import calc_amdahl
from src.calc_gustafson import calc_gustafson

# if __name__ == '__main__':
n = 1000000

print(f"\n**************** Running {n} times ****************")
ts = sequential_case(n)
tp_threading = threading_case(n)
tp_advanced_threading = advanced_threading_case(n)
tp_multiprocessing = multiprocessing_case(n)
tp_advanced_multiprocessing = advanced_multiprocessing_case(n)
0
print("\n**************** Threading Performance Analysis ****************")
p_threading=2
s_threading = calc_speadup(ts, tp_threading)
e_threading = calc_efficiency(s_threading, p_threading)
amdahl_threading = calc_amdahl(s_threading, tp_threading)
gustafson_threading = calc_gustafson(p_threading, s_threading)
print("Speadup             ", s_threading)
print("Efficiency          ", e_threading)
print("Amdhal’s speedup    ", amdahl_threading)
print("Gustaffson’s speedup", gustafson_threading)

print("\n**************** Advanced Threading Performance Analysis ****************")
p_advanced_threading=4
s_advanced_threading = calc_speadup(ts, tp_advanced_threading)
e_advanced_threading = calc_efficiency(s_advanced_threading, p_advanced_threading)
amdahl_advanced_threading = calc_amdahl(p_advanced_threading, 12/18)
gustafson_advanced_threading = calc_gustafson(p_advanced_threading, 12/18)
print("Speadup             ", s_advanced_threading)
print("Efficiency          ", e_advanced_threading)
print("Amdhal’s speedup    ", amdahl_advanced_threading)
print("Gustaffson’s speedup", gustafson_advanced_threading)

print("\n**************** Multiprocessing Performance Analysis ****************")
p_multiprocessing=2
s_multiprocessing = calc_speadup(ts, tp_multiprocessing)
e_multiprocessing = calc_efficiency(s_multiprocessing, p_multiprocessing)
amdahl_multiprocessing = calc_amdahl(p_multiprocessing, 6/12)
gustafson_multiprocessing = calc_gustafson(p_multiprocessing, 6/12)
print("Speadup             ", s_multiprocessing)
print("Efficiency          ", e_multiprocessing)
print("Amdhal’s speedup    ", amdahl_multiprocessing)
print("Gustaffson’s speedup", gustafson_multiprocessing)

print("\n**************** Advanced Multiprocessing Performance Analysis ****************")
p_advanced_multiprocessing=4
s_advanced_multiprocessing = calc_speadup(ts, tp_advanced_multiprocessing)
e_advanced_multiprocessing = calc_efficiency(s_advanced_multiprocessing, p_advanced_multiprocessing)
amdahl_advanced_multiprocessing = calc_amdahl(p_advanced_multiprocessing, 12/18)
gustafson_advanced_multiprocessing = calc_gustafson(p_advanced_multiprocessing, 12/18)
print("Speadup             ", s_advanced_multiprocessing)
print("Efficiency          ", e_advanced_multiprocessing)
print("Amdhal’s speedup    ", amdahl_advanced_multiprocessing)
print("Gustaffson’s speedup", gustafson_advanced_multiprocessing)

# # multiprocessing
# p_multiprocessing=2
...
# print (f"The speed up for multiprocessing case is: {calc_speadup(ts, tp_multiprocessing)}.")


