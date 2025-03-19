from src.tasks import power

def dispatch():
    """
    Dispatch multiple power computations asynchronously using Celery.

    This function asynchronously submits tasks to compute the square of numbers
    in the range from 1 to 10,000 using Celery's `apply_async`. It then retrieves
    the results once they are completed.

    Returns:
        list[int]: A list containing the squares of numbers from 1 to 10,000.

    Example:
        >>> results = dispatch()
        >>> results[:5]  # First five results
        [1, 4, 9, 16, 25]
    """
    results_objs= [
        power.apply_async((number, 2)) for number in range(1, 10001)
    ]

    results = [
        result.get() for result in results_objs
    ]

    return results