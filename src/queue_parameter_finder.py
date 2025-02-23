from time import time
from multiprocessing import Process, Queue, cpu_count
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from math import sqrt
import numpy as np

def train_model(n_estimators, max_features, max_depth, data, queue):
    """
    Trains a Random Forest Regressor on the provided dataset and evaluates its performance.

    Steps:
    1. Initializes and trains a Random Forest model with given hyperparameters.
    2. Makes predictions on the validation set.
    3. Computes the Root Mean Squared Error (RMSE) and Mean Absolute Percentage Error (MAPE).
    4. Prints the model's hyperparameters and evaluation metrics.
    5. Updates the shared_data dictionary if the current model performs better than the previous best.

    Args:
        n_estimators (int): Number of trees in the forest.
        max_features (int or float or str): Number of features to consider at each split.
        max_depth (int or None): Maximum depth of the trees.
        shared_data (dict): Dictionary storing the best model and its performance metrics.
        data (dict): Dictionary containing:
            - X_train_filled (pd.DataFrame): Training feature set.
            - y_train (pd.Series): Training target values.
            - X_val_filled (pd.DataFrame): Validation feature set.
            - y_val (pd.Series): Validation target values.

    Updates shared_data with:
        - 'best_rmse': Lowest RMSE observed.
        - 'best_mape': Corresponding MAPE for the best RMSE.
        - 'best_model': Best-performing Random Forest model.
        - 'best_parameters': Dictionary of hyperparameters for the best model.
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
    print(f"The parameters: {n_estimators}, {max_features}, {max_depth}. RMSE: {rmse}, MAPE: {mape}%")

    queue.put((rmse, mape, (n_estimators, max_features, max_depth)))  # Store result

def queue_parameter_finder(n_estimators_range, max_features_range, max_depth_range, data):
    """
    Performs a parallel grid search for the best hyperparameters using multiprocessing with a shared queue.

    The function:
    1. Initializes a multiprocessing queue to store the best model results.
    2. Iterates through all hyperparameter combinations and starts a separate process for each.
    3. Each process trains a Random Forest model and pushes its RMSE and MAPE results to the queue.
    4. Waits for all processes to complete.
    5. Extracts and prints the best-performing model parameters based on RMSE.
    6. Measures and prints execution time.

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
    
    Prints:
        The best hyperparameters and their corresponding RMSE and MAPE scores.
    """
    print("*"*20, "Starting Queue Multiprocessing Parameter Finder", "*"*20)

    parallel_time = time()
    
    queue = Queue()  # Shared queue for storing best results
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
        if rmse < best_rmse:
            best_rmse, best_mape, best_params = rmse, mape, params

    print(f"The best parameters {best_params} for RMSE = {best_rmse}, MAPE: {best_mape}%")

    parallel_time = time() - parallel_time
    print(f"The queue multiprocessing execution time is {parallel_time}", "\n" * 5)
    return parallel_time

