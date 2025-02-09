def calc_amdahl(p, part_parallelized):
     """
    Calculates the speedup according to Amdahl's Law.

    Parameters:
    p (int or float): Number of processors.
    part_parallelized (float): Fraction of the program that can be parallelized (0 to 1).

    Returns:
    float: The theoretical speedup factor.
    """
     return 1 / ((1 - part_parallelized) + (part_parallelized / p))