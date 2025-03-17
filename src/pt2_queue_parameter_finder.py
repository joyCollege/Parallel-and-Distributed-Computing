from time import time
from multiprocessing import Process, Queue, cpu_count, Manager
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from math import sqrt
import numpy as np

def train_model(n_estimators, max_features, max_depth, data, queue):
    """
    Trains a Random Forest Regressor on the provided dataset and evaluates its performance.
    Args:
        n_estimators (int): Number of trees in the forest.
        max_features (int or float or str): Number of features to consider at each split.
        max_depth (int or None): Maximum depth of the trees.
        data (dict): Dictionary containing:
            - X_train_filled (pd.DataFrame): Training feature set.
            - y_train (pd.Series): Training target values.
            - X_val_filled (pd.DataFrame): Validation feature set.
            - y_val (pd.Series): Validation target values.
        queue (multiprocessing.Queue): Queue to store results.
    """
    rf_model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_features=max_features,
        max_depth=max_depth,
        random_state=42
    )
    rf_model.fit(data['X_train_filled'], data['y_train'])

    y_val_pred = rf_model.predict(data['X_val_filled'])
    rmse = sqrt(mean_squared_error(data['y_val'], y_val_pred))
    mape = np.mean(np.abs((np.expm1(data['y_val']) - np.expm1(y_val_pred)) / np.expm1(data['y_val']))) * 100
    print(f"Added to queue: {n_estimators}, {max_features}, {max_depth} -> RMSE: {rmse}, MAPE: {mape}%")

    queue.put((rmse, mape, (n_estimators, max_features, max_depth)))  # Store result

def queue_parameter_finder(n_estimators_range, max_features_range, max_depth_range, data):
    """
    Performs a parallel grid search for the best hyperparameters using multiprocessing with a shared queue.
    Args:
        n_estimators_range (iterable): Range of values for the number of trees in the Random Forest.
        max_features_range (iterable): Range of values for the number of features considered at each split.
        max_depth_range (iterable): Range of values for the maximum depth of the trees.
        data (dict): Dictionary containing:
            - X_train_filled (pd.DataFrame): Training feature set.
            - y_train (pd.Series): Training target values.
            - X_val_filled (pd.DataFrame): Validation feature set.
            - y_val (pd.Series): Validation target values.
    Returns:
        float: Total execution time for the queue-based multiprocessing parameter search.
    """
    print("*"*20, "Starting Queue Multiprocessing Parameter Finder", "*"*20)

    parallel_time = time()
    
    manager = Manager()
    queue = manager.Queue()  # Shared queue for storing best results
    processes = []

    # Generate all parameter combinations
    param_combinations = [(n, f, d, data, queue) 
                          for n in n_estimators_range 
                          for f in max_features_range 
                          for d in max_depth_range]

    num_workers = max(1, cpu_count() - 1)

    # Start worker processes
    for params in param_combinations:
        process = Process(target=train_model, args=params)
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    # Extract best result from the queue
    best_rmse, best_mape, best_params = float('inf'), float('inf'), None
    while not queue.empty():
        rmse, mape, params = queue.get()
        # Update best result if we find a model with a better RMSE
        if rmse < best_rmse:
            best_rmse, best_mape, best_params = rmse, mape, params

    # print(f"The best parameters {best_params} for RMSE = {best_rmse}, MAPE: {best_mape}%")

    parallel_time = time() - parallel_time
    print(f"The queue multiprocessing execution time is {parallel_time}", "\n" * 5)
    return parallel_time
