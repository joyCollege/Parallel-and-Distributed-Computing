
from src.lab3_1 import lab3_1
from src.lab3_2 import lab3_2

if __name__ == "__main__":
    '''
    Runs the two parts of lab 3
    
    Part 1:Runs performance tests for different parallelization strategies (sequential, threading, and multiprocessing) 
    over a specified number of iterations (1 million).

    Part 2: Evaluates and compares different parallelization techniques (sequential, threading, and multiprocessing)
    for hyperparameter tuning of a Random Forest model.
    '''
    lab3_1()
    lab3_2()

