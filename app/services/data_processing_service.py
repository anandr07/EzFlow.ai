#%%
# app/services/data_processing_service.py - Here goes the actual python code that we do in DS/ML Projects

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

import pandas as pd
from flask import request

user_labeled_col = {} 
custom_col_labels ={}

def process_uploaded_file(file):
    try:
        
        df = file

        x_rows = 5  # Set a default value
        if 'x_rows' in request.form:
            x_rows = int(request.form['x_rows'])

        data_head = df.head(x_rows)
    
        return data_head
    except Exception as e:
        # Handle exceptions, log or print an error message
        print(f"Error processing file: {e}")
        return None


## DONOT CHANGE THIS FILE 

def col_labelling(data):
    for col in data.columns:
        if data[col].dtype == 'object':
            custom_col_labels[col] = 'categorical'
        else:
            unique_values_ratio = len(data) / data[col].nunique()
            if unique_values_ratio > 11:
                custom_col_labels[col] = 'categorical'
            else:
                custom_col_labels[col] = 'numerical'


def perform_imputation(file):
    try:
        df=file
        for col in df.columns:
            if df[col].dtype == 'float64' or df[col].dtype == 'int64':
                df[col].fillna(df[col].mean(), inplace=True)
            else:
                df[col].fillna('Missing', inplace=True)
        return df.head()
    except Exception as e:
        print(f"No file {e}")
        return None
    

def drop_selected_columns(file, columns_to_drop):
    print(columns_to_drop)
    try:
        df= file
        df.drop(columns_to_drop, axis=1, inplace=True)
        return df
    except Exception as e:
        print(f"No File: {e}")
        return None
