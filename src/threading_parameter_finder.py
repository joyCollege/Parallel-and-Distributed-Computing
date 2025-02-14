import time
import threading
from .train_model import train_model

def threading_parameter_finder(n_estimators_range, max_features_range, max_depth_range, data):
    """
    Performs a parallel grid search for the best hyperparameters using threading.

    Steps:
    1. Initializes a dictionary to store the best model, RMSE, MAPE, and hyperparameters.
    2. Iterates through all possible combinations of hyperparameters.
    3. Creates a thread for each combination and calls `train_model` in parallel.
    4. Waits for all threads to complete execution.
    5. Updates and prints the best-performing model and parameters based on RMSE.
    6. Measures and prints the execution time.

    Args:
        n_estimators_range (iterable): Range of values for the number of trees in the forest.
        max_features_range (iterable): Range of values for the number of features considered at each split.
        max_depth_range (iterable): Range of values for the maximum tree depth.
        data (dict): Dictionary containing:
            - X_train_filled (pd.DataFrame): Training feature set.
            - y_train (pd.Series): Training target values.
            - X_val_filled (pd.DataFrame): Validation feature set.
            - y_val (pd.Series): Validation target values.

    Returns:
        float: Total execution time for the threaded parameter search.
    """
    
    print("*"*20, "Starting Threading Parameter Finder", "*"*20)
    parallel_time = time.time()
    # Initialize variables to store the best model and its RMSE and parameters
    shared_data = dict()
    shared_data['best_rmse'] = float('inf')
    shared_data['best_mape'] = float('inf')
    shared_data['best_model'] = None
    shared_data['best_parameters'] = {}

    threads = []
    # Loop over all possible combinations of parameters
    for n_estimators in n_estimators_range:
        for max_features in max_features_range:
            for max_depth in max_depth_range:
                thread = threading.Thread(target=train_model, args=(n_estimators, max_features, max_depth, shared_data, data))
                threads.append(thread)
                thread.start()

    for thread in threads:
        thread.join()

    print(f"The best parameters {shared_data['best_parameters']} for RMSE = {shared_data['best_rmse']}, MAPE: {shared_data['best_mape']}%")

    parallel_time = time.time() - parallel_time 
    print(f"The threading execution time is {parallel_time}", "\n"*5)
    return parallel_time