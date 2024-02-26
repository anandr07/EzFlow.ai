#%%
# app/services/data_processing_service.py - Here goes the actual python code that we do in DS/ML Projects

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

import pandas as pd
from flask import request
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg') # DONOT REMOVE THIS
import io
import base64

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

def plot_na_percentage(df, features_with_na):
    # Extract feature names and their respective missing percentages from the dictionary
    features = list(features_with_na.keys())
    missing_percentages = list(features_with_na.values())
    
    # Calculate the number of rows containing NA values for each feature
    rows_with_na = [df[feature].isnull().sum() for feature in features]
    
    # Plotting
    fig, ax1 = plt.subplots()
    
    # Bar plot for missing percentages
    ax1.bar(features, missing_percentages, color='b', alpha=0.5, label='Percentage of NA values')
    ax1.set_xlabel('Features')
    ax1.set_ylabel('Percentage of NA values', color='b')
    ax1.tick_params('y', colors='b')
    ax1.set_xticklabels(features, rotation=45, ha='right')  # Rotate x-axis labels for better readability
    
    # Twin the x-axis to create another y-axis for the number of rows with NA values
    ax2 = ax1.twinx()
    
    # Line plot for the number of rows with NA values
    ax2.plot(features, rows_with_na, color='r', marker='o', label='Number of rows with NA values')
    ax2.set_ylabel('Number of rows with NA values', color='r')
    ax2.tick_params('y', colors='r')
    
    # Add legend
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    # Title
    plt.title('Percentage of NA Values and Number of Rows with NA Values for Each Feature')
    
    # Show plot
    plt.tight_layout()
    # Convert plot to PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convert PNG image to base64 string
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64
    

def display_rows_with_na_values(df):
    try:
        features_with_na = {}

        # Identify features with missing values and their percentages
        for feature in df.columns:
            missing_count = df[feature].isnull().sum()
            if missing_count > 0:
                missing_percentage = np.round((missing_count / len(df)) * 100, 4)
                features_with_na[feature] = missing_percentage
                print(f"{feature}: {missing_percentage}% missing values")

        rows_before = df.shape[0]
        # Convert the summary of missing values to a DataFrame for display
        series = pd.Series(features_with_na)
        missing_values_summary = pd.DataFrame(series, columns=['Percentage of missing values'])
        # figure = plot_na_percentage(df)

        return missing_values_summary.T,rows_before

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
    
    
def dropping_rows_with_na_values(df,drop_threshold):
    try:
         features_with_na = {}

#         # Identify features with missing values and their percentages
         for feature in df.columns:
             missing_count = df[feature].isnull().sum()
             if missing_count > 0:
                 missing_percentage = np.round((missing_count / len(df)) * 100, 4)
                 features_with_na[feature] = missing_percentage
                 print(f"{feature}: {missing_percentage}% missing values")

         print(f"Features to be considered for row dropping (threshold: {drop_threshold}%):")
         # Determine features for which to drop rows based on the threshold
         features_to_drop = [feature for feature, missing_percentage in features_with_na.items() if missing_percentage <= drop_threshold]
         print(features_to_drop)

        
         if features_to_drop:
             rows_before = df.shape[0]
             df.dropna(subset=features_to_drop, inplace=True)
             rows_after = df.shape[0]
             print(f"Dropped {rows_before - rows_after} rows.")
             
         return df,features_to_drop, rows_after
        
    except Exception as e:
         print(f"An error occurred: {e}")
         return None, None


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
