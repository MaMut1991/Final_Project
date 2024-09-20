# Start with: streamlit run main.py

import streamlit as st

from dashboard import create_diagram, show_corr, get_dashboard, get_store_department_sales_heatmap, get_type_department_sales_heatmap
from random_forest import visualizing_forecasts, sales_forecast
from time_series_analysis_2 import get_time_series
from random_forest import sales_forecast
from sarimax import sales_forecast_sx

st.set_page_config(layout='wide')


# Titel
st.header('SalesEcho © (Prototyp)')
col1 = st.columns(1)



# st.session_state oder st.cache?



# Sidebar

# Analyse

st.sidebar.markdown('# Analysen:', help='In diesem Abschnitt können historische Daten durch Visualisierungen analysiert werden.' )

st.sidebar.markdown('#### Vorgefertigte Analysen:')

# Buttons für Korrelationen
corr = st.sidebar.button('Einflüsse auf Weekly Sales', help='Erzeugt Diagramme, welche die Korrelationen zwischen den Features aufzeigen.')

if corr:
    show_corr()


#Buttons für Time Series Analysis
tsa = st.sidebar.button('Zeitreihenanalyse', help='Erzeugt Diagramme, welche zeitabhängige Features analysieren')
if tsa:
    get_time_series()


# Button für Dashboard
db = st.sidebar.button('Sales Dashboard', help='Visualisiert ein Sales Dashboard, um wichtige Einblicke in den Datensatz zu bekommen')

if db:
    get_dashboard()


# Button für Store-Department-Sales-Heatmap
heat_store = st.sidebar.button('Sales Heatmap by Store and Dept.', help='Erzeugt Heatmap, in der die Stores den Departments gegenübergestellt werden. Die Values entsprechen den Weekly_Sales.')
if heat_store:
    get_store_department_sales_heatmap()  


# Button für Type-Department-Sales-Heatmap
heat_type = st.sidebar.button('Sales Heatmap by Type and Dept.', help='Erzeugt Heatmap, in der die Store-Types den Departments gegenübergestellt werden. Die Values entsprechen den Weekly_Sales.')
if heat_type:
    get_type_department_sales_heatmap()



st.sidebar.markdown('---') # Räumliche Trennung 




st.sidebar.markdown('#### Erstellung eigener Diagramme:')

# Listen für Dropdown-Menü in Sidebar für Parameterauswahl
options_x = [None, 'Date', 'Dept', 'Store']

options_y1 = option_x = [None, 'CPI', 'Date', 'Dept', 'Fuel_Price', 'IsHoliday', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5', 'Size', 'Store', 'Temperature', 'Type', 'Unemployment', 'Weekly_Sales']

options_y2 = option_x = [None,'CPI', 'Date', 'Dept', 'Fuel_Price', 'IsHoliday', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5', 'Size', 'Store', 'Temperature', 'Type', 'Unemployment', 'Weekly_Sales']

# SelectBox für Parameter für Diagrammachsen
x_achse = st.sidebar.selectbox('Was soll auf die x-Achse?',options = options_x, placeholder='x-Achse')
y1_achse = st.sidebar.selectbox('Was soll auf die y-Achse?', options=options_y1, placeholder='y-Achse')

# Checkbox-Abfrage für zweite y-Achse
checkbox_y2_achse = st.sidebar.checkbox('Möchten Sie eine zweite y-Achse einfügen?')

if checkbox_y2_achse:
    y2_achse = st.sidebar.selectbox('Was soll auf die zweite y-Achse?', options=options_y2, disabled=checkbox_y2_achse == False)
else:
    y2_achse = None

# Operation wählen
option_operation = ['Mittelwert', 'Summe']

operation = st.sidebar.selectbox('Darstellung als Summe oder Mittelwert?:',options=option_operation, placeholder='Rechenoperation', help='Entscheiden Sie, ob die Diagramme den Mittelwert oder die Summe der gewünschten Daten anzeigen sollen.')

# Buttons für Analyseteil
show_me = st.sidebar.button('Erstelle Diagramme', help='Erzeugt Diagramme auf Basis der ausgewählten Parameter.')

# Erzeuge Diagramme -> Ausführen create_diagram
if show_me:
    create_diagram(y1 = y1_achse, y2=y2_achse, x=x_achse, operation=operation)




st.sidebar.markdown('---') # Räumliche Trennung 




# Prognose


st.sidebar.markdown('# Prognose:', help='In diesem Abschnitt werden Weekly Sales mithilfe von Machine Learning vorausgesagt.' )

# Random Forest
pred_rf = st.sidebar.button('Random Forest Prognose', help='Hier werden die Weekly_Sales mithilfe des Random Forest-Modells geschätzt.')
if pred_rf:
    sales_forecast()

# Sarimax
pred_sx = st.sidebar.button('SARIMAX Prognose', help='Hier werden die Weekly_Sales mithilfe des SARIMAX-Modells geschätzt.')
if pred_sx:
    sales_forecast_sx() 


    















