cd ~
scp -r assignment1.2_joy student@10.102.0.217:~/
scp -r assignment1.2_joy student@10.102.0.167:~/
scp -r assignment1.2_joy student@10.102.0.150:~/
cd assignment1.2_joy
echo "Done with scp commands. Now running assignment1.2_joy/main.py..." 
mpirun -hostfile machines.txt -np 24 python3 main.py
