from src.tasks import power
from src.dispatch_tasks import dispatch

if __name__ == "__main__":
    """
    Main script to execute the Celery-powered dispatch function.

    This script imports the `dispatch` function, which submits multiple 
    power computations asynchronously using Celery. The first 10 results 
    are printed for quick verification.

    Example Output:
        [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    """
    results = dispatch()
    print(results[:10])

# ssh -L 15672:localhost:15672 student@10.102.0.169
# celery -A src.tasks worker --loglevel=info
# "all alone" means this is not distributed
# redis://localhost:6379/#
# lsof -i : 6379 << what is using port 