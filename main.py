from src.tasks import power
from src.dispatch_tasks import dispatch

if __name__ == "__main__":
    results = dispatch()
    print(results[:10])

# ssh -L 15672:localhost:15672 student@10.102.0.169
# celery -A tasks worker --loglevel=info
# "all alone" means this is not distributed