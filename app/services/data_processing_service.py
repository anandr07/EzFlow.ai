#%%
import pandas as pd
from app import db  # Add the import for db
from app.models.database_models import RawData, ProcessedData

def process_data(imputation_type='mean', encoding_type='label'):  # Add encoding_type as a parameter
    raw_data = pd.read_sql(db.session.query(RawData).statement, db.session.bind)
    
    # Handle missing values based on user choice (Just a sample To be Modified Later)
    if imputation_type == 'mean':
        processed_data = raw_data.fillna(raw_data.mean())
    elif imputation_type == 'median':
        processed_data = raw_data.fillna(raw_data.median())
    elif imputation_type == 'mode':
        processed_data = raw_data.fillna(raw_data.mode().iloc[0])
    else:
        processed_data = raw_data
    
    # Label columns as Continuous or Categorical (Just a sample To be Modified Later)
    for column in processed_data.columns:
        if pd.api.types.is_numeric_dtype(processed_data[column]):
            processed_data[f"{column}_label"] = "Continuous"
        else:
            processed_data[f"{column}_label"] = "Categorical"
            
            # Encode categorical data based on user choice (Just a sample To be Modified Later)
            if encoding_type == 'label':
                processed_data[column] = processed_data[column].astype('category').cat.codes
            elif encoding_type == 'one_hot':
                processed_data = pd.get_dummies(processed_data, columns=[column], prefix=[column])
    
    # Add logic to save labeled and encoded data in ProcessedData table (Just a sample To be Modified Later)
    processed_data.to_sql('processed_data', con=db.engine, index=False, if_exists='replace')
    return {'message': 'Data processed successfully!'}

## DONOT CHANGE THIS FILE 