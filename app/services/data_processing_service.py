#%%
# app/services/data_processing_service.py - Here goes the actual python code that we do in DS/ML Projects

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

import pandas as pd
from flask import request
import numpy as np

col_labels ={}

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
    global col_labels
    col_labels = {}

    for col in cleaned_data.columns:
        if cleaned_data[col].dtype == 'object':
            col_labels[col] = 'categorical'
        else:
            unique_values_ratio = len(cleaned_data) / cleaned_data[col].nunique()
            if unique_values_ratio > 11:
                col_labels[col] = 'categorical'
            else:
                col_labels[col] = 'continuous'
    return col_labels

def manual_col_labelling(col_names, form):
    global col_labels
    for column in col_names:
        col_labels[column] = form.get(column)
    return col_labels

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


def perform_imputation(file, fill_method='mean'):
    global col_labels
    try:
        df = file

        label_source = col_labels
        for col in df.columns:
            # Determine column type using the chosen label source
            col_type = label_source.get(col, None)
            
            # Apply imputation based on the determined column type and specified fill_method
            if col_type == 'continuous':
                # If column type is object, try converting to float
                if df[col].dtype == 'object':
                    try:
                        df[col] = df[col].astype(float)
                    except ValueError:
                        print(f"Warning: Could not convert column '{col}' to float, skipping imputation.")
                        continue  # Skip this column if conversion fails
                
                # Now apply the chosen fill method
                if fill_method == 'mean':
                    df[col].fillna(df[col].mean(), inplace=True)
                elif fill_method == 'median':
                    df[col].fillna(df[col].median(), inplace=True)
                elif fill_method == 'mode':
                    df[col].fillna(df[col].mode()[0], inplace=True)
                elif fill_method=='foward_fill':
                    df[col].fillna(method='ffill', inplace=True)
                elif fill_method == 'backward_fill':
                    df[col].fillna(method='bfill', inplace=True)
                else:
                    print(f"Invalid fill method for numerical column '{col}', skipping imputation.")
            elif col_type == 'categorical':
                if fill_method=='foward_fill':
                    df[col].fillna(method='ffill', inplace=True)
                elif fill_method == 'backward_fill':
                    df[col].fillna(method='bfill', inplace=True)
                else:
                # For categorical columns, replace missing values with the mode
                    df[col].fillna(df[col].mode()[0], inplace=True)
            else:
                # If column type is not determined, handle according to your policy
                print(f"Warning: Column '{col}' type not determined, skipping imputation.")

        return df.head()
    except Exception as e:
        print(f"Error during imputation: {e}")
        return None
 # Function to find ID column
def find_id_column(df):
    for col in df.columns:
        if df[col].is_unique and 'id' in col.lower():
            return pd.DataFrame(df[col]).head()
    return None

# Function to process DataFrame and optionally remove ID column
def process_dataframe_remove_id(df, drop_id=False):
    id_column = find_id_column(df)
    if id_column is None:
        print("No Id columns found")
        return df.head()
    id_column1=id_column.columns[0]
    if id_column1 and drop_id:
        df = df.drop(columns=id_column1)
        print(f"Dropped ID column: {id_column1}")
    elif id_column1:
        print(f"ID column identified but not dropped: {id_column1}")
    else:
        print("No ID column found.")
    return df.head()
   

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
            if col_labels[col] == 'continuous':
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
