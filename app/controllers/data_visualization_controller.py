#%%

from flask import render_template, request, jsonify
from app import db, create_app

app = create_app()

@app.route('/data_visualization')
def data_visualization():
    return render_template('data_visualization.html')
