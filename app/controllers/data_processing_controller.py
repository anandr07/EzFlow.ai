#%%
# app/controllers/data_processing_controller.py

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

# Imports
import pandas as pd
from flask import render_template, request, redirect, url_for
from app import app
from app.services.data_processing_service import process_uploaded_file, get_user_labels, user_labeled_col

@app.route('/')
def index():
    return render_template('index.html', data_head=None, data_des= None, column_names=None)  # Pass data_head as None initially 

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    

    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        data_head, data_des, column_names = process_uploaded_file(file)

        if isinstance(data_head, pd.DataFrame) and isinstance(data_des, pd.DataFrame) and column_names:
            return render_template('index.html', data_head=data_head.to_html(),data_des=data_des.to_html(), column_names = column_names, user_labeled_col=user_labeled_col)  
        else:
            return render_template('index.html', error_message="Invalid file content. Please upload a valid CSV file.")

    return redirect(url_for('index'))

#*****************************************************************DONOT CHANGE THE ABOVE***************************************************************************************** # 


#******************************************************************ADD CODES HERE ONLY***************************************************************************************** # 



# %%
@app.route('/get_user_labels', methods=['POST'])
def get_user_labels_route():
    global user_labeled_col
    user_labeled_col = get_user_labels()
    return redirect(url_for('index'))