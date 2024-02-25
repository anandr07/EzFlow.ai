#%%
# This code should contain logic for training ML Models
# app/services/machine_learning_service.py

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    precision_score, recall_score, confusion_matrix, ConfusionMatrixDisplay
)
from sklearn.preprocessing import StandardScaler
from app.services import data_processing_service  
from app.controllers import data_processing_controller  
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def get_variables_by_type(problem_type):
    col_labels = data_processing_service.col_labels
    print(col_labels)
    if problem_type == 'regression':
        return [var for var, var_type in col_labels.items() if var_type == 'continuous']
    elif problem_type == 'classification':
        return [var for var, var_type in col_labels.items() if var_type == 'categorical']
    else:
        return []
    
def train_linear_regression(selected_variable):
    # Create and fit the linear regression model
    cleaned_data = data_processing_controller .cleaned_data
    y = cleaned_data[selected_variable]
    X = cleaned_data.drop(columns=[selected_variable],axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Calculate evaluation metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)    
    # Return evaluation metrics as a dictionary
    return {'Mean Absolute Error': mae, 'Mean Squared Error': mse, 'Root Mean Squared Error': rmse, 'R^2 Score': r2}

# Define a function to train the SVR model
def train_SVR(selected_variable):
    # Get the cleaned data
    cleaned_data = data_processing_controller.cleaned_data
    # Extract the target variable (y) and features (X)
    y = cleaned_data[selected_variable]
    X = cleaned_data.drop(columns=[selected_variable], axis=1)
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Initialize the SVR model
    model = SVR()
    # Fit the model to the training data
    model.fit(X_train, y_train)
    # Make predictions on the test data
    y_pred = model.predict(X_test)
    # Calculate evaluation metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    # Return the evaluation metrics
    return {'Mean Absolute Error': mae, 'Mean Squared Error': mse, 'Root Mean Squared Error': rmse, 'R^2 Score': r2}

def train_KNN(selected_variable):
    # Get the cleaned data
    cleaned_data = data_processing_controller.cleaned_data
    # Extract the target variable (y) and features (X)
    y = cleaned_data[selected_variable]
    X = cleaned_data.drop(columns=[selected_variable], axis=1)
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Initialize the KNN regression model
    model = KNeighborsRegressor()
    # Fit the model to the training data
    model.fit(X_train, y_train)
    # Make predictions on the test data
    y_pred = model.predict(X_test)
    # Calculate evaluation metrics
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    # Return the evaluation metrics
    return {'Mean Absolute Error': mae, 'Mean Squared Error': mse, 'Root Mean Squared Error': rmse, 'R^2 Score': r2}