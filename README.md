# Celery Lab Tutorial
## DSAI3202: Parallel and Distribute
## Dela Cruz, Joy Anne [600301959]

This project demonstrates how to use **Celery** to run tasks in the background. Instead of making your program wait for a task to finish, Celery allows you to send tasks to a worker, which processes them separately.

## What This Project Does
- It calculates the square of numbers from **1 to 10,000** asynchronously.
- Uses **Celery** to handle the tasks in the background.
- Stores the results in **Redis** so they can be accessed later.

## How It Works
1. The **main script** (`main.py`) starts the process.
2. It calls the **dispatch function** (`dispatch_tasks.py`), which sends tasks to Celery.
3. Celery **workers** pick up the tasks and compute the results.
4. The results are stored and later retrieved when needed.

## Why Use Celery?
- **Faster Execution:** Instead of waiting for each calculation to finish, Celery processes multiple tasks at the same time.
- **Scalability:** Can be expanded to handle thousands of tasks efficiently.
- **Asynchronous Processing:** The main program does not get stuck waiting for results.

## Running the Project
1. **Start Celery:**
   ```sh
   celery -A src.tasks worker --loglevel=info
   ```
2. **Run the script:**
   ```sh
   python main.py
   ```
3. **See the first 10 results printed on the screen.**

## Summary
This project is a simple example of how Celery can be used to process tasks efficiently in the background. It is useful for applications that need to handle large amounts of calculations without slowing down.



## Runing

In a VM terminal, open a redis-server
```bash
(base) student@vg-DSAI-3202-32:~/Parallel-and-Distributed-Computing$ conda activate parallel
(parallel) (base) student@vg-DSAI-3202-32:~/Parallel-and-Distributed-Computing$ redis-server --port 6380
...
```

In a local terminal, connect the localhost
```bash
C:\Users\Joy Anne>ssh -L 15672:localhost:15672 student@10.102.0.169
```

In another VM terminal, 
```bash
(base) student@vg-DSAI-3202-32:~/Parallel-and-Distributed-Computing$ conda activate parallel
(parallel) (base) student@vg-DSAI-3202-32:~/Parallel-and-Distributed-Computing$ celery -A src.tasks worker --loglevel=info
...
```

In another another VM terminal
```bash
(base) student@vg-DSAI-3202-32:~/Parallel-and-Distributed-Computing$ conda activate parallel
(parallel) (base) student@vg-DSAI-3202-32:~/Parallel-and-Distributed-Computing$ python3 main.py
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
(parallel) (base) student@vg-DSAI-3202-32:~/Parallel-and-Distributed-Computing$ 
```