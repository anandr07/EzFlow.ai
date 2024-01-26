#%%
# app/services/data_processing_service.py - Here goes the actual python code that we do in DS/ML Projects

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

import pandas as pd
from flask import request


custom_col_labels = {}

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


def col_labelling(data):
    
    global data
    
    global custom_col_labels
    for col in data.columns:
        if data[col].dtype == 'object':
            custom_col_labels[col] = 'categorical'
        
        else:
            unique_values_ratio = len(data) / data[col].nunique()
            
            # max_nunique = data.nunique().max()

            
            if unique_values_ratio > 11:
                custom_col_labels[col] = 'categorical'
            else:
                custom_col_labels[col] = 'numerical'
                

