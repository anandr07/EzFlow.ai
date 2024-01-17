#%%
# Just a trial - TBU
from app import create_app
from app.controllers import data_processing_controller, machine_learning_controller, data_visualization_controller

app = create_app(template_folder='C:/Anand/Projects_GWU/EzFlow.ai/templates')

if __name__ == '__main__':
    app.run(debug=True)
