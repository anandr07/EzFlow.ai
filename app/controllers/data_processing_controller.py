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
import os
import tempfile
@app.route('/')
def index():
    return render_template('index.html', data_head=None,data_impute=None,imputation_attempted=False)  # Pass data_head as None initially 


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, file.filename)
        print(f"Saving file to: {temp_file_path}") 
        file.save(temp_file_path)
        session['uploaded_file_path'] = temp_file_path
        data_head = process_uploaded_file(session['uploaded_file_path'] )

        if isinstance(data_head, pd.DataFrame):
            return render_template('index.html', data_head=data_head.to_html())  
        else:
            return render_template('index.html', error_message="Invalid file content. Please upload a valid CSV file.")

    return redirect(url_for('index'))

#*****************************************************************DONOT CHANGE THE ABOVE***************************************************************************************** # 


#******************************************************************ADD CODES HERE ONLY***************************************************************************************** # 
@app.route('/data_impuation', methods=['POST'])
def imputation():
    imputation_attempted = True 

    if 'uploaded_file_path' not in session:
        return render_template('index.html', error_message="No data provided for imputation.", imputation_attempted=imputation_attempted)

    try:
        # Assuming the data is passed as a JSON string in form data
        file_path = session['uploaded_file_path']
        print(f"File path from session: {file_path}")
        data_df = pd.read_csv(file_path)
        print(f"Data read from file: \n{data_df.head()}") 

        # Perform imputation
        imputed_data_df = perform_imputation(data_df)
        print(f"Imputed Data: \n{imputed_data_df.head()}")
        # Render the result
        return render_template('index.html', data_impute=imputed_data_df.to_html(), imputation_attempted=imputation_attempted)

    except Exception as e:
        return render_template('index.html', error_message=f"An error occurred during imputation: {e}", imputation_attempted=imputation_attempted)


# %%
