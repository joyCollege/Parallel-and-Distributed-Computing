import time
from .train_model import train_model

def sequential_parameter_finder(n_estimators_range, max_features_range, max_depth_range, data):
    """
    Performs a sequential grid search to find the best hyperparameters for a Random Forest model.

    Steps:
    1. Initializes a dictionary to store the best model, RMSE, MAPE, and hyperparameters.
    2. Iterates through all possible combinations of hyperparameters.
    3. Calls `train_model` for each combination to evaluate the model performance.
    4. Updates the best-performing model and parameters based on RMSE.
    5. Prints the best hyperparameters found along with the RMSE and MAPE.
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
        float: Total execution time for the sequential parameter search.
    """
    
    print("*"*20, "Starting Sequential Parameter Finder", "*"*20)
    parallel_time = time.time()
    
    # Initialize variables to store the best model and its RMSE and parameters
    shared_data = dict()
    shared_data['best_rmse'] = float('inf')
    shared_data['best_mape'] = float('inf')
    shared_data['best_model'] = None
    shared_data['best_parameters'] = {}

    # Loop over all possible combinations of parameters
    for n_estimators in n_estimators_range:
        for max_features in max_features_range:
            for max_depth in max_depth_range:
                train_model(n_estimators, max_features, max_depth, shared_data, data)

    print(f"The best parameters {shared_data['best_parameters']} for RMSE = {shared_data['best_rmse']}, MAPE: {shared_data['best_mape']}%")
    
    parallel_time = time.time() - parallel_time 
    print(f"The sequential execution time is {parallel_time}", "\n"*5)
    return parallel_time