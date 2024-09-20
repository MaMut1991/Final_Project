# Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from preprocessing import data_preprocessing # eigene Funktion aus anderer Datei

from statsmodels.tsa.seasonal import seasonal_decompose
import itertools
import statsmodels.api as sm  # für SARIMAX
import streamlit as st
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.stattools import adfuller


# Datenvorbereitung

@st.cache_data
def get_time_series():
    store4 = 0
    store6 = 0
    sales4 = 0
    sales6 = 0

    # Vordefinierte Farbpaletten 
    color_palette_1 = ['#763DFF']    # 1 Farbe für Diagramm
    color_palette_2 = ['#763DFF', '#FF3D65']    # 2 Farben für Diagramm
    color_palette_3 = ['#763DFF', '#FF3D65', '#C6FF3D']    # 3 Farben für Diagramm
    color_palette_4 = ['#763DFF', '#FF3D65', '#C6FF3D', '#3DFFD7']    # 4 Farben für Diagramm
    
    # Vordefinierte Schriftgrößen für Achsen und Titel
    fontsize_title = 20
    fontsize_axes =15

    # Daten beschaffen aus preprocessing.py
    merge_train, merge_test = data_preprocessing()   
    
    # Date ist ein datetime-Objekt in merge_train
    # merge_train hat keine Null-Werte
    # merge_train hat keine NaN-Werte
    



    # 2. Explorative Datenanalyse (EDA)
    # Visualisierung: Erstelle Zeitreihendiagramme der Target-Variable, um Trends, Saisonalitäten und Zyklen zu identifizieren.
    # Korrelation: Untersuche die Korrelation zwischen den Zeitvariablen und der Target-Variable. Verwende Heatmaps oder Scatterplots.
    # Histogramme: Erstelle Histogramme der nicht zeitabhängigen Variablen.
    
    # Weekly_Sales over Time (AVG) (Liniendiagramm)
    weekly_sales_mean = merge_train[['Date', 'Weekly_Sales']].copy()
    weekly_sales_mean['Date'] = pd.to_datetime(weekly_sales_mean['Date'])  # Sicherstellen, dass das Datum im richtigen Format ist
    weekly_sales_mean.set_index('Date', inplace=True)
    weekly_sales_mean = weekly_sales_mean.resample('W').mean()  # Wöchentliche Mittelwerte berechnen

    fig1,ax1 = plt.subplots(figsize=(15,6))   
    sns.lineplot(x=weekly_sales_mean.index, y='Weekly_Sales', data=weekly_sales_mean, palette=color_palette_1, ax=ax1)
    ax1.set_title('Weekly Sales Over Time (AVG)', fontsize=fontsize_title)
    ax1.set_xlabel('Year', fontsize = fontsize_axes)
    ax1.set_ylabel('Sales', fontsize = fontsize_axes)
    ax1.grid(True, linestyle='-')
    st.pyplot(fig1)


    # Erstelle Korrelationsanalyse (Barplot)
    fig2, ax1 = plt.subplots(figsize=(15,6))
    merge_train.corr()['Weekly_Sales'].abs().sort_values()[:-1].plot(kind='bar', ax=ax1, color=color_palette_1)
    ax1.set_title('Korrelationsanalyse:', fontsize=fontsize_title)
    ax1.set_xlabel('Features', fontsize=fontsize_axes)
    ax1.set_ylabel('Correlation Coefficients', fontsize=fontsize_axes)
    st.pyplot(fig2)
    

    # Zeitlich abhängige Variablen plotten
    fig3, ax1 = plt.subplots(figsize=(40,20))
    merge_train[['Date', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']].plot(x='Date', subplots=True, ax=ax1, color=color_palette_4, title = 'Zeitabhägige Features')
    st.pyplot(fig3)


    # Zeitreihenzerlegung Weekly_Sales über alle Stores
    stores = merge_train 
    stores.set_index('Date',inplace=True) # Setze Date als Index
    # Nach Date gruppieren und Weekly_Sales aufsummieren
    sales = pd.DataFrame(stores.groupby(stores.index)['Weekly_Sales'].sum())
    decomposition = seasonal_decompose(sales.Weekly_Sales, period=12)
    fig4 = decomposition.plot()  # plot ohne 'ax'
    fig4.set_size_inches(15, 6)  # Größe anpassen
    st.pyplot(fig4)
    


    # 3. Zeitreihenanalysen
    
    @st.cache_resource
    def autocorr():
        # Autokorrelationsplot erstellen - Test auf Saisonalität
        plt.rcParams.update({'figure.figsize': (15, 6), 'figure.dpi': 120})
        # Autokorrelationsplot
        fig5 = plt.figure()  # Ein leeres Figure-Objekt erstellen
        autocorrelation_plot(merge_train['Weekly_Sales'].tolist())
        plt.title("Autokorrelationsplot - Test auf Saisonalität der Weekly_Sales", fontsize=20)  # Titel setzen
        st.pyplot(fig5)

    autocorr()

    @st.cache_resource
    def adf():
        # ADF-Test durchführen (Test auf Stationarität)
        result = adfuller(merge_train['Weekly_Sales'])
        st.write('Augmented Dickey Fuller (ADF) Statistic:', result[0])
        st.write('p-value:', result[1])
        st.write('(Bei p < 0.05 liegt eine Stationarität vor.)')

    adf()



    # 4. Datenvorverarbeitung
    # Transformieren: Wenn die Zeitreihe nicht stationär ist, wende Transformationen an:
    # Differenzierung: Differenziere die Zeitreihe, um Trends zu entfernen.
    # Logarithmische Transformation: Wenn die Varianz mit der Zeit zunimmt.
    # Glättung: Verwende gleitende Durchschnitte zur Glättung von Daten.

    # Transformieren: Wenn die Zeitreihe nicht stationär ist, wende Transformationen an:   -> Prüfen!
    # Differenzierung, um Trends zu entfernen
    merge_train['diff_sales'] = merge_train['Weekly_Sales'].diff().dropna()

    # Logarithmische Transformation, wenn Varianz mit der Zeit zunimmt
    merge_train['log_sales'] = np.log(merge_train['Weekly_Sales'])


    