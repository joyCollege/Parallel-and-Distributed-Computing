from mpi4py import MPI
import numpy as np
from src.square import square

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() #number of processes 

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

    

# mpirun -n 6 python main.py