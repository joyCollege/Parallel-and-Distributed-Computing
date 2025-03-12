#!/bin/bash

cd ~
scp -r trying_stuff student@10.102.0.217:~/
scp -r trying_stuff student@10.102.0.167:~/
scp -r trying_stuff student@10.102.0.150:~/
cd trying_stuff #this would be different
echo "Done with scp commands. Now running joeystrial.py..." 
mpirun -hostfile machines.txt -np 24 python3 joeystrial.py | tee output_after_300_seconds.txt