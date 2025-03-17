import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np

def data_preprocessing(file_path):
    """
    Preprocesses the housing prices dataset by performing the following steps:
    
    1. Loads the dataset from a CSV file.
    2. Removes specified columns that are not useful for prediction.
    3. Splits the data into input features (X) and the target variable (y).
    4. Identifies categorical features and applies Label Encoding to convert them into numerical format.
    5. Splits the dataset into training and validation sets (70% training, 30% validation).
    6. Handles missing values by filling them with the median of the respective columns.
    
    Returns:
        tuple: (X_train_filled, X_val_filled, y_train, y_val)
        - X_train_filled (pd.DataFrame): Processed training features.
        - X_val_filled (pd.DataFrame): Processed validation features.
        - y_train (pd.Series): Training target values.
        - y_val (pd.Series): Validation target values.
    """
    # Load the train_dataset
    train_data = pd.read_csv(file_path, index_col="Id")

    # Columns to be deleted
    columns_to_delete = ['MoSold', 'YrSold', 'SaleType', 'SaleCondition', 'Alley', 'FireplaceQu', 'PoolQC', 'Fence', 'MiscFeature']

    # Delete the specified columns
    train_data_cleaned = train_data.drop(columns=columns_to_delete, axis=1)

    # Define the input features (X) and the output (y)
    X = train_data_cleaned.drop('SalePrice', axis=1)
    y = train_data_cleaned['SalePrice']

    # Feature engineering: Apply log transformation to target variable
    y = np.log1p(y)

    # Identify the categorical columns in X
    categorical_columns = X.select_dtypes(include=['object']).columns

    # Initialize a LabelEncoder for each categorical column
    label_encoders = {column: LabelEncoder() for column in categorical_columns}

    # Apply Label Encoding to each categorical column
    for column in categorical_columns:
        X[column] = label_encoders[column].fit_transform(X[column])

    # Outlier detection (using IQR)
    # Q1 = X.quantile(0.25)
    # Q3 = X.quantile(0.75)
    # IQR = Q3 - Q1
    # X = X[~((X < (Q1 - 1.5 * IQR)) | (X > (Q3 + 1.5 * IQR))).any(axis=1)]
    # y = y[X.index]

    # Outlier removal for target variable (y)
    Q1_y = y.quantile(0.25)
    Q3_y = y.quantile(0.75)
    IQR_y = Q3_y - Q1_y
    y = y[(y >= (Q1_y - 1.5 * IQR_y)) & (y <= (Q3_y + 1.5 * IQR_y))]
    X = X.loc[y.index]

    # Split the data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.30, random_state=42)

    # Fill NaN values in X_train and X_val with the median of the respective columns
    X_train_filled = X_train.fillna(X_train.median())
    X_val_filled = X_val.fillna(X_val.median())
    
    return (X_train_filled, X_val_filled, y_train, y_val)
