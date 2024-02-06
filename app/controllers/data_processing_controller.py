#%%
# app/controllers/data_processing_controller.py

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

# Imports
import pandas as pd
from flask import render_template, request, redirect, url_for
from app import app
from app.services.data_processing_service import drop_selected_columns, process_uploaded_file, col_labelling
from app.services.data_processing_service import perform_imputation, dropping_rows_with_missing_value

# import os
# import tempfile


# Here the data is being declared globally
data=None
modified_data = None


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
        print(data_head)
        if isinstance(data_head, pd.DataFrame):
            return render_template('index.html', data_head=data_head.to_html(), col_name=data_head.columns.values.tolist())  
        else:
            return render_template('index.html', error_message="Invalid file content. Please upload a valid CSV file.")

    return redirect(url_for('index'))

#*****************************************************************DONOT CHANGE THE ABOVE***************************************************************************************** # 


#******************************************************************ADD CODES HERE ONLY***************************************************************************************** # 
# @app.route('/invoke_column_type_method', methods=['POST'])
# def invoke_column_type_method():
#     selected_method = request.form.get('column_type_method')

#     if selected_method == 'manual':
#         # Redirect to the manual column type selection method
#         return redirect(url_for('column_type_selection'))
#     elif selected_method == 'automatic':
#         # Call the automatic column type computation method directly
#         return redirect(url_for('compute_custom_labels'))
#     else:
#         # Handle other cases or show an error
#         return render_template('index.html', error_message="Invalid method selected.")



# Route to handle column type selection
@app.route('/column_type_selection', methods=['POST'])
def column_type_selection():
    print("aa gaye")
    # global data
    try:
        # data_head_local = data.head(3)
        print("Hello")
        col_names = modified_data.columns.tolist()
        print("Hello2")
        # print("data head ke baad", data_head)
        # col_names = data_head.columns.tolist()
        # print("colnames ke baad", col_names)
        # col_names = data_head.columns.tolist()
        if request.method == 'POST':
            selected_column_types = {}
            print("Hello")
            for column in col_names:
                selected_column_types[column] = request.form.get(column)

            print("Selected Column Types:", selected_column_types)

            return render_template('index.html', col_names=col_names)
            # return {'message':'API success'}
        return render_template('index.html', col_names=col_names)
        # return {'message':'API success'}
      
    except Exception as e:
        # print("nhi hua")
        return render_template('index.html', error_message=f"An error occurred: {e}")
        # return {'message':'API error'}


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


@app.route('/dropping_rows_with_missing_values' , methods=['POST'])
def dropping_rows_missing_values():
    global data #here the data is being called for global scope
    dropping_rows_attempted=True
    try:
        df, features_na_values_perc = dropping_rows_with_missing_value(data) #df and features with na are returned
        # print(features_na_values_perc)
        # df = datarows_missing_values[0]
        # features_na_values_perc = datarows_missing_values[1]

        return render_template('index.html', dropping_rows_attempted=dropping_rows_attempted, features_na_values_perc = features_na_values_perc) # Here the  data after dropping the rows is outputted in the webpage

    except Exception as e:
        return render_template('index.html', error_message=f"An error occured while dropping rows with missing values: {e}", dropping_rows_attempted=dropping_rows_attempted)


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
    global data, modified_data

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
# %%
