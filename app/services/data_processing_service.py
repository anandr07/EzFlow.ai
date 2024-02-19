#%%
# app/services/data_processing_service.py - Here goes the actual python code that we do in DS/ML Projects

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

import pandas as pd
from flask import request
import numpy as np

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

def col_labelling(cleaned_data):
    global custom_col_labels
    custom_col_labels = {}

    for col in cleaned_data.columns:
        if cleaned_data[col].dtype == 'object':
            custom_col_labels[col] = 'categorical'
        else:
            unique_values_ratio = len(cleaned_data) / cleaned_data[col].nunique()
            if unique_values_ratio > 11:
                custom_col_labels[col] = 'categorical'
            else:
                custom_col_labels[col] = 'numerical'
    return custom_col_labels

def dropping_rows_with_missing_value(file):
    try:
        df = file
        print("Columns with missing values:", [column for column in df.columns if df[column].isnull().any()])

    # Identify features with more than 60% missing values
        features_with_na = {}
        # print("col:",df.columns)
        for feature_names in df.columns:
            if df[feature_names].isnull().sum() > 0:
                missing_percentage = np.round(df[feature_names].isnull().mean() * 100, 4)
                features_with_na[feature_names] = missing_percentage
        print(features_with_na)
        # Print feature names and their respective percentage of missing values
        #print("sadas",len(features_with_na))
        for feature, missing_percentage in features_with_na.items():
            print(f"{feature}: {missing_percentage}% missing values")

            print(feature)
        # Drop rows with missing values in columns having more than 80% missing values
            df.dropna(subset=feature, inplace=True)
        # returning the DataFrame after dropping rows
        print(df)
        return df,features_with_na
        
    except Exception as e:
        print(f"No file {e}")
        return None


def perform_imputation(file):
    try:
        print(custom_col_labels)
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
    

def drop_selected_columns(df, columns_to_drop):
    print(columns_to_drop)
    try:
        df.drop(columns_to_drop, axis=1, inplace=True)
        return df
    except Exception as e:
        print(f"Error Occured: {e}")
        return None

def correct_category_dtype(df, col_labels):
    try:
        print(1)
        for col in col_labels:
            if col_labels[col] == 'Continuous':
                df[col] = pd.to_numeric(df[col], errors='coerce')
                # median = df[col].median()
                # df[col] = df[col].fillna(median)
            else:
                pass
                # mode = df[col].mode()[0]
                # df[col] = df[col].fillna(mode)
        print(1)
        print('Corrected Data Types: \n', df.dtypes)
        return df
    except Exception as e:
        print(f"Error Occured: {e}")
        return None
