# celery lab

working on.....

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