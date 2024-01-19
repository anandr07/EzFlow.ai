#%%
# app/services/data_processing_service.py

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

import pandas as pd
from flask import request

def process_uploaded_file(file):
    try:
        # Read CSV file into a DataFrame
        df = pd.read_csv(file)

        # Get an option from the user if they want to display x number of rows
        x_rows = 10  # Set a default value
        if 'x_rows' in request.form:
            x_rows = int(request.form['x_rows'])

        # Display head of the dataset
        data_head = df.head(x_rows)

        return data_head  # Return the DataFrame head
    except Exception as e:
        # Handle exceptions, log or print an error message
        print(f"Error processing file: {e}")
        return None


## DONOT CHANGE THIS FILE 