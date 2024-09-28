# Imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor

from preprocessing import data_preprocessing

# Predefined color palettes
color_palette_1 = ['#FF6C3E']    # 1 color for the chart
color_palette_2 = ['#FF6C3E','#3ED1FF']    # 2 colors for the chart
color_palette_3 = ['#FF6C3E','#3ED1FF','#70FF3E']    # 3 colors for the chart
color_palette_4 = ['#FF6C3E','#3ED1FF','#70FF3E','#CD3EFF']    # 4 colors for the chart

# Predefined font sizes for axes and title
fontsize_title = 20
fontsize_axes = 15

def visualizing_forecasts(y_test_future):
    # Import merge_train from preprocessing.py
    merge_train, merge_test = data_preprocessing()

    # Save 'Date' from merge_test in a variable
    future_dates = merge_test['Date']  # for later visualization in visualizing_forecasts

    # Enrich predictions with 'Date', 'Store', and 'Dept' for visualization and table
    y_test_future_with_date = y_test_future.copy()
    y_test_future_with_date['Date'] = future_dates
    y_test_future_with_date['Store'] = merge_test['Store']  # Add Store
    y_test_future_with_date['Dept'] = merge_test['Dept']    # Add Dept
    y_test_future_with_date['Year'] = pd.to_datetime(future_dates).dt.year  # Extract year
    y_test_future_with_date['Month'] = pd.to_datetime(future_dates).dt.month  # Extract month

    # Obtain historical values for the chart
    historical_values_for_diagram = merge_train[['Date', 'Weekly_Sales']]

    # Create line chart
    sns.set_style('darkgrid')
    fig1, ax1 = plt.subplots(figsize=(15, 6))

    # Plot historical values
    historical_values_for_diagram.groupby('Date')['Weekly_Sales'].mean().plot(label='Historical', ax=ax1)
    
    # Plot predicted values
    y_test_future_with_date.groupby('Date')['Weekly_Sales'].mean().plot(color='orange', label='Predicted', ax=ax1)

    ax1.legend(loc='best', fontsize=12)
    ax1.set_ylabel('Sales', fontsize=12)
    ax1.set_xlabel('')
    ax1.set_title('Historical vs. Predicted Sales', fontsize=14)

    st.pyplot(fig1)

    # Create tables
    st.markdown('Sales Forecasts:')

    # Create table and group by Date, Store, Dept
    table1 = y_test_future_with_date[['Date', 'Store', 'Dept', 'Weekly_Sales']]
    table1['Date'] = pd.to_datetime(table1['Date']).dt.strftime('%Y-%m-%d')

    # Display the table, grouped by Date, Store, Dept
    daily_forecasts = table1.groupby(['Date', 'Store', 'Dept'])['Weekly_Sales'].mean().round(2)
    
    st.dataframe(daily_forecasts)

# Evaluate model performance on training and test datasets
def evaluate_model(model, X_train, y_train, X_test, y_test):

    # Predictions on training and test data
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Calculate metrics on training data
    mse_train = mean_squared_error(y_train, y_train_pred)
    rmse_train = np.sqrt(mse_train)
    mae_train = mean_absolute_error(y_train, y_train_pred)
    r2_train = r2_score(y_train, y_train_pred)

    # Calculate metrics on test data
    mse_test = mean_squared_error(y_test, y_test_pred)
    rmse_test = np.sqrt(mse_test)
    mae_test = mean_absolute_error(y_test, y_test_pred)
    r2_test = r2_score(y_test, y_test_pred)

    return mse_train, rmse_train, mae_train, r2_train, mse_test, rmse_test, mae_test, r2_test

@st.cache_resource
def sales_forecast():

    # Import merge_train and merge_test
    merge_train, merge_test = data_preprocessing()

    # Split training data (train.csv) into train and test
    X = merge_train.drop(['Date','Year', 'Month', 'Weekly_Sales', 'Fuel_Price','Temperature','Type','MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5','CPI','IsHoliday', 'Unemployment', 'Super_Bowl', 'Labor_Day', 'Thanksgiving', 'Christmas','Easter'], axis=1)
    y = merge_train['Weekly_Sales']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

    # Train the model
    model = XGBRegressor(n_jobs=-1, random_state=42, n_estimators=1000, learning_rate=0.9, max_depth=15, subsample=0.9, colsample_bytree=0.7)
    model.fit(X_train, y_train)

    # Check for overfitting and underfitting
    mse_train, rmse_train, mae_train, r2_train, mse_test, rmse_test, mae_test, r2_test = evaluate_model(model, X_train, y_train, X_test, y_test)

    # Test dataset for estimation and visualization of forecasts
    X_test_future = merge_test.drop(['Date','Year', 'Month', 'Fuel_Price','Temperature','Type','MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5','CPI','IsHoliday', 'Unemployment'], axis=1)

    # Generate forecasts
    predictions = model.predict(X_test_future)
    y_test_future = pd.DataFrame({'Weekly_Sales': predictions})

    # Visualize historical data and forecasts
    visualizing_forecasts(y_test_future)

    # Evaluate model performance
    st.write(f'\nEvaluation Results:')
    st.write(f'Training MSE: {mse_train:.4f}, RMSE: {rmse_train:.4f}, MAE: {mae_train:.4f}, R²: {r2_train:.4f}')
    st.write(f'Test MSE: {mse_test:.4f}, RMSE: {rmse_test:.4f}, MAE: {mae_test:.4f}, R²: {r2_test:.4f}')

    if rmse_test > rmse_train and (rmse_test - rmse_train) > 0.1 * rmse_train:
        st.write(f'\nWarning: Potential overfitting. Test RMSE is significantly higher than Train RMSE.')
    elif rmse_train > rmse_test:
        st.write(f'\nWarning: Potential underfitting. Train RMSE is higher than Test RMSE.')
    else:
        st.write(f'\nThe model seems to be well-balanced.')
