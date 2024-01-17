#%%

from datetime import datetime
from app import db

class RawData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add necessary columns based on your data
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ProcessedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add necessary columns based on your processed data
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
