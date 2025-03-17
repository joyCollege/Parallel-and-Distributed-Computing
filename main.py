import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_data
from src.preprocessing import split_data
from src.model import train_model
from src.evaluation import evaluate_model

if __name__ == "__main__":
    """
    Main script for training and evaluating a machine learning model.

    This script loads data, preprocesses it by splitting into training and test sets,
    trains a model using the training data, and evaluates the model's performance.

    Modules:
        - load_data: Loads the dataset.
        - split_data: Splits the dataset into training and testing sets.
        - train_model: Trains a machine learning model.
        - evaluate_model: Evaluates the trained model and generates a performance report.

    Returns:
        - Prints the evaluation report of the trained model.
    """
    data = load_data()
    X_train, X_test, y_train, y_test = split_data(data)
    model = train_model(X_train, y_train)
    report = evaluate_model(model, X_test, y_test)
    print(report)