#%%
# app/services/data_processing_service.py - Here goes the actual python code that we do in DS/ML Projects

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

import pandas as pd

from dataclasses import dataclass

from typing import List, Optional

import enum

import os
from dataclasses import dataclass
from typing import List, Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.utils.multiclass import type_of_target


from flask import request

custom_col_labels = {}

def process_uploaded_file(file):
    try:
        
        df = pd.read_csv(file)

        x_rows = 5  # Set a default value
        if 'x_rows' in request.form:
            x_rows = int(request.form['x_rows'])

        data_head = df.head(x_rows)

        return data_head  
    except Exception as e:
        # Handle exceptions, log or print an error message
        print(f"Error processing file: {e}")
        return None
    
    



## DONOT CHANGE THIS FILE


def col_labelling(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            custom_col_labels[col] = 'categorical'
        
        else:
            unique_values_ratio = len(df) / df[col].nunique()
            
            # max_nunique = data.nunique().max()

            
            if unique_values_ratio > 11:
                custom_col_labels[col] = 'categorical'
            else:
                custom_col_labels[col] = 'numerical'
                
                


class TaskType(enum.Enum):
    classification = 0
    regression = 1

    @staticmethod
    def from_str(task_type: str):
        if task_type == "classification":
            return TaskType.classification
        elif task_type == "regression":
            return TaskType.regression
        else:
            raise ValueError("Invalid task type: {}".format(task_type))

    @staticmethod
    def list_str():
        return ["classification", "regression"]


class ProblemType(enum.IntEnum):
    binary_classification = 1
    multi_class_classification = 2
    multi_label_classification = 3
    single_column_regression = 4
    multi_column_regression = 5

    @staticmethod
    def from_str(label):
        if label == "binary_classification":
            return ProblemType.binary_classification
        elif label == "multi_class_classification":
            return ProblemType.multi_class_classification
        elif label == "multi_label_classification":
            return ProblemType.multi_label_classification
        elif label == "single_column_regression":
            return ProblemType.single_column_regression
        elif label == "multi_column_regression":
            return ProblemType.multi_column_regression
        else:
            raise NotImplementedError
        
        
@app.route('/column_type_selection', methods=['POST'])
def column_type_selection():
    # global data_head
    try:
        global data_head
        col_names = data_head.columns.tolist()
        print("Hello")
        # col_names = data_head.columns.tolist()
        if request.method == 'POST':
            selected_column_types = {}
            print("Hello")
            for column in col_names:
                selected_column_types[column] = request.form.get(column)

            print(selected_column_types)

                
                



@dataclass
class Model_Auto:
    train_filename: str
    # output: str

    # optional arguments
    # test_filename: Optional[str] = None
    task: Optional[str] = None
    idx: Optional[str] = "id"
    targets: Optional[List[str]] = None
    features: Optional[List[str]] = None
    categorical_features: Optional[List[str]] = None
    # num_folds: Optional[int] = 5
    seed: Optional[int] = 42
    
    
    def __init__(self):
        if self.targets is None:
            print("No target columns specified. Will default to `target`.")
            self.targets = ["target"]

        if self.idx is None:
            print("No id column specified. Will default to `id`.")
            self.idx = "id"
            
            
    
    def _determine_problem_type(self, train_df):
        if self.task is not None:
            if self.task == "classification":
                if len(self.targets) == 1:
                    if len(np.unique(train_df[self.targets].values)) == 2:
                        problem_type = ProblemType.binary_classification
                    else:
                        problem_type = ProblemType.multi_class_classification
                else:
                    problem_type = ProblemType.multi_label_classification

            elif self.task == "regression":
                if len(self.targets) == 1:
                    problem_type = ProblemType.single_column_regression
                else:
                    problem_type = ProblemType.multi_column_regression
            else:
                raise Exception("Problem type not understood")
        else:
            target_type = type_of_target(train_df[self.targets].values)
            
            
            
    
    def _inject_idxumn(self, df):
        if self.idx not in df.columns:
            df[self.idx] = np.arange(len(df))
        return df
    
    
    


            
            
        
            
            
            
            
            
    def _process_data(self):
        print("Reading training data")
        train_df = pd.read_csv(self.train_filename)
        problem_type = self._determine_problem_type(train_df)

        train_df = self._inject_idxumn(train_df)
        if self.test_filename is not None:
            test_df = pd.read_csv(self.test_filename)
            test_df = self._inject_idxumn(test_df)


        # create folds
        # train_df = self._create_folds(train_df, problem_type)
        # ignore_columns = [self.idx, "kfold"] + self.targets

        if self.features is None:
            self.features = list(train_df.columns)

        # encode target(s)
        if problem_type in [ProblemType.binary_classification, ProblemType.multi_class_classification]:
            print("Encoding target(s)")
            target_encoder = LabelEncoder()
            target_encoder.fit(
                train_df[self.targets].values.reshape(
                    -1,
                )
            )
            train_df.loc[:, self.targets] = target_encoder.transform(
                train_df[self.targets].values.reshape(
                    -1,
                )
            )
        else:
            target_encoder = None

        if self.categorical_features is None:
            # find categorical features
            categorical_features = []
            for col in self.features:
                if train_df[col].dtype == "object":
                    categorical_features.append(col)

        else:
            categorical_features = self.categorical_features

        print(f"Found {len(categorical_features)} categorical features.")
        
        if len(categorical_features) > 0:
            ord_encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan)
            train_df[categorical_features] = ord_encoder.fit_transform(train_df[categorical_features].values)
            
        
        
        
        

                

