#%%
# *****************************************************************************************TBU************************************************************************** #
# app/controllers/data_visualization_controller.py
''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

# from flask import render_template
# from app import app

# @app.route('/data-visualization')
# def data_visualization():
#     return render_template('data_visualization.html')

from flask import render_template, request
from app import app
from app.services.data_visualization_service import generate_histogram
from app.services import data_processing_service    



@app.route('/data-visualization')
def data_visualization():
    global custom_col_labels
    custom_col_labels = data_processing_service.custom_col_labels
    return render_template('data_visualization.html', custom_col_labels=custom_col_labels)

@app.route('/get-histogram', methods=['POST'])
def get_histogram():
    selected_column = request.form['column']
    # Logic to generate histogram for the selected_column
    histogram_image = generate_histogram(selected_column)  # Call the function to generate histogram image
    return render_template('data_visualization.html', custom_col_labels=custom_col_labels, histogram_image=histogram_image)


