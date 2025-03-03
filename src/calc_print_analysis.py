from src.calc_speedup import calc_speadup
from src.calc_efficiency import calc_efficiency
from src.calc_amdahl import calc_amdahl
from src.calc_gustafson import calc_gustafson

def calc_print_analysis(serial_time, parallel_time, parallelized_portion, title):
    """
    Perform and print performance analysis based on speedup, efficiency, Amdahl’s speedup, and Gustafson’s speedup.

    :param serial_time: Time taken for the serial (single-threaded) execution.
    :param parallel_time: Time taken for the parallel execution.
    :param parallelized_portion: The fraction of the workload that can be parallelized (between 0 and 1).
    :param title: The title to be printed at the start of the analysis (e.g., "Threading Performance Analysis").
    """
    print(f"**************** {title} Performance Analysis ****************")
    speedup = calc_speadup(serial_time, parallel_time)
    efficiency = calc_efficiency(speedup, 6)
    amdahl_speedup = calc_amdahl(6, parallelized_portion)
    gustafson_speedup = calc_gustafson(6, 1 - parallelized_portion)
    
    # Print the results
    print("Speedup            ", speedup)
    print("Efficiency         ", efficiency)
    print("Amdahl’s speedup   ", amdahl_speedup)
    print("Gustafson’s speedup", gustafson_speedup)
    print()
