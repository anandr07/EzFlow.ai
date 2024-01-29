#%%
# app/services/data_processing_service.py - Here goes the actual python code that we do in DS/ML Projects

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

import pandas as pd
from flask import request

user_labeled_col = {} 

def process_uploaded_file(file):
    try:
        
        df = pd.read_csv(file)

        x_rows = 5  # Set a default value
        if 'x_rows' in request.form:
            x_rows = int(request.form['x_rows'])

        data_head = df.head(x_rows)
        data_des = df.describe()
        column_names = df.columns.tolist()

        return data_head , data_des , column_names 
    except Exception as e:
        # Handle exceptions, log or print an error message
        print(f"Error processing file: {e}")
        return None



## DONOT CHANGE THIS FILE 
    
#%%
def get_user_labels():
    global user_labeled_col

    if request.method == 'POST':
        for col in user_labeled_col:
            user_labeled_col[col] = request.form.get(col, 'unknown')

    return user_labeled_col