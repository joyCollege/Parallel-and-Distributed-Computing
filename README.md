# Lab Tutorial: Distributed Square Computation with MPI
## DSAI3202: Parallel and Distributed Computing
## By: Dela Cruz, Joy Anne P. [60301959]

This project computes the squares of numbers in parallel using MPI (Message Passing Interface). The computation is distributed across multiple machines, with each machine performing part of the computation. The results are gathered at the root process, sorted, and displayed. This example demonstrates how to set up a parallel computing environment using MPI and NumPy.

## Requirements
```bash
conda activate parallel
pip install -r requirements.txt
```

## Running the Program

1. Clone or download this repository to your local machine.
2. The program uses MPI to distribute computation, so you'll need to execute it using `mpirun` or `mpiexec`.
3. To run the program, use the following command:
   ```bash
   mpirun -n 6 python main.py
   ```

   This will execute the program using 6 MPI processes. You can adjust the number of processes based on the available cores.

## How It Works

1. The `numbers` array is distributed using `MPI.Scatter()` to all processes.
2. Each process computes the square of the assigned number.
3. Each process sends its result to the root process using `MPI.isend()` and `MPI.irecv()`.
4. The root process collects the results and displays them.

### Output Example
The output will display the rank of each process and the numbers being processed, followed by the computed squares and the gathered results at the root process:
```
rank: 0 of 6
numbers: [0 1 2 3 4 5]
number: [0]
square of 0 is 0
...
results: [0, 1, 4, 9, 16, 25]
```

## Notes

- **Parallel Execution**: This program distributes tasks among multiple processes to speed up computation.
- **Random Delay**: Each process includes a random delay (`time.sleep()`) to simulate work and avoid synchronization issues during testing.