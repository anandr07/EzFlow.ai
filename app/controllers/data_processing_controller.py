#%%
# data_processing_controller.py
from flask import render_template, request, jsonify
from app import db, app  # Import app instance

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_data', methods=['POST'])
def upload_data():
    file = request.files['file']
    # Add logic to save the file or parse data as needed

    # Render the same HTML page (for now)
    return render_template('index.html')

@app.route('/process_data', methods=['POST'])
def process_data_route():
    imputation_type = request.json.get('imputation_type', 'mean')
    # Assuming process_data is a function defined in data_processing_service.py
    from app.services.data_processing_service import process_data
    result = process_data(imputation_type)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)


