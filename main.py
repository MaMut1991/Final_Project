# Start with: streamlit run main.py

import streamlit as st

from dashboard import create_diagram
from model import visualizing_forecasts, evaluate_model, sales_forecast

st.set_page_config(layout='wide')

# Titel
st.header('[Sales App] (Prototyp)')
col1 = st.columns(1)



# st.session_state oder st.cache?



# Sidebar

# Analyse
options_x = ['CPI', 'Date', 'Dept', 'Fuel_Price', 'IsHoliday', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5', 'Size', 'Store', 'Temperature', 'Type', 'Unemployment', 'Weekly_Sales']

options_y1 = option_x = ['CPI', 'Date', 'Dept', 'Fuel_Price', 'IsHoliday', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5', 'Size', 'Store', 'Temperature', 'Type', 'Unemployment', 'Weekly_Sales']

st.sidebar.markdown('## Analyse:' )
st.selectbox('Was soll auf die x-Achse?',options = options_x, placeholder='x-Achse')
st.selectbox('Was soll auf die y-Achse?', options=options_y1, placeholder='y-Achse')




# Prognose
st.sidebar.markdown('## Prognose:')




# Display: Spalte um Diagramme zu visualisieren

with col1:

    st.subheader('Ihre gewünschten Analyseergebnisse:')









