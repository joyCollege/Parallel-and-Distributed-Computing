def calc_efficiency(s, p):
    """
    Calculates the efficiency of a parallel system.

    Efficiency measures how effectively the processors are utilized when 
    executing a parallelized program.

    Parameters:
    s (float): Speedup of the system.
    p (int or float): Number of processors.

    Returns:
    float: Efficiency of the parallel system (0 to 1).
    """
    return s/p