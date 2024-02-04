#%%
# app/services/data_processing_service.py - Here goes the actual python code that we do in DS/ML Projects

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

import pandas as pd
from flask import request

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

<<<<<<< Updated upstream
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
=======
def col_labelling(data):
    global custom_col_labels
    custom_col_labels = {}

    for col in data.columns:
        if data[col].dtype == 'object':
            custom_col_labels[col] = 'categorical'
        else:
            unique_values_ratio = len(data) / data[col].nunique()
            if unique_values_ratio > 11:
                custom_col_labels[col] = 'categorical'
            else:
                custom_col_labels[col] = 'numerical'
    return custom_col_labels

# def perform_imputation(file):
#     try:
#         df=file
#         for col in df.columns:
#             if df[col].dtype == 'float64' or df[col].dtype == 'int64':
#                 df[col].fillna(df[col].mean(), inplace=True)
#             else:
#                 df[col].fillna('Missing', inplace=True)
#         return df.head()
#     except Exception as e:
#         print(f"No file {e}")
#         return None
    

def drop_selected_columns(file, columns_to_drop):
    print(columns_to_drop)
    try:
        df= file
        df.drop(columns_to_drop, axis=1, inplace=True)
        return df
    except Exception as e:
        print(f"No File: {e}")
        return None
#%%
    
def perform_imputation(file, fill_method='mean'):
    global user_labeled_col, custom_col_labels
    try:
        df = file
        # Determine which label dictionary to use based on whether user_labeled_col is empty
        if not user_labeled_col:  # Check if user_labeled_col is empty ## This Runs when user_labeled_col are empty
            # If user_labeled_col is empty, use custom_col_labels for all columns
            label_source = custom_col_labels
        else:
            # If user_labeled_col is not empty, prefer user labels but fall back to custom labels if necessary
            label_source = {**custom_col_labels, **user_labeled_col}  # Merge, with user_labeled_col taking precedence

        for col in df.columns:
            # Determine column type using the chosen label source
            col_type = label_source.get(col, None)
            
            # Apply imputation based on the determined column type and specified fill_method
            if col_type == 'numerical':
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
    if id_column==None:
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
>>>>>>> Stashed changes
