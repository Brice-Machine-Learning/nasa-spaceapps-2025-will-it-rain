# Brainstorm Questions

This document contains a list of brainstorm questions to help guide the development and improvement of our project. These questions are designed to spark creativity and encourage critical thinking.

## General Questions

1. Wat is the difference between time series analysis and time series forecasting?
2. How can we effectively handle missing data in our datasets?
3. What are the best practices for feature engineering in time series data?
4. How can we evaluate the performance of our forecasting models?
5. What are some examples of time series forecasting and time series analysis in real-world applications?
6. Are they typically used together or separately?
7. Do we need to train separate models for analysis and forecasting?
8. How do we train a model to do both analysis and forecasting?
9. What is the step-by-step process for building a time series forecasting model?

## Answered Questions

1. What is the difference between time series analysis and time series forecasting?
   - Time series analysis involves examining historical data to identify patterns, trends, and seasonal variations. It focuses on understanding the underlying structure of the data.
   - Time series forecasting, on the other hand, uses historical data to predict future values. It involves building models that can extrapolate from past trends to make informed predictions about future events.
2. How can we effectively handle missing data in our datasets?
   - Techniques for handling missing data include:
     - Imputation: Filling in missing values using statistical methods (mean, median, mode) or more advanced techniques like KNN or regression imputation.
     - Interpolation: Estimating missing values based on surrounding data points.
     - Deletion: Removing rows or columns with missing values, though this can lead to loss of valuable information.
     - Using models that can handle missing data natively, such as certain machine learning algorithms.
3. What are the best practices for feature engineering in time series data?
   - Best practices include:
     - Creating lag features to capture temporal dependencies.
     - Generating rolling statistics (mean, median, standard deviation) to capture trends.
     - Encoding cyclical features (e.g., day of the week, month) using sine and cosine transformations.
     - Normalizing or scaling features to ensure consistent ranges.
     - Using domain knowledge to create meaningful features that may impact the target variable.
4. How can we evaluate the performance of our forecasting models?
   - Common evaluation metrics for forecasting models include:
     - Mean Absolute Error (MAE)
     - Mean Squared Error (MSE)
     - Root Mean Squared Error (RMSE)
     - Mean Absolute Percentage Error (MAPE)
     - R-squared (for regression models)
   - Additionally, visualizing predictions against actual values can provide insights into model performance.
5. What are some examples of time series forecasting and time series analysis in real-world applications?
   - Examples include:
     - Stock price prediction
     - Weather forecasting
     - Sales forecasting
     - Demand forecasting in supply chain management
     - Anomaly detection in network traffic
6. Are they typically used together or separately?
   - Time series analysis and forecasting are often used together. Analysis helps in understanding the data, which can inform the development of more accurate forecasting models. However, they can also be used separately depending on the specific goals of a project.
7. Do we need to train separate models for analysis and forecasting?
   - Not necessarily. While some projects may benefit from separate models for analysis and forecasting, it is possible to use a single model for both purposes. The choice depends on the complexity of the data and the specific requirements of the task.
8. How do we train a model to do both analysis and forecasting?
   - To train a model for both analysis and forecasting, we can:
     - Use a multi-task learning approach where the model is designed to perform both tasks simultaneously.
     - Incorporate features that capture both historical patterns and future trends.
     - Use techniques like transfer learning, where a model trained for analysis is fine-tuned for forecasting.
9. What is the step-by-step process for building a time series forecasting model?
   - The process typically involves:
     1. Data Collection: Gather historical time series data.
     2. Data Preprocessing: Clean the data, handle missing values, and perform any necessary transformations.
     3. Exploratory Data Analysis (EDA): Analyze the data to identify patterns, trends, and seasonality.
     4. Feature Engineering: Create relevant features that capture temporal dependencies.
     5. Model Selection: Choose appropriate forecasting models (e.g., ARIMA, LSTM, Prophet).
     6. Model Training: Train the selected model(s) on the training dataset.
     7. Model Evaluation: Assess model performance using appropriate metrics and validation techniques.
     8. Hyperparameter Tuning: Optimize model parameters to improve performance.
     9. Model Deployment: Deploy the model for real-time forecasting or batch predictions.
    10. Monitoring and Maintenance: Continuously monitor model performance and update as necessary.
