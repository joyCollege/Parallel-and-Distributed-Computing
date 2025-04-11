def calc_speadup(ts, tp):
    """
    Calculates the speedup of a parallel system.

    Speedup measures the performance gain when using parallel execution 
    compared to sequential execution.

    Parameters:
    ts (float): Execution time of the sequential program.
    tp (float): Execution time of the parallel program.

    Returns:
    float: The speedup factor.
    """
    return ts/tp