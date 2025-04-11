cd ~
conda activate maze-runner
scp -r assignment2_joy student@10.102.0.150:~/
cd assignment2_joy
echo "Done with scp commands. Now running assignment2_joy/main.py..." 
mpirun -hostfile machines.txt -np 4 python3 main.py