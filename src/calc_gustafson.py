def calc_gustafson(p, part_nonparallelized):
    """
    Calculates the speedup according to Gustafson's Law.

    Gustafson's Law states that the speedup of a parallel system increases 
    with the number of processors, considering that the problem size scales 
    with the number of processors.

    Parameters:
    p (int or float): Number of processors.
    part_nonparallelized (float): Fraction of the program that cannot be parallelized (0 to 1).

    Returns:
    float: The theoretical speedup factor.
    """
    return p + part_nonparallelized * (1 - p)