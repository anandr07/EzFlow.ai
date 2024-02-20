#%%
# ******************************************************************************TBU*******************************************************************#
# app/controllers/machine_learning_controller.py


''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

from app import app
from flask import render_template, request, jsonify

@app.route('/machine-learning', methods=['GET', 'POST'])
def machine_learning():
    if request.method == 'POST':
        problem_type = request.form['problem_type'].lower()  # Get the problem type input and convert to lowercase
        print(problem_type)
        # Handle exceptions or additional logic as needed
        return render_template('machine_learning.html', problem_type=problem_type)
    return render_template('machine_learning.html')

