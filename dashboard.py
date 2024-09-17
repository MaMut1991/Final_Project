# Funktion für Dashboard; Parameter werden per Auswahlmöglichkeiten in App übergeben
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessing import data_preprocessing
import streamlit as st
import matplotlib.ticker as mticker



def create_diagram(y1=None, y2=None, x=None, operation=None):
    '''
    Diese Funktion soll Parameter aus der Web-App entgegennehmen und gemäß der Eingabe entsprechende Diagramme zurückgeben.
    Dafür werden 4 Cases erstellt:

    Case1: Es werden die Weekly_Sales auf der y-Achse und die Zeit, die Stores oder die Departments auf der x-Achse in einem Diagramm (mit nur 1 y-Achse) dargestellt. Man hat die Ausahl die Daten als Mittelwert oder Summe darzustellen und darf den betrachteten Zeitraum auswählen.

    Case2: Es werden die Weekly_Sales auf der y-Achse und die Zeit, die Stores oder die Departments auf der x-Achse in einem Diagramm dargestellt. Im Gegensatz zu Case 1 kann hier eine zweite y-Achse für eine zweite Variable (frei wählbar) eingefügt werden. Man hat die Auswahl die Weekly_Sales als Mittelwert oder Summe darzustellen und darf den betrachteten Zeitraum auswählen.

    Case3: Es wird eine beliebige Variable, welche nicht die Weekly_Sales ist, in einem Diagramm mit einer y-Achse dargestellt. Auf der x-Achse werden ebenso nicht die Weekly_Sales berücksichtigt.

    Case4: Es werden 2 Variablen in einem Diagramm mit 2 y-Achsen dargestellt. Keine Variable beinhaltet die Weekly_Sales

    Parameter:

    y1: Variable Nr. 1, welche auf der linken y-Achse dargestellt wird
    y2: Variable Nr. 2, welche auf der rechten y-Achse dargestellt wird
    x: in der App ausgewählte Variable, welche auf der x-Achse dargestellt wird. Zur Auswahl stehen Store, Department und Zeit.
    operation: Daten als Mittelwert oder Summe auswerten und visualisieren
    '''

    merge_train, merge_test = data_preprocessing()



    def plot_bar(df, x, y, ax, title, xlabel, ylabel):
        """Zeichnet ein Balkendiagramm."""
        sns.barplot(x=x, y=y, data=df, palette='cool', ax=ax)
        ax.set_title(title, fontsize=15)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

    def plot_line(df, x, y, ax, title, xlabel, ylabel, hue=None):
        """Zeichnet ein Liniendiagramm."""
        sns.lineplot(x=x, y=y, hue=hue, data=df, palette='cool', ax=ax)
        ax.set_title(title, fontsize=15)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

    # Case1: 1 Achse: var1 ist weekly sales
    if y1 == 'Weekly_Sales' and y2 is None:

        # Temporärer DataFrame für die getätigte Auswahl in der App
        df_choice = pd.DataFrame({
            'x': merge_train[x],   # Variable für die x-Achse
            'y1': merge_train[y1], # Variable für die y1-Achse
        })

        # Case1.1: x != Date -> Balkendiagramm
        if x != 'Date':
            st.write("Case1.1")

            # Wähle die Aggregationsfunktion
            agg_func = df_choice.groupby('x').mean if operation == 'Mittelwert' else df_choice.groupby('x').sum
            agg_data = agg_func().reset_index()

            # Zeichne Balkendiagramm
            fig, ax = plt.subplots(figsize=(15,6))
            plot_bar(agg_data, 'x', 'y1', ax, 'Auswertung der gewünschten Parameter', x, y1)

            plt.tight_layout()
            st.pyplot(fig)

        # Case1.2: x == Date -> Zeitreihenanalyse per Liniendiagramm
        else:
            st.write("Case1.2")

            # Zeitreihe Plot 2 (Liniendiagramm)
            agg_func = df_choice.groupby('x').mean if operation == 'Mittelwert' else df_choice.groupby('x').sum
            agg_data = agg_func().reset_index()

            fig, ax = plt.subplots(figsize=(15,6))
            plot_line(agg_data, 'x', 'y1', ax, 'Zeitreihe 1: Weekly Sales', 'Date', 'Sales')

            plt.tight_layout()
            st.pyplot(fig)

            # Zeitreihe Plot 3 (Liniendiagramm nach Monaten mit 1 Linie pro Jahr)
            fig2, ax2 = plt.subplots(figsize=(15,6))

            # Data Frame mit Jahren, Wochen, Monaten und Weekly_Sales erstellen
            df_datetime = pd.DataFrame({
                'Date': merge_train['Date'],
                'Year': merge_train['Date'].dt.year, 
                'Month': merge_train['Date'].dt.month,
                'Week': merge_train['Date'].dt.isocalendar().week,
                'Weekly_Sales': merge_train['Weekly_Sales']
            })

            # Wähle die Aggregationsfunktion
            agg_func = df_datetime.groupby(['Year', 'Month']).mean if operation == 'Mittelwert' else df_datetime.groupby(['Year', 'Month']).sum
            datetime_aggregated = agg_func({'Weekly_Sales': 'mean' if operation == 'Mittelwert' else 'sum'}).reset_index()

            plot_line(datetime_aggregated, 'Month', 'Weekly_Sales', ax2, 'Auswertung der gewünschten Parameter', 'Month', 'Weekly_Sales', hue='Year')

            plt.tight_layout()
            st.pyplot(fig2)




            


    # Case2: 2 Achsen, var1 oder var2 sind weekly sales

    elif (y1 == 'Weekly_Sales' or y2 == 'Weekly_Sales') and y2 is not None:
        
        
        # Temporärer DataFrame für die getätigte Auswahl in der App
        df_choice = pd.DataFrame({
            'x': merge_train[x],   # Variable für die x-Achse
            'y1': merge_train[y1], # Variable für die y1-Achse
            'y2': merge_train[y2]  # Variable für die y2-Achse
        })

        if y1 == 'Weekly_Sales' and x == 'Date':   # Falls y1 gleich Weekly_Sales ist
            st.write('Case2.1')
            
            # Erstelle Figur und die erste Achse
            fig, ax1 = plt.subplots(figsize=(15,6))  

            # Zeichne Balkendiagramm (x und y1)
            sns.barplot(x='x', y='y1', data=df_choice, palette='cool', ax=ax1)
            ax1.set_title(f"Auswertung der gewünschten Parameter", fontsize=15)
            ax1.set_ylabel(y1)
            ax1.set_xlabel(x)
           

            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()

            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                agg_data = df_choice.groupby('x').mean().reset_index()
            else:
                agg_data = df_choice.groupby('x').sum().reset_index()
                

            # Visualisiere die aggregierten Verkaufsdaten in Liniendiagramm
            ax2.plot(ax1.get_xticks(),agg_data['y2'], color='red', marker='o')
            ax2.set_ylabel(y2)
          

            # Layout anpassen und anzeigen
            plt.tight_layout()
            st.pyplot(fig)




        elif y2 == 'Weekly_Sales' and x == 'Date':  # Falls y2 gleich Weekly_Sales ist
            st.write('Case2.2')

            # Erstelle Figur und die erste Achse
            fig, ax1 = plt.subplots(figsize=(15,6))

            # Zeichne Balkendiagramm (x und y1)
            sns.barplot(x='x', y='y1', data=df_choice, palette='cool', ax=ax1)
            ax1.set_title(f"Auswertung der gewünschten Parameter", fontsize=15)
            ax1.set_ylabel(y1)
            ax1.set_xlabel(x)
          

            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()

            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                agg_data = df_choice.groupby('x').mean().reset_index()
            else:
                agg_data = df_choice.groupby('x').sum().reset_index()

            # Visualisiere die aggregierten Verkaufsdaten in Liniendiagramm
            ax2.plot(ax1.get_xticks(),agg_data['y2'], color='red', marker='o')
            ax2.set_ylabel(y2)
            #ax2.set_xticks(range(len(df_choice['x'])))
            

            # Layout anpassen und anzeigen
            plt.tight_layout()
            st.pyplot(fig)

        elif (y1 == 'Weekly_Sales' or y2 == 'Weekly_Sales') and x != 'Date' and not (y1 == 'Size' or y2 == 'Size'):
            st.write('Case2.3')
            st.write("Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!")



        elif (y1 == 'Weekly_Sales' or y2 == 'Weekly_Sales') and x != 'Date' and (y1 == 'Size' or y2 == 'Size'):
            st.write('Case2.4')

            # Erstelle Figur und die erste Achse
            fig, ax1 = plt.subplots(figsize=(15,6))

            # Zeichne Balkendiagramm (x und y1)
            sns.barplot(x='x', y='y1', data=df_choice, palette='cool', ax=ax1)
            ax1.set_title(f"Auswertung der gewünschten Parameter", fontsize=15)
            ax1.set_ylabel(y1)
            ax1.set_xlabel(x)
          

            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()

            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                agg_data = df_choice.groupby('x').mean().reset_index()
            else:
                agg_data = df_choice.groupby('x').sum().reset_index()

            # Visualisiere die aggregierten Verkaufsdaten in Liniendiagramm
            ax2.plot(ax1.get_xticks(),agg_data['y2'], color='red', marker='o')
            ax2.set_ylabel(y2)
            #ax2.set_xticks(range(len(df_choice['x'])))
            

            # Layout anpassen und anzeigen
            plt.tight_layout()
            st.pyplot(fig)



       




    # Case3: 1 Achse, var1 ist nicht weekly sales

    elif y1 != 'Weekly_Sales' and y2 == None:

        if y1 == 'Type':
            

            # Case3.1: y1 == Type -> Pie-Chart


            # Pie-Chart Store-Typen
            st.write("Case3.1")
            labels = merge_train.Type.value_counts().index.tolist()
            sizes = merge_train.Type.value_counts().values.tolist()
            palette = sns.color_palette('cool', n_colors=len(labels))
            colors = palette.as_hex()
            explode = (0.05, 0.02, 0)
            plt.figure(figsize=(8,8))  # Setze die Größe des Pie-Charts
            plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=60,
            textprops={'fontsize': 18}, colors=colors)
            plt.title('Store Arten')

            # Zeige das Pie-Chart an
            st.pyplot()

            # Type A ist jetzt Type 1
            # Type B ist jetzt Type 2
            # Type C ist jetzt Type 3



            # Boxplot Type vs. Size
            st.write("Case3.1")
            fig, ax2 = plt.subplots(figsize=(15,6))
            sns.set_style('whitegrid')
            sns.boxplot(x='Type', y='Size', data=merge_train, palette='cool', ax=ax2)
            plt.title('Type vs Size', fontsize=15)
            st.pyplot(fig)




        # Case3.2: y1 == Store 

        if y1 == 'Store' and x == 'Size':
            

            # Barchart Stores, Size, Typen
            st.write('Case3.2')
            plt.subplots(figsize=(15,6))
            sns.barplot(x='Store', y='Size', data=merge_train, hue='Type', palette='cool', order=merge_train.sort_values('Size')['Store'].tolist())
            plt.title('Größe der Stores', fontsize=15)
            plt.tight_layout()
            st.pyplot(fig)



            # Barchart Store, Weekly_Sales
            st.write('Case3.2')
            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                agg_data_c3_2 = merge_train.groupby('Store')['Weekly_Sales'].mean().reset_index()
            else:
                agg_data_c3_2 = merge_train.groupby('Store')['Weekly_Sales'].sum().reset_index()

            # Barplot zeichnen und beschriften
            plt.style.use('default')
            plt.figure(figsize=(15,6))

            # In sns.barplot x und y explizit angeben
            sns.barplot(x='Store', y='Weekly_Sales', data=agg_data_c3_2, palette='cool')

            plt.grid(True)
            plt.title('Durchschnittliche Verkäufe pro Store', fontsize=18)
            plt.ylabel('Sales', fontsize=16)
            plt.xlabel('Store', fontsize=16)
            plt.tight_layout()
            st.pyplot(fig)



        # Case 3.3: y1 == Dept 

        if y1 == 'Dept':
            
            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                agg_data_c3_3 = merge_train.groupby('Dept')['Weekly_Sales'].mean().reset_index()
            else:
                agg_data_c3_3 = merge_train.groupby('Dept')['Weekly_Sales'].sum().reset_index()

            # Barplot zeichnen und beschriften
            st.write('Case3.3')
            plt.style.use('default')
            plt.figure(figsize=(15,6))
            sns.barplot(x='Dept', y='Weekly_Sales',data=agg_data_c3_3, palette='cool')
            plt.grid(True)
            plt.title('Gewünschte Auswertung', fontsize=18)
            plt.ylabel('Sales', fontsize=16)
            plt.xlabel('Departments', fontsize=16)
            st.pyplot(fig)



        # Case 3.4: y1 == Temperatur 
        if y1 == 'Temperature':
            

            df_c3_4 = pd.DataFrame({'Date':merge_train['Date'],
                                    'Year':merge_train['Date'].dt.year, 
                                    'Month':merge_train['Date'].dt.month,
                                    'Week':merge_train['Date'].dt.isocalendar().week,
                                    'Temperature':merge_train['Temperature']})
                
                
            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                temperatur_aggregated_c3_4 = df_c3_4.groupby(['Year', 'Month']).agg({'Temperature': 'mean'}).reset_index()
            else:
                temperatur_aggregated_c3_4 = df_c3_4.groupby(['Year', 'Month']).agg({'Temperature': 'sum'}).reset_index()

                
            # Zeichne Liniendiagramm nach Monaten
            st.write('Case3.4')

            # Erstelle eine Figur und Achse
            fig, ax2 = plt.subplots(figsize=(15,6))

            sns.lineplot(x='Month', y='Temperature', hue='Year', data=temperatur_aggregated_c3_4, palette='cool',ax=ax2)

            # Setze Titel und Achsenbeschriftungen 
            ax2.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax2.set_xlabel('Monate', fontsize=15)
            ax2.set_ylabel('Temperatur', fontsize=15)




            # Pointplot erstellen
            st.write('Case3.4')
            plt.figure(figsize=(15,6))
            sns.pointplot(x="Date", y="Temperature", data=merge_train, color = 'salmon')
            plt.xlabel('Time Period')
            plt.ylabel('Temperature')
            plt.title('Temperature over Time')
            st.pyplot(fig)



            # Layout anpassen und Plots anzeigen
            plt.tight_layout()
            st.pyplot(fig)
    



        # Case 3.5: y1 == CPI 
        if y1 == 'CPI' and x == 'Date':
            df_c3_5 = pd.DataFrame({
                'Date': merge_train['Date'],
                'Year': merge_train['Date'].dt.year, 
                'Month': merge_train['Date'].dt.month,
                'Week': merge_train['Date'].dt.isocalendar().week,
                'CPI': merge_train['CPI']
            })
            
            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                cpi_aggregated_c3_5 = df_c3_5.groupby(['Year', 'Month']).agg({'CPI': 'mean'}).reset_index()
            else:
                cpi_aggregated_c3_5 = df_c3_5.groupby(['Year', 'Month']).agg({'CPI': 'sum'}).reset_index()

            # Zeichne Liniendiagramm nach Monaten
            st.write('Case 3.5')

            # Erstelle eine Figur und Achse
            fig, ax2 = plt.subplots(figsize=(15,6))

            # Zeichne das Liniendiagramm
            sns.lineplot(x='Month', y='CPI', hue='Year', data=cpi_aggregated_c3_5, palette='cool', ax=ax2)

            # Setze Titel und Achsenbeschriftungen 
            ax2.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax2.set_xlabel('Month', fontsize=15)
            ax2.set_ylabel('CPI', fontsize=15)

            # Layout anpassen und Plot anzeigen
            plt.tight_layout()
            st.pyplot(fig)

            # Erstelle Pointplot separat
            fig2, ax3 = plt.subplots(figsize=(15,6))
            
            sns.pointplot(x="Year", y="CPI", data=cpi_aggregated_c3_5, color='turquoise', ax=ax3)
            
            ax3.set_xlabel('Month', fontsize=15)
            ax3.set_ylabel('Consumer Price Index', fontsize=15)
            ax3.set_title('Consumer Price Index over Time', fontsize=18)

            plt.tight_layout()
            st.pyplot(fig2)

        elif y1 == 'CPI' and x != 'Date':
            st.write('Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!')




        # Case 3.6: y1 == Unemployment  
        if y1 == 'Unemployment' and x == 'Date':
            


            df_c3_6 = pd.DataFrame({'Date':merge_train['Date'],
                                    'Year':merge_train['Date'].dt.year, 
                                    'Month':merge_train['Date'].dt.month,
                                    'Week':merge_train['Date'].dt.isocalendar().week,
                                    'Unemployment':merge_train['Unemployment']})
                
                
            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                unemployment_aggregated_c3_6 = df_c3_6.groupby(['Year', 'Month']).agg({'Unemployment': 'mean'}).reset_index()
            else:
                unemployment_aggregated_c3_6 = df_c3_6.groupby(['Year', 'Month']).agg({'Unemployment': 'sum'}).reset_index()


            # Zeichne Liniendiagramm nach Monaten
            st.write('Case3.6')

            # Erstelle eine Figur und Achse
            fig, ax2 = plt.subplots(figsize=(15,6))

            sns.lineplot(x='Month', y='Unemployment', hue='Year', data=unemployment_aggregated_c3_6, palette='cool',ax=ax2)

            # Setze Titel und Achsenbeschriftungen 
            ax2.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax2.set_xlabel('Monate', fontsize=15)
            ax2.set_ylabel('Arbeitslosigkeit', fontsize=15)

            # Layout anpassen und Plots anzeigen
            plt.tight_layout()
            st.pyplot(fig)


            # Erstelle Pointplot
            st.write('Case3.6')
            fig2, ax3 = plt.subplots(figsize=(15,6))
            sns.pointplot(x="Year", y="Unemployment", data=unemployment_aggregated_c3_6, color='khaki', ax=ax3)
            plt.xlabel('Jahre')
            plt.ylabel('Arbeitslosigkeit')
            plt.title('Unemployment over Time')
            st.pyplot(fig2)


        elif y1 == 'Unemployment' and x != 'Date':
            st.write('Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!')




        # Case 3.7: y1 == IsHoliday  
        if y1 == 'IsHoliday' and x == 'Date':
            

            df_c3_7 = pd.DataFrame({'Date': merge_train['Date'],
                                    'Year': merge_train['Date'].dt.year, 
                                    'Month': merge_train['Date'].dt.month,
                                    'Week': merge_train['Date'].dt.isocalendar().week,
                                    'IsHoliday': merge_train['IsHoliday']})


            isholiday_aggregated_c3_7 = df_c3_7.groupby(['Year', 'Month']).agg({'IsHoliday': 'sum'}).reset_index()
            

            # Erstelle eine Figur und Achse
            fig, ax = plt.subplots(figsize=(15,6))

            # Erstelle stem-plot
            st.write('Case3.7')
            
            markerline, stemlines, baseline = ax.stem(isholiday_aggregated_c3_7['Month'], isholiday_aggregated_c3_7['IsHoliday'], markerfmt='o', label='Feiertage')

            # Setze die Farbe der Linien und Marker auf blau
            plt.setp(stemlines, 'color', 'blue')
            plt.setp(markerline, 'color', 'blue')
            plt.setp(stemlines, 'linestyle')

            # Setze Titel und Achsenbeschriftungen 
            ax.set_title('Feiertage', fontsize=15)
            ax.set_xlabel('Monate', fontsize=15)
            ax.set_ylabel('Feiertage', fontsize=15)

            # Zeige das Diagramm
            plt.tight_layout()
            st.pyplot(fig)



            # Zeichne Liniendiagramm nach Monaten
            st.write('Case3.7')

            # Erstelle eine Figur und Achse
            fig, ax2 = plt.subplots(figsize=(15,6))

            sns.lineplot(x='Month', y='IsHoliday', hue='Year', data=isholiday_aggregated_c3_7, palette='cool',ax=ax2)

            # Setze Titel und Achsenbeschriftungen 
            ax2.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax2.set_xlabel('Monate', fontsize=15)
            ax2.set_ylabel('Feiertage', fontsize=15)

            # Layout anpassen und Plots anzeigen
            plt.tight_layout()
            st.pyplot(fig)

        elif y1 == 'IsHoliday' and x != 'Date':
            st.write('Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!')




        # Case 3.8: y1 == Size  
        if y1 == 'Size' and x == 'Store':

     
            # Barplot Size, Store, Type
            st.write('Case3.8')

            fig,ax = plt.subplots(figsize=(15,6))
            sns.barplot(x='Store',y='Size',data=merge_train,hue=merge_train['Type'], palette='cool',order=merge_train.sort_values('Size')['Store'].tolist())
            plt.title('Gewünschte Auswertung',fontsize=15)
            plt.tight_layout()
            st.pyplot(fig)

        elif y1 == 'Size' and x == 'Date':
            st.write('Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!')
        



        # Case 3.9: y1 == Fuel_Price  
        if y1 == 'Fuel_Price' and x == 'Date':

            df_c3_9 = pd.DataFrame({
                'Date': merge_train['Date'],
                'Year': merge_train['Date'].dt.year.astype(int), 
                'Month': merge_train['Date'].dt.month,
                'Week': merge_train['Date'].dt.isocalendar().week,
                'Fuel_Price': merge_train['Fuel_Price']
            })

            # Wähle die Aggregationsfunktion für Plot 1
            if operation == 'Mittelwert':
                fuelprice_aggregated_c3_9_1 = df_c3_9.groupby(['Date']).agg({'Fuel_Price': 'mean'}).reset_index()  # Plot 1
                fuelprice_aggregated_c3_9_2 = df_c3_9.groupby(['Year', 'Month']).agg({'Fuel_Price': 'mean'}).reset_index()  # Plot 2 & 3
            else:
                fuelprice_aggregated_c3_9_1 = df_c3_9.groupby(['Date']).agg({'Fuel_Price': 'sum'}).reset_index()  # Plot 1
                fuelprice_aggregated_c3_9_2 = df_c3_9.groupby(['Year', 'Month']).agg({'Fuel_Price': 'sum'}).reset_index()  # Plot 2 & 3

            # Zeichne Liniendiagramm nach Jahren
            st.write('Case3.9')
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Fuel_Price', data=fuelprice_aggregated_c3_9_1, ax=ax1)
            ax1.set_title('Durchschnittlicher Fuel Price pro Jahr', fontsize=18)
            ax1.set_xlabel('Jahre', fontsize=15)
            ax1.set_ylabel('Fuel_Price', fontsize=15)
            plt.tight_layout()
            st.pyplot(fig1)  # Zeige das erste Diagramm

            # Erstelle Pointplot
            st.write('Case3.9')
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.pointplot(x='Month', y='Fuel_Price', data=fuelprice_aggregated_c3_9_2, color='sandybrown', ax=ax2, hue='Year')
            ax2.set_xlabel('Monate', fontsize=15)
            ax2.set_ylabel('Fuel Price', fontsize=15)
            ax2.set_title('Durchschnittlicher Fuel Price pro Monat und Jahr', fontsize=15)
            plt.tight_layout()
            st.pyplot(fig2)  # Zeige das zweite Diagramm

            # Zeichne Liniendiagramm nach Monaten
            st.write('Case3.9')
            fig3, ax3 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='Fuel_Price', hue='Year', data=fuelprice_aggregated_c3_9_2, palette='cool', ax=ax3)
            ax3.set_title('Fuel Price nach Monaten über Jahre', fontsize=15)
            ax3.set_xlabel('Monate', fontsize=15)
            ax3.set_ylabel('Fuel_Price', fontsize=15)
            plt.tight_layout()
            st.pyplot(fig3)  # Zeige das dritte Diagramm

        elif y1 == 'Fuel_Price' and x != 'Date':
            st.write("Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!")




        # Case 3.10: y1 == MarkDown1
        if y1 == 'MarkDown1' and x == 'Date':
            

            df_c3_10 = pd.DataFrame({'Date':merge_train['Date'],
                                    'Year':merge_train['Date'].dt.year, 
                                    'Month':merge_train['Date'].dt.month,
                                    'Week':merge_train['Date'].dt.isocalendar().week,
                                    'MarkDown1':merge_train['MarkDown1'],
                                    'MarkDown2':merge_train['MarkDown2'],
                                    'MarkDown3':merge_train['MarkDown3'],
                                    'MarkDown4':merge_train['MarkDown4'],
                                    'MarkDown5':merge_train['MarkDown5']})

            # Erstelle das Diagramm1 - Nur MarkDown1 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown1', hue='Year', data=df_c3_10, palette='cool', ax=ax1)
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax1.set_xlabel('Monate', fontsize=15)
            ax1.set_ylabel('MarkDown1', fontsize=15)
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            # Bereite Daten für Diagramm2 vor - Alle MarkDowns im Jahresverlauf
            df_c3_10_long = df_c3_10.melt(id_vars=['Date'], value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                        var_name='MarkDown', value_name='Value')

            # Erstelle Diagramm2 - Alle MarkDowns im Jahresverlauf
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_10_long, palette='cool', ax=ax2)
            ax2.set_title('MarkDowns 1-5 im Jahresverlauf', fontsize=15)
            ax2.set_xlabel('Jahre', fontsize=15)
            ax2.set_ylabel('MarkDowns 1-5', fontsize=15)
            plt.tight_layout()

            # Zeige Diagramm2 an
            st.pyplot(fig2)

        elif y1 in ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'] and x != 'Date':
            st.write('Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!')

        

        # Case 3.11: y1 == MarkDown2

        if y1 == 'MarkDown2' and x == 'Date':
            

            df_c3_11 = pd.DataFrame({'Date':merge_train['Date'],
                                    'Year':merge_train['Date'].dt.year, 
                                    'Month':merge_train['Date'].dt.month,
                                    'Week':merge_train['Date'].dt.isocalendar().week,
                                    'MarkDown1':merge_train['MarkDown1'],
                                    'MarkDown2':merge_train['MarkDown2'],
                                    'MarkDown3':merge_train['MarkDown3'],
                                    'MarkDown4':merge_train['MarkDown4'],
                                    'MarkDown5':merge_train['MarkDown5']})

            # Erstelle das Diagramm1 - Nur MarkDown2 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown2', hue='Year', data=df_c3_11, palette='cool', ax=ax1)
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax1.set_xlabel('Monate', fontsize=15)
            ax1.set_ylabel('MarkDown2', fontsize=15)
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            # Bereite Daten für Diagramm2 vor - Alle MarkDowns im Jahresverlauf
            df_c3_11_long = df_c3_11.melt(id_vars=['Date'], value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                        var_name='MarkDown', value_name='Value')

            # Erstelle Diagramm2 - Alle MarkDowns im Jahresverlauf
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_11_long, palette='cool', ax=ax2)
            ax2.set_title('MarkDowns 1-5 im Jahresverlauf', fontsize=15)
            ax2.set_xlabel('Jahre', fontsize=15)
            ax2.set_ylabel('MarkDowns 1-5', fontsize=15)
            plt.tight_layout()

            # Zeige Diagramm2 an
            st.pyplot(fig2)

        elif y1 in ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'] and x != 'Date':
            st.write('Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!')





        # Case 3.12: y1 == MarkDown3

        if y1 == 'MarkDown3' and x == 'Date':
            

            df_c3_12 = pd.DataFrame({'Date':merge_train['Date'],
                                    'Year':merge_train['Date'].dt.year, 
                                    'Month':merge_train['Date'].dt.month,
                                    'Week':merge_train['Date'].dt.isocalendar().week,
                                    'MarkDown1':merge_train['MarkDown1'],
                                    'MarkDown2':merge_train['MarkDown2'],
                                    'MarkDown3':merge_train['MarkDown3'],
                                    'MarkDown4':merge_train['MarkDown4'],
                                    'MarkDown5':merge_train['MarkDown5']})

            # Erstelle das Diagramm1 - Nur MarkDown3 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown3', hue='Year', data=df_c3_12, palette='cool', ax=ax1)
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax1.set_xlabel('Monate', fontsize=15)
            ax1.set_ylabel('MarkDown3', fontsize=15)
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            # Bereite Daten für Diagramm2 vor - Alle MarkDowns im Jahresverlauf
            df_c3_12_long = df_c3_12.melt(id_vars=['Date'], value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                        var_name='MarkDown', value_name='Value')

            # Erstelle Diagramm2 - Alle MarkDowns im Jahresverlauf
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_12_long, palette='cool', ax=ax2)
            ax2.set_title('MarkDowns 1-5 im Jahresverlauf', fontsize=15)
            ax2.set_xlabel('Jahre', fontsize=15)
            ax2.set_ylabel('MarkDowns 1-5', fontsize=15)
            plt.tight_layout()

            # Zeige Diagramm2 an
            st.pyplot(fig2)

        elif y1 in ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'] and x != 'Date':
            st.write('Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!')





        # Case 3.13: y1 == MarkDown4


        if y1 == 'MarkDown4' and x == 'Date':
            

            df_c3_13 = pd.DataFrame({'Date':merge_train['Date'],
                                    'Year':merge_train['Date'].dt.year, 
                                    'Month':merge_train['Date'].dt.month,
                                    'Week':merge_train['Date'].dt.isocalendar().week,
                                    'MarkDown1':merge_train['MarkDown1'],
                                    'MarkDown2':merge_train['MarkDown2'],
                                    'MarkDown3':merge_train['MarkDown3'],
                                    'MarkDown4':merge_train['MarkDown4'],
                                    'MarkDown5':merge_train['MarkDown5']})

            # Erstelle das Diagramm1 - Nur MarkDown4 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown4', hue='Year', data=df_c3_13, palette='cool', ax=ax1)
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax1.set_xlabel('Monate', fontsize=15)
            ax1.set_ylabel('MarkDown4', fontsize=15)
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            # Bereite Daten für Diagramm2 vor - Alle MarkDowns im Jahresverlauf
            df_c3_13_long = df_c3_13.melt(id_vars=['Date'], value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                        var_name='MarkDown', value_name='Value')

            # Erstelle Diagramm2 - Alle MarkDowns im Jahresverlauf
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_13_long, palette='cool', ax=ax2)
            ax2.set_title('MarkDowns 1-5 im Jahresverlauf', fontsize=15)
            ax2.set_xlabel('Jahre', fontsize=15)
            ax2.set_ylabel('MarkDowns 1-5', fontsize=15)
            plt.tight_layout()

            # Zeige Diagramm2 an
            st.pyplot(fig2)

        elif y1 in ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'] and x != 'Date':
            st.write('Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!')





        # Case 3.14: y1 == MarkDown5

        if y1 == 'MarkDown5' and x == 'Date':
            

            df_c3_14 = pd.DataFrame({'Date':merge_train['Date'],
                                    'Year':merge_train['Date'].dt.year, 
                                    'Month':merge_train['Date'].dt.month,
                                    'Week':merge_train['Date'].dt.isocalendar().week,
                                    'MarkDown1':merge_train['MarkDown1'],
                                    'MarkDown2':merge_train['MarkDown2'],
                                    'MarkDown3':merge_train['MarkDown3'],
                                    'MarkDown4':merge_train['MarkDown4'],
                                    'MarkDown5':merge_train['MarkDown5']})

            # Erstelle das Diagramm1 - Nur MarkDown4 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown5', hue='Year', data=df_c3_14, palette='cool', ax=ax1)
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax1.set_xlabel('Monate', fontsize=15)
            ax1.set_ylabel('MarkDown5', fontsize=15)
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            # Bereite Daten für Diagramm2 vor - Alle MarkDowns im Jahresverlauf
            df_c3_14_long = df_c3_14.melt(id_vars=['Date'], value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                        var_name='MarkDown', value_name='Value')

            # Erstelle Diagramm2 - Alle MarkDowns im Jahresverlauf
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_14_long, palette='cool', ax=ax2)
            ax2.set_title('MarkDowns 1-5 im Jahresverlauf', fontsize=15)
            ax2.set_xlabel('Jahre', fontsize=15)
            ax2.set_ylabel('MarkDowns 1-5', fontsize=15)
            plt.tight_layout()

            # Zeige Diagramm2 an
            st.pyplot(fig2)

        elif y1 in ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'] and x != 'Date':
            st.write('Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!')





    # Case4: 2 y-Achsen, var1 und var2 sind nicht weekly sales

    if y1 != 'Weekly_Sales' and y2 != 'Weekly_Sales' and x == 'Date' and y2 is not None:
        
        # DataFrame erstellen
        df_c4 = pd.DataFrame({
            'Date': merge_train['Date'],
            'Year': merge_train['Date'].dt.year, 
            'Month': merge_train['Date'].dt.month,
            'Week': merge_train['Date'].dt.isocalendar().week,
            y1: merge_train[y1],  # Hier wird die Spalte direkt referenziert
            y2: merge_train[y2]
        })

        # Wähle die Aggregationsfunktion
        if operation == 'Mittelwert':
            agg_c4_month = df_c4.groupby(['Year', 'Month']).agg({y1: 'mean', y2: 'mean'}).reset_index()
            agg_c4_year = df_c4.groupby('Date').agg({y1: 'mean', y2: 'mean'}).reset_index()
        else:
            agg_c4_month = df_c4.groupby(['Year', 'Month']).agg({y1: 'sum', y2: 'sum'}).reset_index()
            agg_c4_year = df_c4.groupby(['Date']).agg({y1: 'sum', y2: 'sum'}).reset_index()

        if x == 'Date' and (y1 == 'Size' or y1 == 'Type' or y1 == 'Dept' or y2 == 'Size' or y2 == 'Type' or y2 == 'Dept'):
            st.write("Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!")
        
        else:

            # Zeichne Diagramm 1 - Jährliche Übersicht
            st.write('Case4.2')
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y=y1, data=agg_c4_year, color='blue', ax=ax1, label=y1)
            ax1.set_ylabel(y1, fontsize=15)
            ax1.legend(loc='upper left')

            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()
            sns.lineplot(x='Date', y=y2, data=agg_c4_year, color='red', ax=ax2, label=y2)
            ax2.set_ylabel(y2, fontsize=15)
            ax2.legend(loc='upper right')

            # Setze Titel und Achsenbeschriftungen 
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax1.set_xlabel('Datum', fontsize=15)
            plt.tight_layout()
            st.pyplot(fig1)

            # Zeichne Diagramm 2 - Monatliche Übersicht
            st.write('Case4.2')
            fig2, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y=y1, data=agg_c4_month, color='blue', ax=ax1, hue='Year', palette='cool')
            ax1.set_ylabel(y1, fontsize=15)
            ax1.legend(loc='upper left')

            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()
            sns.lineplot(x='Month', y=y2, data=agg_c4_month, color='red', ax=ax2, hue='Year', palette='Wistia')
            ax2.set_ylabel(y2, fontsize=15)
            ax2.legend(loc='upper right')

            # Setze Titel und Achsenbeschriftungen 
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax1.set_xlabel('Monate', fontsize=15)
            plt.tight_layout()
            st.pyplot(fig2)

    elif y1 != 'Weekly_Sales' and y2 != 'Weekly_Sales' and x != 'Date' and y2 is not None:   
        st.write('Case4.3')
        st.write("Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!")
