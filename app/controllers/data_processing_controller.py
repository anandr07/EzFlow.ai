#%%
# app/controllers/data_processing_controller.py

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

# Imports
import pandas as pd
from flask import render_template, request, redirect, url_for,session
from app import app
from app.services.data_processing_service import process_uploaded_file
from app.services.data_processing_service import perform_imputation
# import os
# import tempfile


# Here the data is being declared globally
data=None


@app.route('/')
def index():
    return render_template('index.html', data_head=None,data_impute=None,imputation_attempted=False)  # Pass data_head and data_impute as None initially The imputation_attempted should be False as we dont want to display any thing from the data_imputation button if its not clicked


@app.route('/upload', methods=['POST'])
def upload_file():
    global data
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    # Here the file is being inputted.
    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        # temp_dir = tempfile.gettempdir()
        # temp_file_path = os.path.join(temp_dir, file.filename)
        # print(f"Saving file to: {temp_file_path}") 
        # file.save(temp_file_path)
        # session['uploaded_file_path'] = temp_file_path
        data=pd.read_csv(file) # Here the csv file being transformed into a data frame for further usage
        data_head = process_uploaded_file(data)

        if isinstance(data_head, pd.DataFrame):
            return render_template('index.html', data_head=data_head.to_html())  
        else:
            return render_template('index.html', error_message="Invalid file content. Please upload a valid CSV file.")

    return redirect(url_for('index'))

#*****************************************************************DONOT CHANGE THE ABOVE***************************************************************************************** # 


#******************************************************************ADD CODES HERE ONLY***************************************************************************************** # 
@app.route('/data_impuation', methods=['POST'])
def imputation():
    global data #Here the data is being called from the global scope
    imputation_attempted = True 
    try:
        imputed_data_df = perform_imputation(data)
        print(f"Imputed Data: \n{imputed_data_df.head()}")
        # Render the result
        return render_template('index.html', data_impute=imputed_data_df.to_html(), imputation_attempted=imputation_attempted) # Here the imputed data is outputted in the webpage

    except Exception as e:
        return render_template('index.html', error_message=f"An error occurred during imputation: {e}", imputation_attempted=imputation_attempted)


# %%
