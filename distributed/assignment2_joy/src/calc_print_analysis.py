from src.calc_speedup import calc_speadup
from src.calc_efficiency import calc_efficiency

def calc_print_analysis(serial_time, parallel_time, title):
    """
    Perform and print performance analysis based on speedup, efficiency, Amdahl’s speedup, and Gustafson’s speedup.

    :param num_actions: Number of processes or threads used in the parallel execution.
    :param serial_time: Time taken for the serial (single-threaded) execution.
    :param parallel_time: Time taken for the parallel execution.
    :param title: The title to be printed at the start of the analysis (e.g., "Threading Performance Analysis").
    """
    print(f"\n**************** {title} Performance Analysis ****************")
    speedup = calc_speadup(serial_time, parallel_time)
    efficiency = calc_efficiency(speedup, 6)
    
    # Print the results
    print(f"Speedup             {speedup:.16f}")
    print(f"Efficiency          {efficiency:.16f}")
