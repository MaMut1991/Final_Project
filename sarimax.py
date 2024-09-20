# Importe
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
from preprocessing import data_preprocessing


# Vordefinierte Farbpaletten
color_palette_1 = ['#763DFF']    # 1 Farbe für Diagramm
color_palette_2 = ['#763DFF', '#FF3D65']    # 2 Farben für Diagramm
color_palette_3 = ['#763DFF', '#FF3D65', '#C6FF3D']    # 3 Farben für Diagramm
color_palette_4 = ['#763DFF', '#FF3D65', '#C6FF3D', '#3DFFD7']    # 4 Farben für Diagramm

# Vordefinierte Schriftgrößen für Achsen und Titel
fontsize_title = 20
fontsize_axes = 15


def evaluate_model_sx(model, exog_train, exog_test, y_train, y_test):
    # Vorhersagen auf Trainings- und Testdaten
    y_train_pred = model.predict(start=0, end=len(y_train)-1, exog=exog_train)
    y_test_pred = model.predict(start=len(y_train), end=len(y_train)+len(y_test)-1, exog=exog_test)

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


def sales_forecast_sx():

    # Importiere die Daten
    merge_train, merge_test = data_preprocessing()

    # Annahme: Diese Features sind relevante exogene Variablen
    exog_features = merge_train[['Fuel_Price', 'CPI', 'Unemployment', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']]

    # Setze 'Date' als Index, falls noch nicht geschehen
    merge_train.set_index('Date', inplace=True)
    merge_test.set_index('Date', inplace=True)

    # Splitte die Daten in Trainings- und Testset
    y_train = merge_train['Weekly_Sales']
    y_test = merge_test['Weekly_Sales']

    exog_train = exog_features.loc[merge_train.index]
    exog_test = exog_features.loc[merge_test.index]

    # SARIMAX-Modell mit exogenen Variablen
    mod = sm.tsa.statespace.SARIMAX(y_train,
                                    exog=exog_train,
                                    order=(1, 1, 1),
                                    seasonal_order=(1, 1, 1, 52),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)

    # Modell fitten
    results = mod.fit()

    # Vorhersage für die Testdaten (letzte 90 Tage)
    pred = results.get_prediction(start=pd.to_datetime('2012-07-27'), exog=exog_test, dynamic=False)
    pred_ci = pred.conf_int()

    # Plot der echten Werte und der Vorhersagen
    ax = y_train['2010':].plot(label='Observed', figsize=(15, 6))
    pred.predicted_mean.plot(ax=ax, label='Forecast', alpha=0.7)

    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)

    ax.set_xlabel('Years')
    ax.set_ylabel('Weekly Sales')
    plt.legend()
    plt.show()


    # Tabelle mit den vorhergesagten Werten für Weekly_Sales anzeigen
    forecast_values = pred.predicted_mean

    # Erstelle einen DataFrame mit dem Datum aus merge_test und den Vorhersagen
    forecast_df = pd.DataFrame({
        'Date': merge_test.index[:len(forecast_values)],
        'Forecasted Weekly Sales': forecast_values.values
    })

    st.write("\nForecasted Weekly Sales:")
    st.dataframe(forecast_df)




    # Modell evaluieren
    mse_train, rmse_train, mae_train, r2_train, mse_test, rmse_test, mae_test, r2_test = evaluate_model_sx(results, exog_train, exog_test, y_train, y_test)

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

