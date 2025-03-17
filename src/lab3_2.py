import time
from src.pt2_data_preprocessing import data_preprocessing
from src.pt2_sequential_parameter_finder import sequential_parameter_finder
from src.pt2_multiprocessing_parameter_finder import multiprocessing_parameter_finder
from src.pt2_queue_parameter_finder import queue_parameter_finder
from src.pt2_threading_parameter_finder import threading_parameter_finder
from src.calc_print_analysis import print_analysis

def lab3_2():
    """
    Part 2: Evaluates and compares different parallelization techniques (sequential, threading, and multiprocessing)
    for hyperparameter tuning of a Random Forest model.

    The function:
    1. Preprocesses the housing price data and splits it into training and validation sets.
    2. Defines the range of hyperparameters for the Random Forest model.
    3. Runs the sequential, threading, and multiprocessing grid search methods to find the best hyperparameters.
    4. Measures the execution times of each method and prints analysis comparing their performance.
    
    Args:
        None
    
    Prints:
        Performance analysis of each parallelization method in terms of execution time and parallelized portion.
    """
    print("\n"*5)
    print("*"*70)
    print("*"*20, 'Part 2: finding best parameters', "*"*20)
    print("*"*70, "\n")

    non_parallized_time = time.time()

    # Preprocess the data and split
    csv_path = './data/housing_prices_data/train.csv'
    data = dict()
    data['X_train_filled'], data['X_val_filled'], data['y_train'], data['y_val'] = data_preprocessing(csv_path)
    
    # Putting the original parameters back 
    n_estimators_range = [10, 25, 50, 100, 200, 300, 400]
    max_features_range = ['sqrt', 'log2', None]  # None means using all features
    max_depth_range = [1, 2, 5, 10, 20, None]  # None means no limit

    # # New the parameter ranges
    # n_estimators_range = [10, 25, 50, 100, 200, 300, 400, 500, 600, 800]
    # max_features_range = ['sqrt', 'log2', None, 0.2, 0.5]
    # max_depth_range = [1, 2, 5, 10, 20, 30, 50, None]

    non_parallized_time =  time.time() - non_parallized_time
    
    # Run sequential, threading, and multiprocessing parameter finder
    sequential_time =  sequential_parameter_finder(n_estimators_range, max_features_range, max_depth_range, data)
    threading_time = threading_parameter_finder(n_estimators_range[::-1], max_features_range, max_depth_range, data)
    multiprocessing_time = multiprocessing_parameter_finder(n_estimators_range[::-1], max_features_range, max_depth_range, data)
    queue_time = queue_parameter_finder(n_estimators_range[::-1], max_features_range, max_depth_range, data)

    print_analysis(num_actions = len(n_estimators_range) * len(max_features_range) * len(max_depth_range) ,
        serial_time = sequential_time,
        parallel_time = threading_time,
        parallelized_portion = threading_time / (non_parallized_time+threading_time) ,
        title = "threading_parameter_finder"
        )
    
    print_analysis(num_actions = len(n_estimators_range) * len(max_features_range) * len(max_depth_range),
        serial_time = sequential_time,
        parallel_time = multiprocessing_time,
        parallelized_portion = multiprocessing_time / (non_parallized_time+multiprocessing_time),
        title = "multiprocessing_parameter_finder"
        )

    print_analysis(num_actions = len(n_estimators_range) * len(max_features_range) * len(max_depth_range),
        serial_time = sequential_time,
        parallel_time = queue_time,
        parallelized_portion = queue_time / (non_parallized_time+queue_time),
        title = "queue_parameter_finder"
        )
    