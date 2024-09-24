# Importe
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor

from preprocessing import data_preprocessing

# Vordefinierte Farbpaletten
color_palette_1 = ['#FF6C3E']    # 1 Farbe für Diagramm
color_palette_2 = ['#FF6C3E','#3ED1FF']    # 2 Farben für Diagramm
color_palette_3 = ['#FF6C3E','#3ED1FF','#70FF3E']    # 3 Farben für Diagramm
color_palette_4 = ['#FF6C3E','#3ED1FF','#70FF3E','#CD3EFF']    # 4 Farben für Diagramm

# Vordefinierte Schriftgrößen für Achsen und Titel
fontsize_title = 20
fontsize_axes = 15

def visualizing_forecasts(y_test_future):
    # merge_train aus preprocessing.py importieren
    merge_train, merge_test = data_preprocessing()

    # 'Date' aus merge_test in Variable abspeichern
    future_dates = merge_test['Date']  # für spätere Visualisierung in visualizing_forecasts

    # Predictions mit 'Date', 'Store', und 'Dept' anreichern für Visualisierung und Tabelle
    y_test_future_with_date = y_test_future.copy()
    y_test_future_with_date['Date'] = future_dates
    y_test_future_with_date['Store'] = merge_test['Store']  # Store hinzufügen
    y_test_future_with_date['Dept'] = merge_test['Dept']    # Dept hinzufügen
    y_test_future_with_date['Year'] = pd.to_datetime(future_dates).dt.year  # Jahr extrahieren
    y_test_future_with_date['Month'] = pd.to_datetime(future_dates).dt.month  # Monat extrahieren

    # Historische Werte für Diagramm beschaffen
    historical_values_for_diagram = merge_train[['Date', 'Weekly_Sales']]

    # Erstellung Liniendiagramm
    sns.set_style('darkgrid')
    fig1, ax1 = plt.subplots(figsize=(15, 6))

    # Historische Werte plotten
    historical_values_for_diagram.groupby('Date')['Weekly_Sales'].mean().plot(label='Historisch', ax=ax1)
    
    # Prognostizierte Werte plotten
    y_test_future_with_date.groupby('Date')['Weekly_Sales'].mean().plot(color='orange', label='Prognostiziert', ax=ax1)

    ax1.legend(loc='best', fontsize=12)
    ax1.set_ylabel('Sales', fontsize=12)
    ax1.set_xlabel('')
    ax1.set_title('Historische vs. Prognostizierte Sales', fontsize=14)

    st.pyplot(fig1)

    # Erstellung Tabellen
    st.markdown('Sales Forecasts:')

    # Erstelle Tabelle und gruppiere nach Date, Store, Dept
    table1 = y_test_future_with_date[['Date', 'Store', 'Dept', 'Weekly_Sales']]
    table1['Date'] = pd.to_datetime(table1['Date']).dt.strftime('%Y-%m-%d')

    # Zeige die Tabelle an, gruppiert nach Date, Store, Dept
    daily_forecasts = table1.groupby(['Date', 'Store', 'Dept'])['Weekly_Sales'].mean().round(2)
    
    st.dataframe(daily_forecasts)

# Bewertung der Modellleistung auf dem Trainings- und Testdatensatz
def evaluate_model(model, X_train, y_train, X_test, y_test):

    # Vorhersagen auf Trainings- und Testdaten
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Berechnung der Metriken auf Trainingsdaten
    mse_train = mean_squared_error(y_train, y_train_pred)
    rmse_train = np.sqrt(mse_train)
    mae_train = mean_absolute_error(y_train, y_train_pred)
    r2_train = r2_score(y_train, y_train_pred)

    # Berechnung der Metriken auf Testdaten
    mse_test = mean_squared_error(y_test, y_test_pred)
    rmse_test = np.sqrt(mse_test)
    mae_test = mean_absolute_error(y_test, y_test_pred)
    r2_test = r2_score(y_test, y_test_pred)

    return mse_train, rmse_train, mae_train, r2_train, mse_test, rmse_test, mae_test, r2_test

def sales_forecast():

    # Import merge_train und merge_test
    merge_train, merge_test = data_preprocessing()

    # Splitte Trainingsdaten (train.csv) in train und test
    X = merge_train.drop(['Date','Year', 'Month', 'Weekly_Sales', 'Fuel_Price','Temperature','Type','MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5','CPI','IsHoliday', 'Unemployment', 'Super_Bowl', 'Labor_Day', 'Thanksgiving', 'Christmas','Easter'], axis=1)
    y = merge_train['Weekly_Sales']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

    # Modell trainieren
    model = XGBRegressor(n_jobs=-1, random_state=42, n_estimators=1000, learning_rate=0.9, max_depth=15, subsample=0.9, colsample_bytree=0.7)
    model.fit(X_train, y_train)

    # Überprüfung auf Overfitting und Underfitting
    mse_train, rmse_train, mae_train, r2_train, mse_test, rmse_test, mae_test, r2_test = evaluate_model(model, X_train, y_train, X_test, y_test)

    # Testdatensatz für Schätzung und Visualisierung der Prognosen
    X_test_future = merge_test.drop(['Date','Year', 'Month', 'Fuel_Price','Temperature','Type','MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5','CPI','IsHoliday', 'Unemployment'], axis=1)

    # Prognosen generieren
    predictions = model.predict(X_test_future)
    y_test_future = pd.DataFrame({'Weekly_Sales': predictions})

    # Historische Daten und Forecasts visualisieren
    visualizing_forecasts(y_test_future)

    # Modellperformance bewerten
    st.write(f'\nEvaluation Results:')
    st.write(f'Training MSE: {mse_train:.4f}, RMSE: {rmse_train:.4f}, MAE: {mae_train:.4f}, R²: {r2_train:.4f}')
    st.write(f'Test MSE: {mse_test:.4f}, RMSE: {rmse_test:.4f}, MAE: {mae_test:.4f}, R²: {r2_test:.4f}')

    if rmse_test > rmse_train and (rmse_test - rmse_train) > 0.1 * rmse_train:
        st.write(f'\nWarning: Potential overfitting. Test RMSE is significantly higher than Train RMSE.')
    elif rmse_train > rmse_test:
        st.write(f'\nWarning: Potential underfitting. Train RMSE is higher than Test RMSE.')
    else:
        st.write(f'\nThe model seems to be well-balanced.')
