#!/bin/bash

cd ~
scp -r workingLab5 student@10.102.0.217:~/
scp -r workingLab5 student@10.102.0.167:~/
scp -r workingLab5 student@10.102.0.150:~/
cd workingLab5
echo "Done with scp commands. Now running main.py..." 
mpirun -hostfile machines.txt -np 24 python3 main.py | tee output_after_300_seconds.txt