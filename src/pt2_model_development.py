import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score,
    recall_score, f1_score, classification_report
)
from multiprocessing import Pool

# 2. Choose Three Models
models = {
    'RandomForest': RandomForestClassifier(n_estimators=100, n_jobs=1, random_state=42),
    'SVM': SVC(kernel='rbf', probability=True, random_state=42),
    'LogisticRegression': LogisticRegression(max_iter=2000, n_jobs=1, random_state=42)
}

# 3. Define a helper function to train and evaluate a single model
def train_and_evaluate(name, model, X_train, y_train, X_test, y_test):
    start = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start

    # Validate the model on the test set
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    report = classification_report(y_test, y_pred)

    return {
        'Model': name,
        'Training Time (s)': training_time,
        'Confusion Matrix': cm,
        'Accuracy': acc,
        'Precision': prec,
        'Recall': rec,
        'F1 Score': f1,
        'Classification Report': report
    }

def model_development(shuffled_dataframe):
    # 1. Split the Data
    # Assuming 'shuffled_dataframe' is already defined and contains a column 'Tumor'
    X = shuffled_dataframe.drop('Tumor', axis=1)
    y = shuffled_dataframe['Tumor']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    # 4. Parallelize Training Using Multiprocessing Pool with starmap
    # Create a list of arguments for each model
    tasks = [(name, model, X_train, y_train, X_test, y_test) for name, model in models.items()]
    
    # Using Pool with a process count equal to the number of models (or set a specific number)
    with Pool(processes=len(models)) as pool:
        results = pool.starmap(train_and_evaluate, tasks)
    
    # 5. Validate the Models and Print the Results
    for result in results:
        print("Model:", result['Model'])
        print("Training Time (s):", result['Training Time (s)'])
        print("Confusion Matrix:\n", result['Confusion Matrix'])
        print("Accuracy:", result['Accuracy'])
        print("Precision:", result['Precision'])
        print("Recall:", result['Recall'])
        print("F1 Score:", result['F1 Score'])
        print("Classification Report:\n", result['Classification Report'])
        print("-----------------------------------------------------")
