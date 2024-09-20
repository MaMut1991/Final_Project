# Importe
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
from xgboost import XGBRegressor

from preprocessing import data_preprocessing



# Vordefinierte Farbpaletten
color_palette_1 = ['#763DFF']    # 1 Farbe für Diagramm
color_palette_2 = ['#763DFF', '#FF3D65']    # 2 Farben für Diagramm
color_palette_3 = ['#763DFF', '#FF3D65', '#C6FF3D']    # 3 Farben für Diagramm
color_palette_4 = ['#763DFF', '#FF3D65', '#C6FF3D', '#3DFFD7']    # 4 Farben für Diagramm

# Vordefinierte Schriftgrößen für Achsen und titel
fontsize_title = 20
fontsize_axes =15



'''
def get_tuned_model_random_forest():

    # Import merge_train
    merge_train, merge_test = data_preprocessing()

    # Splitte Trainingsdaten (train.csv) in train und test 
    X = merge_train.drop(['Date','Year', 'Month', 'Week', 'Weekly_Sales'], axis=1) # Alle Originalfeatures (ohne Weekly_Sales = Target und ohne Zeitkomponenten) 
    y = merge_train['Weekly_Sales']     # Nur Weekly_Sales (Target) 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)     

    model = RandomForestRegressor(n_estimators=70, min_samples_split=3, min_samples_leaf=1, max_depth=30, max_features=3)
    model.fit(X_train,y_train)
    # model.scores = cross_val_score(model,X_train, y_train, cv=10)
    #np.mean(model_scores)

    
    # Hyperparameter für GridSearch festlegen
    param_grid = {
        'n_estimators': [50, 100, 150, 200],
        'max_depth': [5, 10, 15, 20, 25],
        'min_samples_split': [2, 5],
        'max_features': ['sqrt', 'log2', 'auto', None],
        'max_leaf_nodes':[3,6,9]
    }
    

    param_grid = {
        'n_estimators': 100,
    }
    
    # RandomForest mit GridSearchCV
    model = RandomForestRegressor()
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=2, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    # Bestes Modell finden
    tuned_model = grid_search.best_estimator_

    # Modell in pkl-Datei speichern
    joblib.dump(tuned_model, 'random_forest_model.pkl')
    '''
    


def visualizing_forecasts(y_test_future):
    # merge_train aus preprocessing.py importieren
    merge_train, merge_test = data_preprocessing()

    # 'Date' aus merge_test in Variable abspeichern
    future_dates = merge_test['Date']  # für spätere Visualisierung in visualizing_forecasts

    # Predictions mit 'Date' anreichern für Visualisierung im Diagramm
    y_test_future_with_date = y_test_future.copy()
    y_test_future_with_date['Date'] = future_dates

    # historische Werte für Diagramm beschaffen
    historical_values_for_diagram = merge_train[['Date', 'Weekly_Sales']]

    # Erstellung Liniendiagramm
    sns.set_style('darkgrid')
    fig1, ax1 = plt.subplots(figsize=(15, 6))

    # Historische Werte plotten
    historical_values_for_diagram.groupby('Date')['Weekly_Sales'].mean().plot(label='Historisch', ax=ax1)
    # Prognostizierte Werte plotten
    y_test_future_with_date.groupby('Date')['Weekly_Sales'].mean().plot(color='orange', label='Prognostiziert', ax=ax1)

    ax1.legend(loc='best', fontsize=12)  # Setze die Schriftgröße direkt
    ax1.set_ylabel('Sales', fontsize=12)  # Korrigierte Methode
    ax1.set_xlabel('Year', fontsize=12)    # Korrigierte Methode
    ax1.set_title('Historische vs. Prognostizierte Sales', fontsize=14)  # Korrigierte Methode

    st.pyplot(fig1)

    # Erstellung Tabellen
    st.markdown('Weekly Predictions:')
    table1 = y_test_future_with_date.set_index('Date')
    table1.index = pd.to_datetime(table1.index).strftime('%Y-%m-%d')
    daily = table1.groupby(table1.index)['Weekly_Sales'].mean().round()
    st.dataframe(daily.round(2))

    


# Bewertung der Modellleistung auf dem Trainings- und Testdatensatz
def evaluate_model(model, X_train, y_train, X_test, y_test):

    # Vorhersagen auf Trainings- und Testdaten (basierend auf train.csv)
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)  

    # Berechnung der Metriken auf Trainingsdaten (basierend auf train.csv)
    mse_train = mean_squared_error(y_train, y_train_pred)
    rmse_train = np.sqrt(mse_train)
    mae_train = mean_absolute_error(y_train, y_train_pred)
    r2_train = r2_score(y_train, y_train_pred)

    # Berechnung der Metriken auf Testdaten (basierend auf train.csv)
    mse_test = mean_squared_error(y_test, y_test_pred)  
    rmse_test = np.sqrt(mse_test)
    mae_test = mean_absolute_error(y_test, y_test_pred)  
    r2_test = r2_score(y_test, y_test_pred) 

    return mse_train, rmse_train, mae_train, r2_train, mse_test, rmse_test, mae_test, r2_test




def sales_forecast():

    # Import merge_train
    merge_train, merge_test = data_preprocessing()

    # Splitte Trainingsdaten (train.csv) in train und test 
    X = merge_train.drop(['Date','Year', 'Month', 'Weekly_Sales', 'Fuel_Price','Temperature','Type','MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown4','MarkDown5','CPI','IsHoliday', 'Unemployment'], axis=1) # Alle Originalfeatures (ohne Weekly_Sales = Target und ohne Zeitkomponenten) 
    y = merge_train['Weekly_Sales']     # Nur Weekly_Sales (Target) 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)     

    # Modell trainieren
    #model = RandomForestRegressor(n_estimators=70, min_samples_split=3, min_samples_leaf=1, max_depth=30, max_features=3)
    #model = RandomForestRegressor(n_estimators=100, max_depth=10,min_samples_split=4,min_samples_leaf=4, max_features=9, max_samples=160000, random_state=101)
    model=XGBRegressor(n_jobs=-1, random_state=42, n_estimators=1000, learning_rate=0.9, max_depth=15, subsample=0.9, colsample_bytree=0.7)
    model.fit(X_train,y_train)
    # model.scores = cross_val_score(model,X_train, y_train, cv=10)
    #np.mean(model_scores)
    

    # Überprüfung auf Overfitting und Underfitting
    mse_train, rmse_train, mae_train, r2_train, mse_test, rmse_test, mae_test, r2_test = evaluate_model(model, X_train, y_train, X_test, y_test)

    
    # Prognosen für Zukunft erstellen (basierend auf train.csv)

    # Einführung zusätzlicher Testdatensatz aus merge_test für Schätzung und Visualisierung der Prognosen
    X_test_future = merge_test.drop(['Date','Year', 'Month', 'Fuel_Price','Temperature','Type','MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown4','MarkDown5','CPI','IsHoliday', 'Unemployment'], axis=1)     # Features aus Testdatensatz (test.csv)

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