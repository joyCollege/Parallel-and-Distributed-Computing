from celery import Celery

app = Celery("tasks", broker = "pyamqp://guest@localhost//", backend='rpc://' )

@app.task
def power(n, e):
    return n ** e