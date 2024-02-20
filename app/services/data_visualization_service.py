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


def generate_boxplot(column_name):
    plt.figure(figsize=(10, 6))
    plt.boxplot(data_processing_controller.raw_data[column_name])
    plt.title('Boxplot of ' + column_name)
    plt.ylabel(column_name)
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

def generate_violineplot(column_name):
    plt.figure(figsize=(10, 6))
    plt.violinplot(data_processing_controller.raw_data[column_name])
    plt.title('Violinplot of ' + column_name)
    plt.ylabel(column_name)
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

def generate_density(column_name):
    plt.figure(figsize=(10, 6))
    data_processing_controller.raw_data[column_name].plot(kind='kde', color='skyblue')
    plt.title('Density Plot of ' + column_name)
    plt.xlabel(column_name)
    plt.ylabel('Density')
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

def generate_scatterplot(x_column, y_column):
    plt.figure(figsize=(10, 6))
    plt.scatter(data_processing_controller.raw_data[x_column], data_processing_controller.raw_data[y_column], color='skyblue')
    plt.title('Scatterplot of ' + x_column + ' vs ' + y_column)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
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


def generate_barplot(x_column, y_column, agg_type):
    plt.figure(figsize=(10, 6))
    grouped = data_processing_controller.raw_data.groupby(x_column)[y_column]
    if agg_type == 'mean':
        grouped.mean().plot(kind='bar', color='skyblue')
    elif agg_type == 'sum':
        grouped.sum().plot(kind='bar', color='skyblue')
    elif agg_type == 'count':
        grouped.count().plot(kind='bar', color='skyblue')
    # data_processing_controller.raw_data.groupby(x_column)[y_column].mean().plot(kind='bar', color='skyblue')
    plt.title('Barplot of ' + x_column + ' vs ' + y_column)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
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

def generate_line_chart(x_column, y_column, agg_type):
    plt.figure(figsize=(10, 6))
    grouped = data_processing_controller.raw_data.groupby(x_column)[y_column]
    if agg_type == 'mean':
        grouped.mean().plot(kind='line', color='skyblue')
    elif agg_type == 'sum':
        grouped.sum().plot(kind='line', color='skyblue')
    elif agg_type == 'count':
        grouped.count().plot(kind='line', color='skyblue')
    plt.title('Line Chart of ' + x_column + ' vs ' + y_column)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
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

def generate_piechart(column_name):
    plt.figure(figsize=(10, 6))
    data_processing_controller.raw_data[column_name].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['skyblue', 'lightgreen', 'lightcoral', 'orange', 'yellow'])
    plt.title('Piechart of ' + column_name)
    plt.axis('equal')
    plt.tight_layout()

    # Convert plot to PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convert PNG image to base64 string
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

def generate_corr_heatmap(continue_label):
    plt.figure(figsize=(10, 6))
    corr = data_processing_controller.raw_data[continue_label].corr()
    plt.matshow(corr, cmap='coolwarm', fignum=1)
    plt.colorbar()
    plt.title('Correlation Heatmap')
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.tight_layout()
    
    # Convert plot to PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convert PNG image to base64 string
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64




