# Assignment 1 - Part 1 
## DSAI3202 - Parallel and Distributed Computing
## By: Dela Cruz, Joy Anne 60301959

### Overview
This assignment explores parallel and distributed computing techniques to enhance performance in computational tasks. It compares different multiprocessing approaches, focusing on squaring a list of numbers using various parallelization techniques.

### Objectives
- Implement and compare sequential and parallel approaches for squaring numbers.
- Utilize Python's `multiprocessing` module to handle parallel computations efficiently.
- Analyze execution times for different methods and discuss performance trade-offs.
- Simulate a database connection pool using semaphores to manage concurrent access.

### Implemented Methods

#### 1. **Sequential Processing**
   - Directly computes the square of numbers using a loop.
   - Measures execution time as a baseline for comparison.

#### 2. **Multiprocessing Techniques**
   - **Direct Process Creation**: Creates a separate process for each number to compute its square.
   - **Process Pooling**: Utilizes `Pool.map()` and `Pool.apply()` for efficient task distribution.
   - **Asynchronous Processing**: Uses `Pool.map_async()` and `Pool.apply_async()` to execute tasks asynchronously.
   - **Executor-Based Multiprocessing**: Implements parallel execution using `concurrent.futures.ProcessPoolExecutor`.

#### 3. **Database Connection Simulation**
   - Implements a connection pool using semaphores to limit the number of concurrent database connections.
   - Simulates processes requesting and releasing database connections.

### Files and Functions
| File | Description |
|------|-------------|
| `square.py` | Contains the `square(n)` function to compute squares. |
| `sequential.py` | Implements sequential execution of squaring numbers. |
| `multiprocessing.py` | Handles process-based parallel execution. |
| `pool.py` | Implements `Pool.map()` and `Pool.apply()` approaches. |
| `pool_async.py` | Uses asynchronous processing with `Pool.map_async()`. |
| `pool_ex.py` | Implements multiprocessing using `concurrent.futures.ProcessPoolExecutor`. |
| `connectionPool.py` | Simulates a database connection pool with semaphores. |
| `main.py` | Runs all methods, measures execution times, and performs analysis. |

### Usage Instructions
1. Ensure Python 3 is installed.
2. Install required dependencies (if any).
3. Run `main.py` to execute all methods and view performance results:
   ```sh
   python3 main.py
   ```
4. Compare execution times printed in the console.

### Expected Output
- Execution time for sequential and parallel methods.
- Performance analysis of different multiprocessing techniques.
- Simulated database access logs.

### Conclusion
When squaring 10^6 numbers, the sequential run is the fastest, running for 0.061s, because squaring numbers is not a CPU-intensive task; the overhead introduced by multiprocessing, like inter-process communication, slows down the execution. When doing multiprocessing, applying a process per number is not very practical because memory cannot handle one million processes and it crashes. To fix that, pooling was applied which allows reusing worker processes instead of creating new ones for every task.

Note: I tried to make multiprocessing work with queue which you can see in the tests folder and commits

First, I applied synchronous pools where blocking is allowed. Pool.map() (0.162s) performed better than Pool.apply() (167.38s) because the Pool.map() distributes the task better whereas Pool.apply() sends the task one by one. Even though Pool.map() was better, it is still slower than the sequential approach due to the IPC slowing the execution down. 

Then, the same multiprocessing pools are implemented but asynchronously. Pool.map_async() (0.172s) did not improve as it was already distributing the tasks efficienty before allowing non-blocking processes. Pool.apply_async(), however, significantly preformed better than the synchronous Pool.apply(), reducing execution time 3x from 167.38s to 53.75s. This is because asynchronous execution allows multiple tasks to be submitted without waiting for each one to complete sequentially.

Using concurrent.futures.ProcessPoolExecutor, we achieved a time of 127.65s, which is slightly faster than Pool.apply() but still the second slowest approach overall.

Overall, the communication overhead in multiprocessing outweighs its benefits for a non-CPU intensive task like squaring numbers. Parallel processing is more beneficial for truly CPU-bound problems where computations per task are significantly larger not for squaring numbers

Moving on to the next task, a simulatulation of a database connection pool is created with semaphores. With semaphores, if more processes try to access the pool than there are available connections the extra processe swill wait until a working process releases the lock. Since we have 6 cores, the maximum number of connection at any current time is 6. This prevents race conditions and ensure safe access to the connections by enforcing a limit on the number of processes running. With get_connection(), a process acquire one of the sixe sempahores; when are are no semaphores left, the other processes have to wait. When a running process is done, it releases its semaphore with release_connection() and another process waiting can get the connection. This approach guarantees that no process overwrites another process's changes in the database.
