#%%
# Basic Elements added: 
#%%
# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=True)
app.template_folder = 'templates'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

from app.controllers import data_processing_controller, machine_learning_controller, data_visualization_controller
