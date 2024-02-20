#%%
# *****************************************************************************************TBU************************************************************************** #
# app/controllers/data_visualization_controller.py
''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

# from flask import render_template
# from app import app

# @app.route('/data-visualization')
# def data_visualization():
#     return render_template('data_visualization.html')

from flask import render_template, request
from app import app
from app.services.data_visualization_service import generate_histogram, generate_boxplot, generate_scatterplot, generate_barplot, generate_piechart, generate_corr_heatmap, generate_line_chart, generate_violineplot, generate_density
from app.services import data_processing_service    



@app.route('/data-visualization')
def data_visualization():
    global col_labels
    col_labels = data_processing_service.col_labels
    return render_template('data_visualization.html', col_labels=col_labels)

@app.route('/get-histogram', methods=['POST'])
def get_histogram():
    selected_column = request.form['column']
    # Logic to generate histogram for the selected_column
    histogram_image = generate_histogram(selected_column)  # Call the function to generate histogram image
    return render_template('data_visualization.html', col_labels=col_labels, histogram_image=histogram_image)

# *****************************************************************************************TBU************************************************************************** #

@app.route('/get-violine', methods=['POST'])
def get_violine():
    selected_column = request.form['column']
    # Logic to generate histogram for the selected_column
    violine_image = generate_violineplot(selected_column)
    return render_template('data_visualization.html', col_labels=col_labels, violine_image=violine_image)

# *****************************************************************************************TBU************************************************************************** #

@app.route('/get-boxplot', methods=['POST'])
def get_boxplot():
    print(request.form)
    selected_column = request.form['column']
    # Logic to generate boxplot for the selected_column
    boxplot_image = generate_boxplot(selected_column)
    return render_template('data_visualization.html', col_labels=col_labels, boxplot_image=boxplot_image)

# *****************************************************************************************TBU************************************************************************** #

@app.route('/get-density', methods=['POST'])
def get_density():
    print(request.form)
    selected_column = request.form['column']
    # Logic to generate boxplot for the selected_column
    density_image = generate_density(selected_column)
    return render_template('data_visualization.html', col_labels=col_labels, density_image=density_image)

# *****************************************************************************************TBU************************************************************************** #

@app.route('/get-scatterplot', methods=['POST'])
def get_scatterplot():
    x_column = request.form['x_column']
    y_column = request.form['y_column']
    # Logic to generate scatterplot for the x_column and y_column
    scatterplot_image = generate_scatterplot(x_column, y_column)
    return render_template('data_visualization.html', col_labels=col_labels, scatterplot_image=scatterplot_image)

# *****************************************************************************************TBU************************************************************************** #

@app.route('/get_barplot', methods=['POST'])
def get_barplot():
    x_column = request.form['x_column']
    y_column = request.form['y_column']
    agg_type = request.form['agg_type']
    # Logic to generate barplot for the selected_column
    barplot_image = generate_barplot(x_column, y_column, agg_type)
    return render_template('data_visualization.html', col_labels=col_labels, barplot_image=barplot_image)

# *****************************************************************************************TBU************************************************************************** #

@app.route('/get-piechart', methods=['POST'])
def get_piechart():
    selected_column = request.form['column']
    # Logic to generate piechart for the selected_column
    piechart_image = generate_piechart(selected_column)
    return render_template('data_visualization.html', col_labels=col_labels, piechart_image=piechart_image)

# *****************************************************************************************TBU************************************************************************** #

@app.route('/get-corr-heatmap', methods=['POST'])
def get_corr_heatmap():
    continue_label = [i for i in col_labels if col_labels[i] == 'continuous']
    heatmap_image = generate_corr_heatmap(continue_label)
    return render_template('data_visualization.html', col_labels=col_labels, heatmap_image=heatmap_image)

# *****************************************************************************************TBU************************************************************************** #

@app.route('/get-linechart', methods=['POST'])
def get_linechart():
    x_column = request.form['x_column']
    y_column = request.form['y_column']
    agg_type = request.form['agg_type']
    # Logic to generate line chart for the x_column and y_column
    linechart_image = generate_line_chart(x_column, y_column, agg_type)
    return render_template('data_visualization.html', col_labels=col_labels, linechart_image=linechart_image)