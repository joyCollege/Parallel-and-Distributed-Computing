from mpi4py import MPI
import numpy as np
import time
import os

def square(arr):
    return arr ** 2  # Vectorized NumPy operation
    
# Set the time limit in seconds
TIME_LIMIT = 60
start_time = time.time()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Each process will store its computed results as a list of tuples (n, square(n))
local_results = []
# Start at a different number based on rank to distribute work
n = rank

# Continue computing until the time limit is reached
print("Calculating the squares", end="")
while time.time() - start_time < TIME_LIMIT:
    local_results.append((n, square(n)))
    n += size  # This ensures different processes compute different numbers

# Gather all results at the root process
all_results = comm.gather(local_results, root=0)

if rank == 0:
    # Flatten the list of lists
    flat_results = [item for sublist in all_results for item in sublist]
    # Optionally, sort the results by the original number
    flat_results.sort(key=lambda x: x[0])
    
    # Print a summary of the computed results
    print(f"Total squares computed: {len(flat_results)}")
    print("First 10 results:", flat_results[:10])
    print("Last 10 results:", flat_results[-10:])
    
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")
