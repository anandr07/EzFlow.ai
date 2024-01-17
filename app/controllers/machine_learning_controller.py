#%%
from flask import render_template, request, jsonify
from app import db, create_app

app = create_app()

@app.route('/machine_learning')
def machine_learning():
    return render_template('machine_learning.html')
