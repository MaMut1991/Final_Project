# Import Bibliotheken
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import itertools
import statsmodels.api as sm  # für SARIMAX
import streamlit as st
from preprocessing import data_preprocessing
from pandas.plotting import autocorrelation_plot


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

    st.markdown(' ')
    st.markdown('##### Zeitabhängige Features plotten')

    # 2. EDA - Zeitabhängige Features plotten
    fig, ax = plt.subplots(figsize=(15, 8))
    merge_train[['Date', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Weekly_Sales']].plot(x='Date', subplots=True, ax=ax, color=color_palette_4, title = 'Zeitabhägige Features')
    #ax.set_title('Zeitabhägige Features', fontsize=fontsize_title)
    st.pyplot(fig)

    st.markdown('##### Zeitreihenzerlegung für Weekly Sales')

    # Zeitreihenzerlegung für alle Stores

    # Stores
    stores = merge_train 
    stores.set_index('Date',inplace=True) # Setze Date als Index
    # Nach Date gruppieren und Weekly_Sales aufsummieren
    sales = pd.DataFrame(stores.groupby(stores.index)['Weekly_Sales'].sum())
 
    # Zeitreihen-Zerlegung - Weekly_Sales
    decomposition = seasonal_decompose(sales.Weekly_Sales, period=12)
    fig = decomposition.plot()  # plot ohne 'ax'
    fig.set_size_inches(15, 6)  # Größe anpassen
    st.pyplot(fig)


    # Test auf Saisonalität - Weekly_Sales
    

    # Daten laden (hier ein Beispiel)
    # merge_train = pd.read_csv('deine_daten.csv')

    st.title("Autokorrelationsplot der wöchentlichen Verkaufszahlen")

    # Autokorrelationsplot erstellen - Test auf Saisonalität
    plt.rcParams.update({'figure.figsize': (15, 6), 'figure.dpi': 120})
    autocorrelation_plot(merge_train['Weekly_Sales'].tolist())
    plt.title("Autokorrelationsplot")
    # Plot in Streamlit anzeigen
    st.pyplot(plt)


    
    




