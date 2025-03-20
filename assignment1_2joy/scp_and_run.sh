cd ~
scp -r assignment1_2joy student@10.102.0.167:~/
cd assignment1_2joy
echo "Done with scp commands. Now running assignment1_2joy/main.py..." 
mpirun -hostfile machines.txt -np 2 python3 main.py