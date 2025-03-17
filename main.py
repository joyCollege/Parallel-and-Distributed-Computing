from src.sequential_case import sequential_case
from src.threading_case import threading_case
from src.advanced_threading_case import advanced_threading_case
from src.multiprocessing_case import multiprocessing_case
from src.advanced_multiprocessing_case import advanced_multiprocessing_case
from src.calc_speadup import calc_speadup
from src.calc_efficiency import calc_efficiency
from src.calc_amdahl import calc_amdahl
from src.calc_gustafson import calc_gustafson

if __name__ == '__main__':
    """
    Performance Analysis of Parallel Processing Techniques

    This script compares different execution methods (sequential, threading, 
    advanced threading, multiprocessing, and advanced multiprocessing) to analyze 
    speedup, efficiency, and performance based on Amdahl’s and Gustafson’s laws.

    Execution steps:
    1. Runs a computation-intensive task sequentially.
    2. Runs the same task using threading, advanced threading, multiprocessing, 
    and advanced multiprocessing.
    3. Computes speedup, efficiency, Amdahl’s law speedup, and Gustafson’s law speedup 
    for each parallel execution technique.

    Modules used:
    - `sequential_case`: Runs the task sequentially.
    - `threading_case`: Runs the task using basic threading.
    - `advanced_threading_case`: Runs the task using optimized threading.
    - `multiprocessing_case`: Runs the task using basic multiprocessing.
    - `advanced_multiprocessing_case`: Runs the task using optimized multiprocessing.
    - `calc_speadup`: Calculates speedup.
    - `calc_efficiency`: Computes efficiency based on speedup and number of processors.
    - `calc_amdahl`: Computes theoretical speedup using Amdahl’s law.
    - `calc_gustafson`: Computes theoretical speedup using Gustafson’s law.

    Usage:
    Run the script to compare execution methods with `n = 1000000`.

    Author:
    """
    n = 1000000

    print(f"\n**************** Running {n} times ****************")
    ts = sequential_case(n)
    tp_threading = threading_case(n)
    tp_advanced_threading = advanced_threading_case(n)
    tp_multiprocessing = multiprocessing_case(n)
    tp_advanced_multiprocessing = advanced_multiprocessing_case(n)
    
    print("\n**************** Threading Performance Analysis ****************")
    p_threading=2
    s_threading = calc_speadup(ts, tp_threading)
    e_threading = calc_efficiency(s_threading, p_threading)
    amdahl_threading = calc_amdahl(6, tp_threading)
    gustafson_threading = calc_gustafson(6, s_threading)
    print("Speadup             ", s_threading)
    print("Efficiency          ", e_threading)
    print("Amdhal’s speedup    ", amdahl_threading)
    print("Gustaffson’s speedup", gustafson_threading)

    print("\n**************** Advanced Threading Performance Analysis ****************")
    p_advanced_threading=4
    s_advanced_threading = calc_speadup(ts, tp_advanced_threading)
    e_advanced_threading = calc_efficiency(s_advanced_threading, p_advanced_threading)
    amdahl_advanced_threading = calc_amdahl(6, 12/18)
    gustafson_advanced_threading = calc_gustafson(6, 12/18)
    print("Speadup             ", s_advanced_threading)
    print("Efficiency          ", e_advanced_threading)
    print("Amdhal’s speedup    ", amdahl_advanced_threading)
    print("Gustaffson’s speedup", gustafson_advanced_threading)

    print("\n**************** Multiprocessing Performance Analysis ****************")
    p_multiprocessing=2
    s_multiprocessing = calc_speadup(ts, tp_multiprocessing)
    e_multiprocessing = calc_efficiency(s_multiprocessing, p_multiprocessing)
    amdahl_multiprocessing = calc_amdahl(6, 6/12)
    gustafson_multiprocessing = calc_gustafson(6, 6/12)
    print("Speadup             ", s_multiprocessing)
    print("Efficiency          ", e_multiprocessing)
    print("Amdhal’s speedup    ", amdahl_multiprocessing)
    print("Gustaffson’s speedup", gustafson_multiprocessing)

    print("\n**************** Advanced Multiprocessing Performance Analysis ****************")
    p_advanced_multiprocessing=4
    s_advanced_multiprocessing = calc_speadup(ts, tp_advanced_multiprocessing)
    e_advanced_multiprocessing = calc_efficiency(s_advanced_multiprocessing, p_advanced_multiprocessing)
    amdahl_advanced_multiprocessing = calc_amdahl(6, 12/18)
    gustafson_advanced_multiprocessing = calc_gustafson(6, 12/18)
    print("Speadup             ", s_advanced_multiprocessing)
    print("Efficiency          ", e_advanced_multiprocessing)
    print("Amdhal’s speedup    ", amdahl_advanced_multiprocessing)
    print("Gustaffson’s speedup", gustafson_advanced_multiprocessing)


