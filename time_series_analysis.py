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
    # Daten beschaffen aus preprocessing.py
    merge_train, merge_test = data_preprocessing()

    # 2. EDA - Zeitabhängige Features plotten
    st.subheader("Untersuchung zeitabhängige Features")
    fig, ax = plt.subplots(figsize=(20, 15))
    merge_train[['Date', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']].plot(x='Date', subplots=True, ax=ax, title='Zeitabhängige Features')
    st.pyplot(fig)

    # Modellierung der Zeitreihe

    # Store 4
    store4 = merge_train[merge_train.Store == 4]
    sales4 = pd.DataFrame(store4.Weekly_Sales.groupby(store4.index).sum())

    # Store 6
    store6 = merge_train[merge_train.Store == 6]
    sales6 = pd.DataFrame(store6.Weekly_Sales.groupby(store6.index).sum())

    # Zeitreihen-Zerlegung
    decomposition = seasonal_decompose(sales4.Weekly_Sales, period=12)
    st.subheader("Zeitreihen-Zerlegung für Store 4")
    fig, ax = plt.subplots(figsize=(12, 10))
    decomposition.plot(ax=ax)
    st.pyplot(fig)

    # Plot Store 4 vs Store 6
    st.subheader("Vergleich: Store 4 vs Store 6 Weekly Sales")
    fig, ax = plt.subplots(figsize=(15, 6))
    sales4.Weekly_Sales.plot(ax=ax, legend=True, color='turquoise', label="Store 4")
    sales6.Weekly_Sales.plot(ax=ax, legend=True, color='salmon', label="Store 6")
    ax.set_ylabel('Weekly Sales')
    ax.set_title('Store 4 vs Store 6 Weekly Sales')
    st.pyplot(fig)

    # SARIMAX Modell
    st.subheader("SARIMAX-Modell und Vorhersage für Store 4")

    y1 = sales4.Weekly_Sales

    mod = sm.tsa.statespace.SARIMAX(y1,
                                    order=(4, 4, 3),
                                    seasonal_order=(1, 1, 0, 52),
                                    enforce_invertibility=False)
    results = mod.fit()

    # Vorhersage für die letzten 90 Tage
    pred = results.get_prediction(start=pd.to_datetime('2012-07-27'), dynamic=False)
    pred_ci = pred.conf_int()

    fig, ax = plt.subplots(figsize=(12, 8))
    y1['2010':].plot(ax=ax, label='Beobachtet')
    pred.predicted_mean.plot(ax=ax, label='Vorhersage der letzten 90 Tage', alpha=0.7)
    ax.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='k', alpha=0.2)
    ax.set_xlabel('Jahre')
    ax.set_ylabel('Weekly Sales')
    plt.legend()
    st.pyplot(fig)

    # Vorhersage für die nächsten 12 Wochen
    st.subheader("12 Wochen Vorhersage für Store 4")
    pred_uc = results.get_forecast(steps=12)
    pred_ci = pred_uc.conf_int()

    fig, ax = plt.subplots(figsize=(12, 8))
    y1.plot(ax=ax, label='Beobachtet')
    pred_uc.predicted_mean.plot(ax=ax, label='Vorhersage')
    ax.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='k', alpha=0.25)
    ax.set_xlabel('Zeitraum')
    ax.set_ylabel('Sales')
    plt.legend()
    st.pyplot(fig)

# Streamlit aufrufen
st.title("Zeitreihenanalyse")
get_time_series()
