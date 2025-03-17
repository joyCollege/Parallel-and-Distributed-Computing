# Lab 5: Distributed Square Computation with MPI
## DSAI3202: Parallel and Distributed Computing
## By: Dela Cruz, Joy Anne P. [60301959]

This project computes the squares of numbers in parallel using MPI (Message Passing Interface). The computation is distributed across multiple machines, with each machine performing part of the computation. The results are gathered at the root process, sorted, and displayed. This example demonstrates how to set up a parallel computing environment using MPI and NumPy.

## Setup and Execution

To run this program, the `main.py` script must be placed in a shared directory accessible by all computers in the cluster. Additionally, you need to use the provided `scp_and_run.sh` script to copy the necessary files to each machine and run the computations across multiple nodes.

## Requirements
```bash
conda activate parallel
pip install -r requirements.txt
```

### Folder Structure

Ensure the folder `workingLab5` is set up correctly on the shared network and contains the `main.py` file for computation.

### Step 1: Copy the Files to the Cluster

The `scp_and_run.sh` script is used to securely copy the `workingLab5` folder to the cluster nodes and then execute the `main.py` script on the cluster.

#### SCP and Execution Script (`scp_and_run.sh`)

```bash
#!/bin/bash

cd ~
scp -r workingLab5 student@10.102.0.217:~/
scp -r workingLab5 student@10.102.0.167:~/
scp -r workingLab5 student@10.102.0.150:~/
cd workingLab5
echo "Done with scp commands. Now running main.py..." 
mpirun -hostfile machines.txt -np 24 python3 main.py | tee output_after_300_seconds.txt
```

#### Explanation of the Script:
1. It copies the `workingLab5` directory to three remote machines using `scp`.
2. It then runs `main.py` on the cluster using `mpirun`, specifying the number of processes (`-np 24`) and a host file (`machines.txt`) that lists the cluster nodes.
3. The output of the execution is logged to `output_after_300_seconds.txt`.

### Step 2: Configuration Files

- **machines.txt**: This file should contain the list of IPs or hostnames for the machines in your cluster. For example:
  ```
  10.102.0.217
  10.102.0.167
  10.102.0.150
  ```
  Make sure that the file is placed in the same directory as `scp_and_run.sh` and contains the correct machine IPs.

### Step 3: Running the Program

Once the files are copied to the cluster and the environment is set up, execute the `scp_and_run.sh` script from your terminal:
```bash
bash scp_and_run.sh
```

This will copy the `workingLab5` directory to the remote machines and start the MPI-based computation across the cluster.

### Output

The results of the computation will be printed on the terminal, and a log file (`output_after_300_seconds.txt`) will be generated, containing the output of the `main.py` script.

### Example Output
The program will print the total number of squares computed, and display the first and last 10 computed squares:
```
Calculating the squares... 
Total squares computed: 10000
First 10 results: [(0, 0), (24, 576), (48, 2304), (72, 5184), ...]
Last 10 results: [(9996, 99920016), (10020, 100400400), ...]
Total time taken: 60.0234 seconds
```

## Notes

- **Cluster Configuration**: Ensure that all cluster nodes are properly configured and have access to the shared folder where `workingLab5` resides.
- **Time Limit**: The computation continues until the set time limit (300 seconds) is reached, which you can adjust in the `main.py` script.
- **MPI Processes**: The script uses `24` processes as specified by `-np 24`. Adjust the number based on the number of available cores in your cluster.
