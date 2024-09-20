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