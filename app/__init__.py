#%%
# app/__init__.py
from flask import Flask

app = Flask(__name__)
from config.config import Config
app.config.from_object(Config)

from app.controllers import data_processing_controller
from app.controllers import data_visualization_controller
from app.controllers import machine_learning_controller
