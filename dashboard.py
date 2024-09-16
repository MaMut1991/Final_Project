# Funktion für Dashboard; Parameter werden per Auswahlmöglichkeiten in App übergeben
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessing
import streamlit as st



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

    merge_train = preprocessing.merge_train


    # Case1: 1 Achse, var1 ist weekly sales

    if y1 == 'Weekly_Sales' and y2 == None: 

        # Temporärer DataFrame für die getätigte Auswahl in der App
        df_choice = pd.DataFrame({
            'x': merge_train[x],   # Variable für die x-Achse
            'y1': merge_train[y1], # Variable für die y1-Achse
        })
        
        # Case1.1: x != Date -> Balkendiagramm
        if x != 'Date':

            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                agg_data_c1_1 = df_choice.groupby('x').mean().reset_index()
            else:
                agg_data_c1_1 = df_choice.groupby('x').sum().reset_index()

        
            # Zeitreihenanalyse Plot 1 (nur Balkendiagramm)

            # Erstelle eine Figur und Achse
            fig, ax = plt.subplots(figsize=(15,6))

            # Zeichne Balkendiagramm
            sns.barplot(x='x', y='y1', data=agg_data_c1_1, palette='cool',ax=ax)

            # Setze Titel und Achsenbeschriftungen auf dem Achsenobjekt
            ax.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax.set_xlabel(x)
            ax.set_ylabel(y1)

            # Zeige das Diagramm
            plt.tight_layout()
            st.pyplot(fig)

        # Case1.2: x == Date  -> Zeitreihenanalyse per Liniendiagramm

        else:  
      
            # Zeitreihenanalyse Plot 2 (Liniendiagramm nach Jahren)

            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                agg_data_c1_2 = df_choice.groupby('x').mean().reset_index()
            else:
                agg_data_c1_2 = df_choice.groupby('x').sum().reset_index()
            
            # Erstelle eine Figur und Achse
            fig, ax = plt.subplots(figsize=(15,6))

            # Zeichne Liniendiagramm und setze Titel und Achsenbeschriftung
            sns.lineplot(x='x', y='y1', data=agg_data_c1_2, palette='cool', ax=ax)
            ax.set_title('Zeitreihenanalye 1: Weekly Sales', fontsize=18)
            ax.set_ylabel('Sales', fontsize=16)
            ax.set_xlabel('Date', fontsize=16)

            # Setze Titel und Achsenbeschriftungen auf dem Achsenobjekt für Plot 2
            ax.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax.set_xlabel(x)
            ax.set_ylabel(y1)


            # Zeitreihenanalyse Plot 3 (Liniendiagramm nach Monaten mit 1 Linie pro Jahr)

            # Erstelle eine Figur und Achse
            fig, ax2 = plt.subplots(figsize=(15,6))

            # Data Frame mit Jahren, Wochen, Monaten und Weekly_Sales erstellen
            df_datetime = pd.DataFrame({'Date':merge_train['Date'],
                                        'Year':merge_train['Date'].dt.year, 
                                        'Month':merge_train['Date'].dt.month,
                                        'Week':merge_train['Date'].dt.isocalendar().week,
                                        'Weekly_Sales':merge_train['Weekly_Sales']})
            
            
            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                datetime_aggregated = df_datetime.groupby(['Year', 'Month']).agg({'Weekly_Sales': 'mean'}).reset_index()
            else:
                datetime_aggregated = df_datetime.groupby(['Year', 'Month']).agg({'Weekly_Sales': 'sum'}).reset_index()

            # Zeichne Liniendiagramm und setze Titel und Achsenbeschriftung

            sns.lineplot(x='Month', y='Weekly_Sales', hue='Year', data=datetime_aggregated, palette='cool',ax=ax2)
        
            # Setze Titel und Achsenbeschriftungen auf dem Achsenobjekt für Plot 3
            ax2.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax2.set_xlabel('Month')
            ax2.set_ylabel(y1)

            # Layout anpassen und Plots anzeigen
            plt.tight_layout()
            st.pyplot(fig)


            


    # Case2: 2 Achsen, var1 oder var2 sind weekly sales

    elif (y1 == 'Weekly_Sales' or y2 == 'Weekly_Sales') and y2 is not None:
        
        # Temporärer DataFrame für die getätigte Auswahl in der App
        df_choice = pd.DataFrame({
            'x': merge_train[x],   # Variable für die x-Achse
            'y1': merge_train[y1], # Variable für die y1-Achse
            'y2': merge_train[y2]  # Variable für die y2-Achse
        })

        if y1 == 'Weekly_Sales':   # Falls y1 gleich Weekly_Sales ist
            
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




        else:  # Falls y2 gleich Weekly_Sales ist

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

    elif y1 != 'Weekly_Sales' and y2 == None and x != 'Date':

        if y1 == 'Type':

            # Case3.1: y1 == Type -> Pie-Chart


            # Pie-Chart Store-Typen
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
        fig, ax2 = plt.subplots(figsize=(15,6))
        sns.set_style('whitegrid')
        sns.boxplot(x='Type', y='Size', data=merge_train, palette='cool', ax=ax2)
        plt.title('Type vs Size', fontsize=15)
        st.pyplot(fig)




        # Case3.2: y1 == Store 

        if (y1 == 'Store' or y1 == 'Size'):

            # Barchart Stores, Size, Typen

            plt.subplots(figsize=(15,6))
            sns.barplot(x='Store', y='Size', data=merge_train, hue='Type', palette='cool', order=merge_train.sort_values('Size')['Store'].tolist())
            plt.title('Größe der Stores', fontsize=15)
            plt.tight_layout()
            st.pyplot(fig)



        # Barchart Store, Weekly_Sales

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


        # Wähle die Aggregationsfunktion
        if operation == 'Mittelwert':
            agg_data_c3_3 = merge_train.groupby('Dept')['Weekly_Sales'].mean().reset_index()
        else:
            agg_data_c3_3 = merge_train.groupby('Dept')['Weekly_Sales'].sum().reset_index()

        # Barplot zeichnen und beschriften
        plt.style.use('default')
        plt.figure(figsize=(15,6))
        sns.barplot(x='Dept', y='Weekly_Sales',data=agg_data_c3_3, palette='cool')
        plt.grid(True)
        plt.title('Gewünschte Auswertung', fontsize=18)
        plt.ylabel('Sales', fontsize=16)
        plt.xlabel('Departments', fontsize=16)
        st.pyplot(fig)



        # Case 3.4: y1 == Temperatur 


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


        # Erstelle eine Figur und Achse
        fig, ax2 = plt.subplots(figsize=(15,6))

        sns.lineplot(x='Month', y='Temperature', hue='Year', data=temperatur_aggregated_c3_4, palette='cool',ax=ax2)

        # Setze Titel und Achsenbeschriftungen 
        ax2.set_title('Auswertung der gewünschten Parameter', fontsize=15)
        ax2.set_xlabel('Monate', fontsize=15)
        ax2.set_ylabel('Temperatur', fontsize=15)




        # Pointplot erstellen
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

        df_c3_5 = pd.DataFrame({'Date':merge_train['Date'],
                                'Year':merge_train['Date'].dt.year, 
                                'Month':merge_train['Date'].dt.month,
                                'Week':merge_train['Date'].dt.isocalendar().week,
                                'CPI':merge_train['CPI']})
            
            
        # Wähle die Aggregationsfunktion
        if operation == 'Mittelwert':
            cpi_aggregated_c3_5 = df_c3_5.groupby(['Year', 'Month']).agg({'CPI': 'mean'}).reset_index()
        else:
            cpi_aggregated_c3_5 = df_c3_5.groupby(['Year', 'Month']).agg({'CPI': 'sum'}).reset_index()


        # Zeichne Liniendiagramm nach Monaten


        # Erstelle eine Figur und Achse
        fig, ax2 = plt.subplots(figsize=(15,6))

        sns.lineplot(x='Month', y='CPI', hue='Year', data=cpi_aggregated_c3_5, palette='cool',ax=ax2)

        # Setze Titel und Achsenbeschriftungen 
        ax2.set_title('Auswertung der gewünschten Parameter', fontsize=15)
        ax2.set_xlabel('Month', fontsize=15)
        ax2.set_ylabel(y1, fontsize=15)



        # Erstelle Pointplot
        plt.figure(figsize=(15,6))
        sns.pointplot(x="Date", y="CPI", data=cpi_aggregated_c3_5, color = 'turquoise')
        plt.xlabel('Time Period')
        plt.ylabel('Consumer Price Index')
        plt.title('Consumer Price Index over Time')
        st.pyplot(fig)



        # Layout anpassen und Plots anzeigen
        plt.tight_layout()
        st.pyplot(fig)




        # Case 3.6: y1 == Unemployment  


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
        plt.figure(figsize=(15,6))
        sns.pointplot(x="Date", y="Unemployment", data=unemployment_aggregated_c3_6, color='khaki')
        plt.xlabel('Time Period')
        plt.ylabel('Unemployment')
        plt.title('Unemployment over Time')
        st.pyplot(fig)




        # Case 3.7: y1 == IsHoliday  

        df_c3_7 = pd.DataFrame({'Date': merge_train['Date'],
                                'Year': merge_train['Date'].dt.year, 
                                'Month': merge_train['Date'].dt.month,
                                'Week': merge_train['Date'].dt.isocalendar().week,
                                'IsHoliday': merge_train['IsHoliday']})


        isholiday_aggregated_c3_7 = df_c3_7.groupby(['Year', 'Month']).agg({'IsHoliday': 'sum'}).reset_index()

        # Erstelle eine Figur und Achse
        fig, ax = plt.subplots(figsize=(15,6))

        # Erstelle stem-plot
        
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




        # Case 3.8: y1 == Size  


        #Boxplot Type, Size

        sns.set_style('whitegrid')
        sns.boxplot(x='Type',y='Size',data=merge_train,palette='cool')
        plt.title('Gewünschte Auswertung',fontsize=15)


        # Barplot Size, Store, Type

        plt.subplots(figsize=(15,6))
        sns.barplot(x='Store',y='Size',data=merge_train,hue=merge_train['Type'], palette='cool',order=merge_train.sort_values('Size')['Store'].tolist())
        plt.title('Gewünschte Auswertung',fontsize=15)
        plt.tight_layout()
        st.pyplot(fig)
        



        # Case 3.9: y1 == Fuel_Price  


        df_c3_9 = pd.DataFrame({'Date':merge_train['Date'],
                                'Year':merge_train['Date'].dt.year, 
                                'Month':merge_train['Date'].dt.month,
                                'Week':merge_train['Date'].dt.isocalendar().week,
                                'Fuel_Price':merge_train['Fuel_Price']})
            
            
        # Wähle die Aggregationsfunktion
        if operation == 'Mittelwert':
            fuelprice_aggregated_c3_9 = df_c3_9.groupby(['Year', 'Month']).agg({'Fuel_Price': 'mean'}).reset_index()
        else:
            fuelprice_aggregated_c3_9 = df_c3_9.groupby(['Year', 'Month']).agg({'Fuel_Price': 'sum'}).reset_index()

            
        # Zeichne Liniendiagramm nach Jahren


        # Erstelle eine Figur und Achse
        fig, ax = plt.subplots(figsize=(15,6))

        # Zeichne Liniendiagramm und setze Titel und Achsenbeschriftung
        sns.lineplot(x='Year', y='Fuel_Price', data=fuelprice_aggregated_c3_9, palette='cool', ax=ax)


        # Setze Titel und Achsenbeschriftungen auf dem Achsenobjekt 
        ax.set_title('Gewünschte Auswertung', fontsize=18)
        ax.set_ylabel('Fuel_Price', fontsize=15)
        ax.set_xlabel('Jahre', fontsize=15)




        # Erstelle pointplot
        plt.figure(figsize=(15,6))
        sns.pointplot(x="Date", y="Fuel_Price", data=fuelprice_aggregated_c3_9, color = 'sandybrown')
        plt.xlabel('Time Period')
        plt.ylabel('Fuel Price')
        plt.title('Fuel Price over Time')
        st.pyplot(fig)




        # Zeichne Liniendiagramm nach Monaten


        # Erstelle eine Figur und Achse
        fig, ax2 = plt.subplots(figsize=(15,6))

        sns.lineplot(x='Month', y='Fuel_Price', hue='Year', data=fuelprice_aggregated_c3_9, palette='cool',ax=ax2)

        # Setze Titel und Achsenbeschriftungen 
        ax2.set_title('Auswertung der gewünschten Parameter', fontsize=15)
        ax2.set_xlabel('Monate', fontsize=15)
        ax2.set_ylabel('Fuel_Price', fontsize=15)

        # Layout anpassen und Plots anzeigen
        plt.tight_layout()
        st.pyplot(fig)



        # Case 3.10: y1 == MarkDown1-5 
        

        df_c3_10 = pd.DataFrame({'Date':merge_train['Date'],
                                'Year':merge_train['Date'].dt.year, 
                                'Month':merge_train['Date'].dt.month,
                                'Week':merge_train['Date'].dt.isocalendar().week,
                                'MarkDown1':merge_train['MarkDown1'],
                                'MarkDown2':merge_train['MarkDown2'],
                                'MarkDown3':merge_train['MarkDown3'],
                                'MarkDown4':merge_train['MarkDown4'],
                                'MarkDown5':merge_train['MarkDown5']})

        # Erstelle eine Figur und Achsen für Subplots
        fig, axes = plt.subplots(5, 1, figsize=(15,6))  # 5 Zeilen, 1 Spalte

        # Liste der MarkDown-Spalten
        markdown_columns = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']

        # Zeichne für jede Spalte ein Seaborn-Liniendiagramm
        for i, column in enumerate(markdown_columns):
            sns.lineplot(x='Month', y=column, data=df_c3_10, ax=axes[i], hue='Year', palette='cool')
            axes[i].set_title(f'{column} über Monate')  # Setze Titel für jeden Plot
            axes[i].set_ylabel(column)

        # Passe das Layout an, damit die Plots sich nicht überlappen
        plt.tight_layout()

        # Zeige die Plots an
        st.pyplot(fig)



    # Case4: 2 Achsen, var1 und var2 sind nicht weekly sales


    elif (y1 != 'Weekly_Sales' and y2 != 'Weekly_Sales') and y2 != None:
        
       
        if x != 'Date':   # Wenn auf x-Achse keine Zeit angegeben
            
            print("Keine sinnvolle Auswertung möglich. Versuchen Sie es mit anderen Parametern.")



        else:   # Wenn auf x-Achse Zeit angegeben

            # DataFrame erstellen
            df_c4 = pd.DataFrame({'Date': merge_train['Date'],
                                'Year': merge_train['Date'].dt.year, 
                                'Month': merge_train['Date'].dt.month,
                                'Week': merge_train['Date'].dt.isocalendar().week,
                                y1: merge_train[y1],  # Hier wird die Spalte direkt referenziert
                                y2: merge_train[y2]})

            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                agg_c4 = df_c4.groupby(['Year', 'Month']).agg({y1: 'mean', y2: 'mean'}).reset_index()
            else:
                agg_c4 = df_c4.groupby(['Year', 'Month']).agg({y1: 'sum', y2: 'sum'}).reset_index()

            # Eine neue Spalte erstellen, um das Jahr und den Monat zu kombinieren
            agg_c4['Date'] = pd.to_datetime(agg_c4[['Year', 'Month']].assign(DAY=1))

            # Erstelle eine Figur und Achsen
            fig, ax1 = plt.subplots(figsize=(15,6))

            # Zeichne y1 als Linie auf ax1
            sns.lineplot(x='Date', y=y1, data=agg_c4, color='blue', ax=ax1, label=y1)
            ax1.set_ylabel(y1, fontsize=15)
            ax1.legend(loc='upper left')

            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()

            # Zeichne y2 als Linie auf ax2
            sns.lineplot(x='Date', y=y2, data=agg_c4, color='red', ax=ax2, label=y2)
            ax2.set_ylabel(y2, fontsize=15)
            ax2.legend(loc='upper right')

            # Setze Titel und Achsenbeschriftungen 
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax1.set_xlabel('Jahre', fontsize=15)

            # Layout anpassen und Plots anzeigen
            plt.tight_layout()
            plt.legend()
            st.pyplot(fig)


            # Zeichne Liniendiagramm nach Monaten

            # Erstelle eine Figur und Achsen
            fig, ax1 = plt.subplots(figsize=(15,6))

            # Zeichne y1 als Linie auf ax1
            sns.lineplot(x='Month', y=y1, data=agg_c4, palette='cool', ax=ax1,hue='Year')
            ax1.set_ylabel(y1, fontsize=15)
            ax1.legend(loc='upper left')

            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()

            # Zeichne y2 als Linie auf ax2
            sns.lineplot(x='Month', y=y2, data=agg_c4, palette='Wistia', ax=ax2, hue='Year')
            ax2.set_ylabel(y2, fontsize=15)
            ax2.legend(loc='upper right')

            # Setze Titel und Achsenbeschriftungen 
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax1.set_xlabel('Monate', fontsize=15)

            # Layout anpassen und Plots anzeigen
            plt.tight_layout()
            #plt.legend()
            st.pyplot(fig)



            # Zeichne Liniendiagramm nach Monaten

            # Erstelle eine Figur und Achsen
            fig, ax1 = plt.subplots(figsize=(15,6))

            # Zeichne y1 als Linie auf ax1
            sns.lineplot(x='Month', y=y1, data=agg_c4, color='blue', ax=ax1, label=y1, hue='Years')
            ax1.set_ylabel(y1, fontsize=15)
            ax1.legend(loc='upper left')

            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()

            # Zeichne y2 als Linie auf ax2
            sns.lineplot(x='Month', y=y2, data=agg_c4, color='red', ax=ax2, label=y2, hue='Years')
            ax2.set_ylabel(y2, fontsize=15)
            ax2.legend(loc='upper right')

            # Setze Titel und Achsenbeschriftungen 
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=15)
            ax1.set_xlabel('Monate', fontsize=15)

            # Layout anpassen und Plots anzeigen
            plt.tight_layout()
            plt.legend()
            st.pyplot(fig)