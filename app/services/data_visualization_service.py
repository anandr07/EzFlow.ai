#%%

''' Make sure to handle exceptions, and scale the code accordingly.
If a new change is made make sure it doesn't affect the earlier codes.
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.models.database_models import ProcessedData

def visualize_data():
    processed_data = pd.read_sql(db.session.query(ProcessedData).statement, db.session.bind)
    
    # Add logic for data visualization - To Be Updated
    # For example, a correlation matrix heatmap, scatter plot etc... To be Decided
    plt.figure(figsize=(12, 10))
    sns.heatmap(processed_data.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Matrix Heatmap')
    plt.show()
    
    return {'message': 'Data visualized successfully!'}


#  num_bins, density = 1,color ='green',alpha = 0.7


colors = ['green', 'blue', 'lime']


def hist_plot(df, bins, color):
    colors = ['green', 'blue', 'lime']
    col_names = df.columns
    for i, e in enumerate(col_names):
        plt.hist(df[i].values, bins, color=colors)
        
