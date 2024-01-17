#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.models.database_models import ProcessedData

def visualize_data():
    processed_data = pd.read_sql(db.session.query(ProcessedData).statement, db.session.bind)
    
    # Add logic for data visualization
    # For example, a correlation matrix heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(processed_data.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Matrix Heatmap')
    plt.show()
    
    return {'message': 'Data visualized successfully!'}
