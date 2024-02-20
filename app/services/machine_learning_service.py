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

def get_variables_by_type(problem_type):
    custom_col_labels = data_processing_service.custom_col_labels
    if problem_type == 'regression':
        return [var for var, var_type in custom_col_labels.items() if var_type == 'numerical']
    elif problem_type == 'classification':
        return [var for var, var_type in custom_col_labels.items() if var_type == 'categorical']
    else:
        return []