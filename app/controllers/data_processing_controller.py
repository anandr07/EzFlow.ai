#%%
# app/controllers/data_processing_controller.py

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

# Imports
import pandas as pd
from flask import render_template, request, redirect, url_for
from app import app
from app.services.data_processing_service import drop_selected_columns, process_uploaded_file, col_labelling,correct_category_dtype
from app.services.data_processing_service import perform_imputation, dropping_rows_with_missing_value, manual_col_labelling

# Here the data is being declared globally
cleaned_data=None
raw_data=None

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/')
def index():
    return render_template('index.html', data_head=None,data_impute=None,imputation_attempted=False)  # Pass data_head and data_impute as None initially The imputation_attempted should be False as we dont want to display any thing from the data_imputation button if its not clicked


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

# Route to handle column type selection
@app.route('/column_type_selection', methods=['POST'])
def column_type_selection():
    global col_labels,cleaned_data
    data_head = process_uploaded_file(cleaned_data)
    try:
        col_names = cleaned_data.columns.tolist()
        if request.method == 'POST' :
            col_labels = manual_col_labelling(col_names, request.form)            
            print("Selected Column Types:", col_labels)
            if request.form.to_dict():
                print(col_labels)
                cleaned_data = correct_category_dtype(cleaned_data, col_labels)
                data_head = process_uploaded_file(cleaned_data)
                return render_template('index.html',data_head=data_head.to_html(), col_names=col_names,custom_labels=col_labels)
            return render_template('index.html',data_head=data_head.to_html(), col_names=col_names,custom_labels=col_labels)
        return render_template('index.html',data_head=data_head.to_html(), col_names=col_names,custom_labels=col_labels)
      
    except Exception as e:
        return render_template('index.html', error_message=f"An error occurred: {e}")

@app.route('/compute_custom_labels', methods=['POST'])
def compute_custom_labels():
    global cleaned_data
    global col_labels
    Custom_labelling = True

    try:
        col_labels = col_labelling(cleaned_data)
        print(f"Custom Column Labels: {col_labels}")
        cleaned_data = correct_category_dtype(cleaned_data, col_labels)
        data_head = process_uploaded_file(cleaned_data)
        return render_template('index.html',data_head=data_head.to_html(), custom_labels=col_labels, Custom_labelling=Custom_labelling)

    except Exception as e:
        return render_template('index.html', error_message=f"An error occurred during custom label computation: {e}", Custom_labelling=Custom_labelling)


@app.route('/dropping_rows_with_missing_values' , methods=['POST'])
def dropping_rows_missing_values():
    global cleaned_data #here the data is being called for global scope
    dropping_rows_attempted=True
    try:
        cleaned_data, features_na_values_perc = dropping_rows_with_missing_value(cleaned_data) #df and features with na are returned
        data_head = process_uploaded_file(cleaned_data)
        print(data_head)
        print(dropping_rows_attempted)
        print(features_na_values_perc)
        return render_template('index.html',data_head = data_head.to_html(), dropping_rows_attempted=dropping_rows_attempted, features_na_values_perc = features_na_values_perc) # Here the  data after dropping the rows is outputted in the webpage
    except Exception as e:
        return render_template('index.html', error_message=f"An error occured while dropping rows with missing values: {e}", dropping_rows_attempted=dropping_rows_attempted)


# @app.route('/data_impuation', methods=['POST'])
# def imputation():
#     global cleaned_data #Here the data is being called from the global scope
#     imputation_attempted = True 

#     try:
#         imputed_data_df = perform_imputation(cleaned_data)
#         print(f"Imputed Data: \n{imputed_data_df.head()}")

#         # Render the result
#         return render_template('index.html', data_head=imputed_data_df.to_html(), imputation_attempted=imputation_attempted) # Here the imputed data is outputted in the webpage

#     except Exception as e:
#         return render_template('index.html', error_message=f"An error occurred during imputation: {e}", imputation_attempted=imputation_attempted)
    
    
@app.route('/data_impuation', methods=['POST'])
def imputation():
    global cleaned_data #Here the data is being called from the global scope
    imputation_attempted = True 

    try:
        strategy = request.form.get('strategy')

        imputed_data_df = perform_imputation(cleaned_data, strategy=strategy)
        print(f"Imputed Data: \n{imputed_data_df.head()}")

        # Render the result
        return render_template('index.html', data_head=imputed_data_df.to_html(), imputation_attempted=imputation_attempted) # Here the imputed data is outputted in the webpage

    except Exception as e:
        return render_template('index.html', error_message=f"An error occurred during imputation: {e}", imputation_attempted=imputation_attempted)

@app.route('/drop_columns', methods=['POST'])
def drop_columns():
    global cleaned_data

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
    global cleaned_data

    if 'confirm_drop' in request.form:
        confirm = request.form['confirm_drop']
        columns_to_drop = request.form.getlist('columns_to_drop')  # Get the list of columns to drop

        if confirm == 'Yes':
            
            cleaned_data = drop_selected_columns(cleaned_data, columns_to_drop)
            data_head = process_uploaded_file(cleaned_data)

            if data_head is not None:
                return render_template('index.html', data_head=data_head.to_html(), col_name=data_head.columns.values.tolist())
            else:
                return render_template('index.html', error_message="An error occurred during column dropping.")
        else:
            return redirect(url_for('index'))

    return redirect(url_for('index'))
# %%
