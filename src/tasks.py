from celery import Celery

app = Celery("tasks", broker = "pyamqp://guest@localhost//", backend='redis://localhost:6379/#' )

@app.task
def power(n, e):
    """
    Compute the power of a number.

    This function takes a base number `n` and raises it to the exponent `e`.

    Args:
        n (int): The base number.
        e (int): The exponent.

    Returns:
        int: The result of `n` raised to the power of `e`.

    Example:
        >>> power(2, 3)
        8
    """
    return n ** e