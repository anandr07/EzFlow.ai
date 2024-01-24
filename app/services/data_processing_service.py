#%%
# app/services/data_processing_service.py - Here goes the actual python code that we do in DS/ML Projects

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

import pandas as pd
from flask import request

def process_uploaded_file(file):
    try:
        
        df = pd.read_csv(file)

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

def perform_imputation(file):
    try:
        df=file
        for col in df.columns:
            if df[col].dtype == 'float64' or df[col].dtype == 'int64':
                df[col].fillna(df[col].mean(), inplace=True)
            else:
                df[col].fillna('Missing', inplace=True)
        return df
    except Exception as e:
        print(f"No file {e}")
        return None