import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# 1. Choose Models
models = {
    'RandomForest': RandomForestClassifier(n_estimators=100, n_jobs=1, random_state=42),
    'SVM': SVC(kernel='rbf', probability=True, random_state=42),
    'LogisticRegression': LogisticRegression(max_iter=5000, solver='saga', random_state=42)
}

# 2. Hyperparameter grid for Random Forest
rf_param_grid = {
    'n_estimators': [50, 100, 200, 300, 500],  # More estimators
    'max_depth': [10, 20, 30, 40, None],  # Deeper trees
    'min_samples_split': [2, 5, 10, 20],  # Split points at more intervals
    'min_samples_leaf': [1, 2, 4, 8],  # Leaf size adjustments
    'max_features': ['sqrt', 'log2', None, 0.1, 0.5],  # Feature selections
    'bootstrap': [True, False],  # Whether to bootstrap samples
    'warm_start': [True, False]  # Allows for more flexible fitting
}

# 3. Define Logistic Regression pipeline with scaling
logistic_pipeline = Pipeline([
    ('scaler', StandardScaler()),  # Feature scaling
    ('model', LogisticRegression(max_iter=5000, solver='saga', random_state=42))
])

# 4. Hyperparameter grid for Logistic Regression
logistic_param_grid = {
    'model__C': [0.001, 0.01, 0.1, 1, 10, 100],  # Regularization strength
    'model__penalty': ['l1', 'l2', 'elasticnet'],  # Penalty types (added elasticnet)
    'model__solver': ['lbfgs', 'saga', 'newton-cg'],  # Solvers to use
    'model__max_iter': [1000, 2000, 5000],  # Increase max_iter for convergence
    'model__tol': [1e-4, 1e-5, 1e-6],  # Tolerance for stopping criteria
    'model__fit_intercept': [True, False]  # Fit an intercept or not
}

# 5. Train and Evaluate Function
def train_and_evaluate(name, model, X_train, y_train, X_test, y_test):
    start = time.time()
    if name == "RandomForest":
        grid_search = GridSearchCV(model, rf_param_grid, cv=3, n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train)
        model = grid_search.best_estimator_
    elif name == "LogisticRegression":
        grid_search = GridSearchCV(logistic_pipeline, logistic_param_grid, cv=3, n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train)
        model = grid_search.best_estimator_
    else:
        model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    report = classification_report(y_test, y_pred)

    training_time = time.time() - start
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

# 6. Model Development Function
def model_development(shuffled_dataframe):
    # 1. Split the Data
    X = shuffled_dataframe.drop('Tumor', axis=1)
    y = shuffled_dataframe['Tumor']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # 2. Train and Evaluate Models in Parallel
    results = []
    for name, model in models.items():
        result = train_and_evaluate(name, model, X_train, y_train, X_test, y_test)
        results.append(result)

    # 3. Print the Results
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

