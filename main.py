# Start with: streamlit run main.py

import streamlit as st

from dashboard import create_diagram, show_corr, get_dashboard, get_store_department_sales_heatmap, get_type_department_sales_heatmap, get_holiday
from preprocessing import data_preprocessing
from XGBoost import sales_forecast
from time_series_analysis_2 import get_time_series
from XGBoost import sales_forecast


st.set_page_config(layout='wide')


# Titel
st.header('SalesWizard (Prototyp)')
col1 = st.columns(1)

# Sidebar

# Analyse

st.sidebar.markdown('# Analyses:', help='In this section, historical data can be analyzed through visualizations.' )

st.sidebar.markdown('#### Pre-built Analyses:')

# Buttons für Korrelationen
corr = st.sidebar.button('Correlation', help='Generates charts that illustrate the correlations between the features.')

if corr:
    show_corr()

# Feiertagsanalyse
holiday = st.sidebar.button('Holiday & MarkDown', help='Displays charts to analyze the holidays in more detail.')
if holiday:
    get_holiday()

#Buttons für Time Series Analysis
tsa = st.sidebar.button('Time Series', help='Generates charts that analyze time-dependent features.')
if tsa:
    get_time_series()

# Button für Dashboard
db = st.sidebar.button('Sales Dashboard', help='Visualizes a sales dashboard to gain key insights into the dataset.')

if db:
    get_dashboard()

# Button für Store-Department-Sales-Heatmap
heat_store = st.sidebar.button('Sales Heatmap by Store and Dept.', help='Generates a heatmap that compares stores against departments. The values correspond to Weekly Sales.')
if heat_store:
    get_store_department_sales_heatmap()  

# Button für Type-Department-Sales-Heatmap
heat_type = st.sidebar.button('Sales Heatmap by Type and Dept.', help='Generates a heatmap that compares store types against departments. The values correspond to Weekly Sales.')
if heat_type:
    get_type_department_sales_heatmap()

st.sidebar.markdown('---') # Räumliche Trennung 

st.sidebar.markdown('#### Creation of Custom Charts:')

# Listen für Dropdown-Menü in Sidebar für Parameterauswahl
options_x = [None, 'Date', 'Dept', 'Store']

options_y1 = option_x = [None, 'CPI', 'Dept', 'Fuel_Price', 'IsHoliday', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5', 'Size', 'Store', 'Temperature', 'Type', 'Unemployment', 'Weekly_Sales']

options_y2 = option_x = [None,'CPI', 'Dept', 'Fuel_Price', 'IsHoliday', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5', 'Size', 'Store', 'Temperature', 'Type', 'Unemployment', 'Weekly_Sales']

# SelectBox für Parameter für Diagrammachsen
x_achse = st.sidebar.selectbox('What should go on the x-axis?',options = options_x, placeholder='x-Achse')
y1_achse = st.sidebar.selectbox('What should go on the y-axis?', options=options_y1, placeholder='y-Achse')

# Checkbox-Abfrage für zweite y-Achse
checkbox_y2_achse = st.sidebar.checkbox('Would you like to add a 2nd y-axis?')

if checkbox_y2_achse:
    y2_achse = st.sidebar.selectbox('What should go on the 2nd y-axis?', options=options_y2, disabled=checkbox_y2_achse == False)
else:
    y2_achse = None

# Operation wählen
option_operation = ['Average', 'Sum']

operation = st.sidebar.selectbox('Display as sum or average?',options=option_operation, placeholder='Rechenoperation', help='Decide whether the charts should display the average or the sum of the desired data.')

# Buttons für Analyseteil
show_me = st.sidebar.button('Create Diagrams', help='Generates charts based on the selected parameters.')

# Erzeuge Diagramme -> Ausführen create_diagram
if show_me:
    create_diagram(y1 = y1_achse, y2=y2_achse, x=x_achse, operation=operation)

st.sidebar.markdown('---') # Räumliche Trennung 



# Prognose
st.sidebar.markdown('# Forecast:', help='In this section, Weekly Sales are predicted using a Machine Learning algorithm called XGBoost.' )

# XGBoost
pred_rf = st.sidebar.button('Start XGBoost', help='Here, the Weekly_Sales are estimated using the Random Forest model.')
if pred_rf:
    sales_forecast()

# Cache leeren
if st.sidebar.button('Clear Cache'):
    st.cache_data.clear()
    st.cache_resource.clear()
    