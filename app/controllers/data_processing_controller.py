#%%
# app/controllers/data_processing_controller.py

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

# Imports
import pandas as pd
from flask import render_template, request, redirect, url_for
from app import app
from app.services.data_processing_service import process_uploaded_file

@app.route('/')
def index():
    return render_template('index.html', data_head=None)  # Pass data_head as None initially

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        data_head = process_uploaded_file(file)

        if isinstance(data_head, pd.DataFrame):
            return render_template('index.html', data_head=data_head.head().to_html())
        else:
            return render_template('index.html', error_message="Invalid file content. Please upload a valid CSV file.")

    return redirect(url_for('index'))

#*****************************************************************DONOT CHANGE THE ABOVE***************************************************************************************** # 


#******************************************************************ADD CODES HERE ONLY***************************************************************************************** # 


