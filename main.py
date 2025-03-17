from mpi4py import MPI
import numpy as np
from src.square import square

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() #number of processes 

if __name__ == "__main__":
    """
    Main parallel square computation using MPI.

    This program distributes the task of computing the squares of numbers across multiple processes. 
    Each process computes the square of a number, and the results are sent to the root process.

    Steps:
    1. The root process (rank 0) creates an array of numbers to be squared and scatters them across all processes.
    2. Each process computes the square of the number it received and sends the result back to the root process.
    3. The root process collects and displays the results.

    MPI operations used:
    - MPI.Scatter: Distributes data to all processes.
    - MPI.isend/irecv: Asynchronously sends and receives results between processes.

    """
    print(f"rank: {rank} of {size}")

    if rank == 0:
        numbers = np.arange(size, dtype = 'i')
    else:
        numbers = None
    print("numbers", numbers)

    number = np.zeros(1, dtype = 'i')
    comm.Scatter(numbers, number, root =0) # MPI_Bcast() sends the same piece of data to everyone, while MPI_Scatter() sends each process a part of the input array.
    print("numbers:", numbers)
    print("number:", number)

    result = square(number[0])
    print(result)
    import time 
    import random

    time.sleep(random.random())
    request = comm.isend(result, dest=0, tag=rank)

    if rank == 0:
        results = np.zeros(size, dtype = 'i')
        for i in range(size):
            results[i] = comm.irecv(source=i, tag=i).wait()
        print("results", results)

    request.wait()