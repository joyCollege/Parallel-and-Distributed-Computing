# Lab 1
## Parallel-and-Distributed-Computing
## Joy Anne P. Dela Cruz 60301959

## Overview
This project implements a machine learning pipeline using the Iris dataset. The pipeline consists of loading data, splitting it into training and testing sets, training a model, and evaluating its performance.

## Project Structure
- `load_data()`: Loads the Iris dataset.
- `split_data(data, test_size=0.2, random_state=42)`: Splits data into training and testing sets.
- `train_model(X_train, y_train)`: Trains a RandomForestClassifier model.
- `evaluate_model(model, X_test, y_test)`: Evaluates the model and generates a classification report.

## Installation
Ensure you have Python installed along with the required libraries:
```bash
pip install -1 requirements.txt
```

## Usage
Run the script to train and evaluate the model:
```bash
python3 main.py
```

## Output
The script prints a classification report showing model performance metrics.

## License
This project is open-source and available for use under the MIT License.