#%%
# app/controllers/data_processing_controller.py

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

# Imports
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from flask import render_template, request, redirect, url_for
from app import app
from app.services.data_processing_service import process_uploaded_file
from app.services.data_processing_service import perform_imputation
# import os
# import tempfile


# Here the data is being declared globally
cleaned_data=None
raw_data=None

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/')
def index():
    return render_template('index.html', data_head=None,data_impute=None,imputation_attempted=False,atm=False)  # Pass data_head and data_impute as None initially The imputation_attempted should be False as we dont want to display any thing from the data_imputation button if its not clicked


@app.route('/upload', methods=['POST'])
def upload_file():
    global raw_data,cleaned_data
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    # Here the file is being inputted.
    file = request.files['file']
    

    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        raw_data=pd.read_csv(file) # Here the csv file being transformed into a data frame for further usage
        data_head = process_uploaded_file(raw_data)
        cleaned_data = raw_data.copy()
        print(data_head)
        if isinstance(data_head, pd.DataFrame):
            return render_template('index.html', data_head=data_head.to_html(), col_name=data_head.columns.values.tolist())  
        else:
            return render_template('index.html', error_message="Invalid file content. Please upload a valid CSV file.")

    return redirect(url_for('index'))

#*****************************************************************DONOT CHANGE THE ABOVE***************************************************************************************** # 


#******************************************************************ADD CODES HERE ONLY***************************************************************************************** # 
@app.route('/data_impuation', methods=['POST'])
def imputation():
    global cleaned_data  # Here the data is being called from the global scope
    imputation_attempted = True

    # Extract the imputation method from the form data
    impute_method = request.form.get('impute_method', 'mean')  # Default to 'mean' if not specified
    
    try:
        imputed_data_df = perform_imputation(cleaned_data, impute_method)
        print(f"Imputed Data: \n{imputed_data_df.head()}")

        # Render the result
        return render_template('index.html', imputed_data_df=imputed_data_df.to_html(), imputation_attempted=imputation_attempted)

    except Exception as e:
        return render_template('index.html', error_message=f"An error occurred during imputation: {e}", imputation_attempted=imputation_attempted)


# %%

@app.route('/remove_id_column', methods=['POST'])
def remove_id_column():
    global data
    data = process_dataframe_remove_id(data, drop_id=True)
    return render_template('index.html', data_id=data.to_html())