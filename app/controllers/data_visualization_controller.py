#%%
# *****************************************************************************************TBU************************************************************************** #

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

from flask import render_template
from app import app

@app.route('/data-visualization')
def data_visualization():
    return render_template('data_visualization.html')


# Import necessary libraries
# import pandas as pd
# from flask import render_template
# from app import app

# # Sample continuous data for demonstration
# continuous_data = {'Age': [25, 30, 35, 40, 45],
#                    'Income': [50000, 60000, 70000, 80000, 90000]}

# @app.route('/data-visualization')
# def data_visualization():
#     # Pass continuous variable names and data to the template
#     continuous_variable_names = list(continuous_data.keys())
#     return render_template('data_visualization.html', continuous_variable_names=continuous_variable_names)
