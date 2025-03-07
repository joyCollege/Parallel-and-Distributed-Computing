import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score,
    recall_score, f1_score, classification_report
)
from multiprocessing import Pool
from imblearn.over_sampling import SMOTE

# 1. Define models
models = {
    'RandomForest': RandomForestClassifier(n_jobs=-1, random_state=42),
    'SVM': SVC(kernel='rbf', probability=True, random_state=42),
    'LogisticRegression': LogisticRegression(max_iter=2000, n_jobs=-1, random_state=42)
}

# 2. Expanded hyperparameter grid for RandomForest
rf_param_grid = {
    'n_estimators': [50, 100, 200, 300, 500],  # Number of trees
    'max_depth': [10, 20, 30, 50, None],  # Tree depth
    'min_samples_split': [2, 5, 10, 15],  # Min samples required to split a node
    'min_samples_leaf': [1, 2, 4, 8],  # Min samples required at a leaf node
    'max_features': ['sqrt', 'log2', None],  # Features considered for best split
    'bootstrap': [True, False]  # Bootstrapping for better generalization
}

# 3. Function to train and evaluate models
def train_and_evaluate(name, model, X_train, y_train, X_test, y_test):
    start = time.time()

    if name == "RandomForest":
        grid_search = GridSearchCV(model, rf_param_grid, cv=3, n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train)
        model = grid_search.best_estimator_  # Use best model from GridSearchCV
    else:
        model.fit(X_train, y_train)

    training_time = time.time() - start

    # Validate model on test set
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

# 4. Main function
def model_development(shuffled_dataframe):
    # Split data
    X = shuffled_dataframe.drop('Tumor', axis=1)
    y = shuffled_dataframe['Tumor']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Apply SMOTE to balance classes
    smote = SMOTE(random_state=42)
    X_train, y_train = smote.fit_resample(X_train, y_train)

    # Prepare tasks for multiprocessing
    tasks = [(name, model, X_train, y_train, X_test, y_test) for name, model in models.items()]
    
    # Train models in parallel
    with Pool(processes=len(models)) as pool:
        results = pool.starmap(train_and_evaluate, tasks)
    
    # Display results
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
