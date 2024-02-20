#%%
# app/services/data_visualization_service.py
''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg') # DONOT REMOVE THIS
import io
import base64
from app.controllers import data_processing_controller


def generate_histogram(column_name):

    plt.figure(figsize=(10, 6))
    plt.hist(data_processing_controller.raw_data[column_name], bins=20, color='skyblue', edgecolor='black')
    plt.title('Histogram of ' + column_name)
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()

    # Convert plot to PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convert PNG image to base64 string
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

