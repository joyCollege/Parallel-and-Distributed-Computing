from sklearn.metrics import mean_absolute_percentage_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt

def train_model(n_estimators, max_features, max_depth, shared_data, data):
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
    # Create and train the Random Forest model
    rf_model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_features=max_features,
        max_depth=max_depth,
        random_state=42
    )
    rf_model.fit(data['X_train_filled'], data['y_train'])
    
    # Make predictions and compute RMSE
    y_val_pred = rf_model.predict(data['X_val_filled'])
    rmse = sqrt(mean_squared_error(data['y_val'], y_val_pred))
    # Compute MAPE
    mape = mean_absolute_percentage_error(data['y_val'], y_val_pred) * 100
    print(f"The parameters: {n_estimators}, {max_features}, {max_depth}. RMSE: {rmse}, MAPE: {mape}%")
    # If the model is better than the current best, update the best model and its parameters
    if rmse < shared_data['best_rmse']:
        shared_data['best_rmse'] = rmse
        shared_data['best_mape'] = mape
        shared_data['best_model'] = rf_model
        shared_data['best_parameters'] = {
            'n_estimators': n_estimators,
            'max_features': max_features,
            'max_depth': max_depth
        }

    