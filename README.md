# Under Construction :))
# EzFlow.ai
Welcome to EzFlow.ai , your go-to platform for effortlessly turning raw tabular data into powerful machine learning models! EzFlow.ai is an intuitive and user-friendly software product designed to democratize machine learning, making it accessible to everyone, regardless of their expertise.

# EzFlow.ai

## Process Flow / Architecture

### User Interaction:

1. User uploads data through the UI.
2. Specifies ML options and preferences.

**Tools:**
- Frontend: Developed using React for an interactive and responsive UI.
- File Upload: Utilizing Dropzone library for handling data uploads.
- Communication: Axios for sending user configurations to the backend.

### Backend Processing:

1. Backend (Flask) receives data and configurations.
2. Processes data (labeling, encoding, imputation) using Pandas.
3. Stores processed data in the database (PostgreSQL).

**Tools:**
- Backend: Flask (Python) for handling user requests and processing data.
- Database: PostgreSQL for storing processed data.
- Data Processing: Pandas for efficient data manipulation.

### Machine Learning Model Training:

1. Backend triggers a virtual machine for model training.
2. Virtual machine (AWS EC2) loads processed data, preprocesses it further.
3. Trains machine learning models using Scikit-learn, TensorFlow, or PyTorch.
4. Stores results back in the database.

**Tools:**
- Virtual Machine: AWS EC2 for scalable and flexible computing resources.
- Containerization: Docker for creating isolated environments.
- Machine Learning: Scikit-learn, TensorFlow, or PyTorch for training models.

### Result Display:

1. User accesses results through the UI.
2. Compares models and reviews predictions.

**Tools:**
- Frontend: React for dynamic result display.
- Communication: Axios for fetching results from the backend.
- Visualization: D3.js or Chart.js for presenting model comparisons.

---

This comprehensive process flow involves a user-friendly frontend, a robust backend utilizing Flask and Pandas for data processing, a PostgreSQL database for efficient data storage, a scalable AWS EC2 virtual machine for model training, and popular machine learning libraries for building and training models.
