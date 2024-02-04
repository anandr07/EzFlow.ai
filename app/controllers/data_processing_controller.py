#%%
# app/controllers/data_processing_controller.py

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

# Imports
import pandas as pd
from flask import render_template, request, redirect, url_for,jsonify
from app import app
from app.services.data_processing_service import drop_selected_columns, process_uploaded_file, col_labelling
from app.services.data_processing_service import perform_imputation,find_id_column,process_dataframe_remove_id
# import os
# import tempfile


# Here the data is being declared globally
data=None


@app.route('/')
def index():
    return render_template('index.html', data_head=None,data_impute=None,imputation_attempted=False,data_id=None,id_col=None,atm=False)  # Pass data_head and data_impute as None initially The imputation_attempted should be False as we dont want to display any thing from the data_imputation button if its not clicked


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
            return render_template('index.html', data_head=data_head.to_html(), col_name=data_head.columns.values.tolist())  
        else:
            return render_template('index.html', error_message="Invalid file content. Please upload a valid CSV file.")

    return redirect(url_for('index'))

#*****************************************************************DONOT CHANGE THE ABOVE***************************************************************************************** # 


#******************************************************************ADD CODES HERE ONLY***************************************************************************************** # 
@app.route('/compute_custom_labels', methods=['POST'])
def compute_custom_labels():
    global data
    global custom_col_labels
    Custom_labelling = True

    try:
        custom_col_labels = col_labelling(data)
        return render_template('index.html', custom_labels=custom_col_labels, Custom_labelling=Custom_labelling)

    except Exception as e:
        return render_template('index.html', error_message=f"An error occurred during custom label computation: {e}", Custom_labelling=Custom_labelling)


@app.route('/data_imputation', methods=['POST'])
def imputation():
    global data  # Here the data is being called from the global scope
    imputation_attempted = True

    # Extract the imputation method from the form data
    impute_method = request.form.get('impute_method', 'mean')  # Default to 'mean' if not specified

    try:
        imputed_data_df = perform_imputation(data, impute_method)
        print(f"Imputed Data: \n{imputed_data_df.head()}")

        # Render the result
        return render_template('index.html', data_impute=imputed_data_df.to_html(), imputation_attempted=imputation_attempted)

    except Exception as e:
        return render_template('index.html', error_message=f"An error occurred during imputation: {e}", imputation_attempted=imputation_attempted)
    

@app.route('/drop_columns', methods=['POST'])
def drop_columns():
    global data

    if 'drop_columns' in request.form:
        columns_to_drop = request.form.getlist('columns_to_drop')  # Get the list of columns to drop
        print(f"Columns to drop: {columns_to_drop}")

        if not columns_to_drop:
            return render_template('index.html', error_message="No columns selected for dropping.")

        # Passing selected columns to the confirmation page
        return render_template('confirm_drop.html', columns_to_drop=columns_to_drop)

    return redirect(url_for('index'))

@app.route('/dropped_columns', methods=['POST'])
def confirm_drop():
    global data

    if 'confirm_drop' in request.form:
        confirm = request.form['confirm_drop']
        columns_to_drop = request.form.getlist('columns_to_drop')  # Get the list of columns to drop

        if confirm == 'Yes':
            modified_data = drop_selected_columns(data, columns_to_drop)
            print(modified_data)
            data_head = process_uploaded_file(modified_data)

            if data_head is not None:
                return render_template('index.html', data_head=data_head.to_html(), col_name=data_head.columns.values.tolist())
            else:
                return render_template('index.html', error_message="An error occurred during column dropping.")
        else:
            return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/identify_id_column', methods=['POST'])
def identify_id_column():
    atm=True
    global data
    id_column = find_id_column(data)
    if id_column==None:
        return render_template('index.html', error_message='No Id Column',id_col=None,atm=True)
    else:
        return render_template('index.html', error_message="Id column is there",id_col=id_column.to_html(),atm=True)

@app.route('/remove_id_column', methods=['POST'])
def remove_id_column():
    global data
    data = process_dataframe_remove_id(data, drop_id=True)
    return render_template('index.html', data_id=data.to_html())