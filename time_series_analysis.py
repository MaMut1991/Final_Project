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

def get_time_series():
    store4 = 0
    store6 = 0
    sales4 = 0
    sales6 = 0

    fontsize_title = 20
    fontsize_axes =15

    # Daten beschaffen aus preprocessing.py
    merge_train, merge_test = data_preprocessing()

    # 2. EDA - Zeitabhängige Features plotten
    fig, ax = plt.subplots(figsize=(15, 8))
    merge_train[['Date', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment']].plot(x='Date', subplots=True, ax=ax, title = 'Zeitabhägige Features')
    ax.set_title('Zeitabhägige Features', fontsize=fontsize_title)
    st.pyplot(fig)



    # Zeitreihenzerlegung für alle Stores

    # Stores
    stores = merge_train 
    stores.set_index('Date',inplace=True) # Setze Date als Index
    # Nach Date gruppieren und Weekly_Sales aufsummieren
    sales = pd.DataFrame(stores.groupby(stores.index)['Weekly_Sales'].sum())
 
    # Zeitreihen-Zerlegung
    decomposition = seasonal_decompose(sales.Weekly_Sales, period=12)
    fig = decomposition.plot()  # plot ohne 'ax'
    fig.set_size_inches(15, 6)  # Größe anpassen
    st.pyplot(fig)


    
    




