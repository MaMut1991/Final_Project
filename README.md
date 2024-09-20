# Final project

Sales Forecasting - Increasing Efficiency through Machine Learning

### Introduction to the fictional story
Imagine you run a successful retail business. You always want your shelves to be stocked with the right products—neither too much nor too little. However, reality often looks different: one day you have excess inventory that spoils and incurs costs. The next day, your shelves are empty because demand was underestimated, leaving your customers disappointed.

Finding the balance is an art—but also a huge challenge. Traditional sales forecasting methods are time-consuming and often inaccurate. The consequences? High storage costs, frustrated customers, and missed revenue opportunities.

But now, imagine you had a solution. An app that works like an experienced sales forecasting expert but is more precise and efficient. This app leverages cutting-edge technologies such as machine learning to analyze your sales data and tell you exactly which products are needed and in what quantities.

This opportunity gave rise to the idea for my final project: to develop a prototype app to analyze historical sales data, visualize it, and forecast future sales. In addition to historical data, external factors such as holidays, weather, the consumer price index, oil prices, promotional activities, and regional unemployment will also be considered.

### Dataset description
For the prototype, five CSV files from the Kaggle competition "Walmart Recruiting - Store Sales Forecasting" are available.

https://www.kaggle.com/competitions/walmart-recruiting-store-sales-forecasting/overview

##### Available Files:

Historical sales data for 45 Walmart stores in various regions is available. Each store contains a number of departments, and the task is to predict department-wide sales for each store.

Additionally, Walmart runs several promotional discount events throughout the year, which precede major holidays. The four biggest are the Super Bowl, Labor Day, Thanksgiving, and Christmas.

##### stores.csv

This file contains anonymized information about the 45 stores, indicating the type and size of the store.

- Store: The store number (Primary Key)
- Type: The type of store (A, B, C)
- Size: The size of the store
- train.csv

These are the historical training data spanning from 02/05/2010 to 11/01/2012. This file contains the following fields:

- Store: The store number (Primary Key)
- Dept: The department number
- Date: The date of the respective week (Secondary Key)
- Weekly_Sales: Sales for the respective department in the respective store
- IsHoliday: Whether the week is a holiday week
- test.csv

This file is identical to train.csv, except the weekly sales are withheld. The task is to predict sales for each triplet of store, department, and date in this file.

##### features.csv

This file contains additional data related to the store, department, and regional activity for the given dates. It includes the following fields:

- Store: The store number (Primary Key)
- Date: The date of the respective week (Secondary Key)
- Temperature: The average temperature in the region
- Fuel_Price: Fuel prices in the region
- MarkDown1-5: Anonymized data related to promotional discounts run by Walmart. MarkDown data is only available after November 2011 and is not always available for all stores. Any missing value is marked as NA.
- CPI: The Consumer Price Index
- Unemployment: The unemployment rate
- IsHoliday: Whether the week is a holiday week
For simplicity, the four holidays fall within the following weeks in the dataset (not all holidays are included):
Super Bowl: February 12, 2010; February 11, 2011; February 10, 2012; February 8, 2013
Labor Day: September 10, 2010; September 9, 2011; September 7, 2012; September 6, 2013
Thanksgiving: November 26, 2010; November 25, 2011; November 23, 2012; November 29, 2013
Christmas: December 31, 2010; December 30, 2011; December 28, 2012; December 27, 2013

### Approach

- Develop a function to create charts or a dashboard for the app.
- Develop a function that trains models, validates them, selects the best model, tunes hyperparameters if necessary, and generates sales forecasts.
- Develop a Streamlit app to visualize the charts and forecasts. Parameters can be adjusted and passed to the two functions above to customize the analysis results.
- 
Three Python files will be created: main.py, dashboard.py, and model.py.
- main.py: This file creates the Streamlit app and controls the function calls of the other files.
- data.py: This file analyzes the sales data and visualizes it in the form of charts.
- model.py: In this file, models will be trained, validated, the best model selected, hyperparameters tuned, and sales forecasts generated.

List of Supervised Models Used:
- Random Forest
- Lasso Regression
- XGBoost
  
The final model evaluation will be based on MSE, MAE, RMSE, and R² (coefficient of determination). These evaluation metrics will not only assess the model's accuracy but also check for overfitting or underfitting. To determine and fine-tune the optimal model, negative MSE (neg_mse) will be used for evaluation.
