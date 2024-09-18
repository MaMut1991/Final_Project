import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from preprocessing import data_preprocessing

# Funktion für die Visualisierung der Prognosen
def visualizing_forecasts(past_dates, future_dates, y_test_future, merge_train):
    y_test_future_with_dates = y_test_future.copy()
    y_test_future_with_dates['Date'] = future_dates
    y_train_with_dates = merge_train[['Date', 'Weekly_Sales']]

    # Erstellung des Diagramms
    sns.set_style('darkgrid')
    plt.figure(figsize=(15, 5))

    # Historische Daten plotten
    y_train_with_dates.groupby('Date')['Weekly_Sales'].mean().plot(label='Historisch')

    # Prognostizierte Daten plotten
    y_test_future_with_dates.groupby('Date')['Weekly_Sales'].mean().plot(color='orange', label='Prognostiziert')

    plt.legend(loc='best', fontsize=16)
    plt.ylabel('Sales', fontsize=16)
    plt.xlabel('Date', fontsize=16)
    plt.title('Historische vs. Prognostizierte Sales', fontsize=18)

    # Ausgabe des Plots in Streamlit
    st.pyplot(plt.gcf())

# Funktion zur Modellauswertung
def evaluate_model(model, X_train, y_train, X_test, y_test):
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    mse_train = mean_squared_error(y_train, y_train_pred)
    rmse_train = np.sqrt(mse_train)
    mae_train = mean_absolute_error(y_train, y_train_pred)
    r2_train = r2_score(y_train, y_train_pred)

    mse_test = mean_squared_error(y_test, y_test_pred)
    rmse_test = np.sqrt(mse_test)
    mae_test = mean_absolute_error(y_test, y_test_pred)
    r2_test = r2_score(y_test, y_test_pred)

    return mse_train, rmse_train, mae_train, r2_train, mse_test, rmse_test, mae_test, r2_test

# Funktion für den Forecast
def sales_forecast():
    merge_train, merge_test = data_preprocessing()
    past_dates = merge_train['Date']
    future_dates = merge_test['Date']

    X = merge_train.drop(['Date', 'Year', 'Weekly_Sales', 'MarkDown1', 'MarkDown2', 'MarkDown4', 'MarkDown3', 'MarkDown5', 'CPI', 'Unemployment', 'Temperature', 'Fuel_Price'], axis=1)
    y = merge_train['Weekly_Sales']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

    # Modell trainieren
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Modell evaluieren
    mse_train, rmse_train, mae_train, r2_train, mse_test, rmse_test, mae_test, r2_test = evaluate_model(model, X_train, y_train, X_test, y_test)

    # Metriken in Streamlit anzeigen
    st.write(f"### Modellauswertung:")
    st.write(f"**Training MSE**: {mse_train:.4f}, **RMSE**: {rmse_train:.4f}, **MAE**: {mae_train:.4f}, **R²**: {r2_train:.4f}")
    st.write(f"**Test MSE**: {mse_test:.4f}, **RMSE**: {rmse_test:.4f}, **MAE**: {mae_test:.4f}, **R²**: {r2_test:.4f}")

    if rmse_test > rmse_train and (rmse_test - rmse_train) > 0.1 * rmse_train:
        st.write(f"**Warning**: Potential overfitting. Test RMSE is significantly higher than Train RMSE.")
    elif rmse_train > rmse_test:
        st.write(f"**Warning**: Potential underfitting. Train RMSE is high.")
    else:
        st.write(f"Das Modell scheint gut ausbalanciert zu sein.")

    # Prognosen für Zukunft erstellen
    X_test_future = merge_test.drop(['Date', 'Year', 'MarkDown1', 'MarkDown2', 'MarkDown4', 'MarkDown3', 'MarkDown5', 'CPI', 'Unemployment', 'Temperature', 'Fuel_Price'], axis=1)

    predictions = model.predict(X_test_future)
    y_test_future = pd.DataFrame({'Weekly_Sales': predictions})

    return past_dates, future_dates, y_test_future, merge_train

    



