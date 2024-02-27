

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
from app.services.data_processing_service import drop_selected_columns, process_uploaded_file, col_labelling,correct_category_dtype
from app.services.data_processing_service import perform_imputation, display_rows_with_na_values,dropping_rows_with_na_values, manual_col_labelling, find_id_column,process_dataframe_remove_id

# Here the data is being declared globally
cleaned_data=None
raw_data=None

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/')
def index():
    
    return render_template('index.html', data_head=None,data_impute=None,imputation_attempted=False,dropping_rows_attempted=False,dropping_rows_attempted_1=False,rows_before=None,features_dropped=None)  # Pass data_head and data_impute as None initially The imputation_attempted should be False as we dont want to display any thing from the data_imputation button if its not clicked
  # Pass data_head and data_impute as None initially The imputation_attempted should be False as we dont want to display any thing from the data_imputation button if its not clicked


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
    


@app.route('/displaying_rows_with_na_values' , methods=['POST'])
def display_rows_na_values():
    global cleaned_data
    try:
        dropping_rows_attempted_1=True
        features_dropped,rows_before = display_rows_with_na_values(cleaned_data)
        return render_template('index.html',dropping_rows_attempted_1=dropping_rows_attempted_1, features_dropped = features_dropped.to_html(),rows_before=rows_before) # Here the  data after dropping the rows is outputted in the webpage

    except Exception as e:
        return render_template('index.html', error_message=f"An error occured while dropping rows with missing values: {e}", dropping_rows_attempted_1=dropping_rows_attempted_1)


        
@app.route('/dropping_rows_with_missing_values' , methods=['POST'])
def dropping_rows_na_values():
     global cleaned_data #here the data is being called for global scope
     dropping_rows_attempted=True
     try:
         threshold = float(request.form['threshold'])#
         df_cleaned, features_dropped__1,rows = dropping_rows_with_na_values(cleaned_data, threshold)
         data_head = df_cleaned.head()
         print('-----------',data_head)
         
         print('--------------------------------',rows)
        #  return render_template('index.html',data_head = data_head.to_html(), dropping_rows_attempted=dropping_rows_attempted, features_na_values_perc = features_na_values_perc.to_html()) # Here the  data after dropping the rows is outputted in the webpage
         return render_template('index.html',data_head = data_head.to_html(),dropping_rows_attempted=dropping_rows_attempted, features_dropped_1 = features_dropped__1,rows=rows) # Here the  data after dropping the rows is outputted in the webpage

     except Exception as e:
         return render_template('index.html', error_message=f"An error occured while dropping rows with missing values: {e}", dropping_rows_attempted=dropping_rows_attempted)

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
@app.route('/remove_duplicate_rows', methods=['POST'])
def remove_duplicate_rows():
    global cleaned_data, raw_data
    removing_duplicate_rows_attempted=True
    try:
        
        if cleaned_data is not None:   #picking up the last modified data
            prev_length = len(cleaned_data)
            cleaned_data.drop_duplicates(inplace=True)
            removed_rows = prev_length - len(cleaned_data)
            message = f"{removed_rows} duplicate rows removed."
            print(message)
            print(removing_duplicate_rows_attempted)
            return render_template('index.html', message=message, removing_duplicate_rows_attempted = removing_duplicate_rows_attempted)
        elif raw_data is not None:      #in case, user wants to operate on original data
            prev_length = len(raw_data)
            raw_data.drop_duplicates(inplace=True)
            removed_rows = prev_length - len(raw_data)
            message = f"{removed_rows} duplicate rows removed."
            print(message)
            return render_template('index.html', message=message, removing_duplicate_rows_attempted = removing_duplicate_rows_attempted)
        else:
            message = "No data available to remove duplicates."
            print(message)
            return render_template('index.html', message=message, removing_duplicate_rows_attempted = removing_duplicate_rows_attempted)            
    except Exception as e:
        message = f"An error occurred while removing duplicate rows: {e}"
        print(message)
        return render_template('index.html', message=message, removing_duplicate_rows_attempted = removing_duplicate_rows_attempted)


@app.route('/encoding_options', methods=['POST'])
def encoding_options():
    global cleaned_data
    encoding_attempted = True
    # Get the selected encoding method from the form
    encoding_method = request.form['encoding_method']
    if encoding_method == 'label_encoding':
        # Perform label encoding
        label_encoder = LabelEncoder()
        for column in cleaned_data.select_dtypes(include=['object']).columns:
            cleaned_data[column] = label_encoder.fit_transform(cleaned_data[column])
        message = "Label Encoding Applied"
        print(message)
    elif encoding_method == 'one_hot_encoding':
        # Perform one-hot encoding
        cleaned_data = pd.get_dummies(cleaned_data, drop_first=True)
        message = "One-Hot Encoding Applied"
        print(message)
    else:
        # Invalid encoding method selected
        message = "Invalid Encoding Method"
        print(message)
    # Render the template with the appropriate message
    return render_template('index.html', message=message, encoding_attempted=encoding_attempted)

@app.route('/outlier_removal', methods=['POST'])
def outlier_removal():
    global cleaned_data
    removing_outliers_attempted = True
    method = request.form['outlier_removal_method']

    if method == 'isolation_forest':
        outlier_removal_model = IsolationForest()
    elif method == 'minimum_covariance_determinant':
        outlier_removal_model = EllipticEnvelope()
    elif method == 'local_outlier_factor':
        outlier_removal_model = LocalOutlierFactor(novelty=False)
    elif method == 'one_class_svm':
        outlier_removal_model = OneClassSVM()

    try:
        outliers = outlier_removal_model.fit_predict(cleaned_data)
        outliers_removed = cleaned_data[outliers == 1]

        num_outliers = len(cleaned_data) - len(outliers_removed)
        
        cleaned_data.drop(cleaned_data.index[outliers != 1], inplace=True)  #modifying the dataset after outlier removal
        message = f"{num_outliers} outliers removed using {method}."
        print(message)       
        return render_template('index.html', message=message, removing_outliers_attempted = removing_outliers_attempted)
    except Exception as e:
        error_message = f"An error occurred during outlier removal: {e}"
        print(error_message)
        return render_template('index.html', error_message=error_message, removing_outliers_attempted=removing_outliers_attempted)
    

# %%
@app.route('/identify_id_column', methods=['POST'])
def identify_id_column():
    atm=True
    global cleaned_data
    id_column = find_id_column(cleaned_data)
    if id_column is None:
        return render_template('index.html', error_message='No Id Column',id_col=None,atm=True)
    else:
        return render_template('index.html', error_message="Id column is there",id_col=id_column.to_html(),atm=True)
@app.route('/remove_id_column', methods=['POST'])
def remove_id_column():
    global cleaned_data
    data = process_dataframe_remove_id(cleaned_data, drop_id=True)
    return render_template('index.html', data_id=data.to_html())