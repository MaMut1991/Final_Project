# Importe
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
import itertools

from preprocessing import data_preprocessing



# Vordefinierte Farbpaletten
color_palette_1 = ['#763DFF']    # 1 Farbe für Diagramm
color_palette_2 = ['#763DFF', '#FF3D65']    # 2 Farben für Diagramm
color_palette_3 = ['#763DFF', '#FF3D65', '#C6FF3D']    # 3 Farben für Diagramm
color_palette_4 = ['#763DFF', '#FF3D65', '#C6FF3D', '#3DFFD7']    # 4 Farben für Diagramm

# Vordefinierte Schriftgrößen für Achsen und titel
fontsize_title = 20
fontsize_axes =15


#def visualizing_forecasts():

#def evaluate_model():


def sales_forecast_sx():

    # Import merge_train
    merge_train, merge_test = data_preprocessing()


    # 5. Modellierung
    # Wähle ein Modell: Überlege, welche Modelle für deine Daten geeignet sind:
    

    # Annahme: Diese Features sind relevante exogene Variablen
    exog_features = merge_train[['Fuel_Price', 'CPI', 'Unemployment', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']]

    # SARIMAX-Modell mit exogenen Variablen (order und seasonal_order müssen auf Basis der Zeitreihe gewählt werden)
    p, d, q = 1, 1, 1  # ARIMA-Parameter
    P, D, Q, m = 1, 1, 1, 52  # Saisonale Parameter (z.B. für wöchentliche Daten)

    # Erstelle das SARIMAX-Modell

    '''
    # Define the p, d and q parameters to take any value between 0 and 2
    p = d = q = range(0, 5)

    # Generate all different combinations of p, d and q triplets
    pdq = list(itertools.product(p, d, q))

    # Generate all different combinations of seasonal p, d and q triplets
    seasonal_pdq = [(x[0], x[1], x[2], 52) for x in list(itertools.product(p, d, q))]
    '''

    mod = sm.tsa.statespace.SARIMAX(merge_train['Weekly_Sales'],
                                    exog=exog_features,
                                    order=(1, 1, 1),
                                    seasonal_order=(1, 1, 1, 52),   #enforce_stationarity=False,
                                    enforce_invertibility=False)

    results = mod.fit()

    # predict for last 90 days
    pred = results.get_prediction(start=pd.to_datetime('2012-07-27'), dynamic=False)
    pred_ci = pred.conf_int()

    ax = merge_train.index['2010':].plot(label='observed')
    pred.predicted_mean.plot(ax=ax, label='Forecast last 90 days', alpha=.7)

    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)

    ax.set_xlabel('Years')
    ax.set_ylabel('Weekly Sales')
    plt.legend()

    plt.show()



    # 6. Modellbewertung
    # Trainings- und Testdaten: Teile die Daten in Trainings- und Testsets auf.
    # Metriken: Verwende Metriken wie RMSE, MAE oder MAPE zur Bewertung der Vorhersagegenauigkeit.



    #7. Vorhersage
    #Zukunftsprognose: Verwende das ausgewählte Modell, um Vorhersagen für die nächsten Tage zu erstellen.
    #Visualisierung der Vorhersagen: Vergleiche die Vorhersagen mit den tatsächlichen Werten, um die Modellleistung zu bewerten.



    #8. Dokumentation und Reporting
    #Bericht: Dokumentiere alle Schritte und Ergebnisse, um eine klare Vorstellung von der Analyse und den Vorhersagen zu vermitteln.
    #Diagramme, die nützlich sein könnten:
    #Zeitreihendiagramm der Weekly_Sales
    #Histogramm der nicht zeitabhängigen Variablen
    #Autokorrelations- und Partielle Autokorrelationsdiagramme
    #Residuenanalyse (z.B. Scatterplots der Residuen)
    #Vorhersageplots