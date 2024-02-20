#%%
# ******************************************************************************TBU*******************************************************************#
# app/controllers/machine_learning_controller.py


''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

from app import app
from flask import render_template, request, jsonify
from app.services.machine_learning_service import get_variables_by_type
from app.controllers import data_processing_controller 

problem_type = None 
selected_variable = None 

@app.route('/machine-learning', methods=['GET', 'POST'])
def machine_learning():
    global problem_type
    if request.method == 'POST':
        problem_type = request.form['problem_type'].lower()  # Get the problem type input and convert to lowercase
        variables = get_variables_by_type(problem_type)
        print(problem_type, variables)
        return render_template('machine_learning.html', problem_type=problem_type, variables=variables)
    return render_template('machine_learning.html')

@app.route('/variable-selection', methods=['POST'])
def variable_selection():
    global selected_variable
    if request.method == 'POST':
        selected_variable = request.form['column']
        return render_template('machine_learning.html', selected_variable=selected_variable)
    
