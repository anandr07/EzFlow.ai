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


