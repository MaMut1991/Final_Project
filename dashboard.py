# Funktion für Dashboard; Parameter werden per Auswahlmöglichkeiten in App übergeben
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

import streamlit as st
from preprocessing import data_preprocessing, get_holiday_without_Easter



def create_diagram(y1=None, y2=None, x=None, operation=None):
    '''
    Diese Funktion soll Parameter aus der Web-App entgegennehmen und gemäß der Eingabe entsprechende Diagramme zurückgeben.
    Dafür werden 4 Cases erstellt:

    Case1: Es werden die Weekly_Sales auf der y-Achse und die Zeit, die Stores oder die Departments auf der x-Achse in einem Diagramm (mit nur 1 y-Achse) dargestellt. Man hat die Ausahl die Daten als Average oder Sum darzustellen und darf den betrachteten Zeitraum auswählen.

    Case2: Es werden die Weekly_Sales auf der y-Achse und die Zeit, die Stores oder die Departments auf der x-Achse in einem Diagramm dargestellt. Im Gegensatz zu Case 1 kann hier eine zweite y-Achse für eine zweite Variable (frei wählbar) eingefügt werden. Man hat die Auswahl die Weekly_Sales als Average oder Sum darzustellen und darf den betrachteten Zeitraum auswählen.

    Case3: Es wird eine beliebige Variable, welche nicht die Weekly_Sales ist, in einem Diagramm mit einer y-Achse dargestellt. Auf der x-Achse werden ebenso nicht die Weekly_Sales berücksichtigt.

    Case4: Es werden 2 Variablen in einem Diagramm mit 2 y-Achsen dargestellt. Keine Variable beinhaltet die Weekly_Sales

    Parameter:

    y1: Variable Nr. 1, welche auf der linken y-Achse dargestellt wird
    y2: Variable Nr. 2, welche auf der rechten y-Achse dargestellt wird
    x: in der App ausgewählte Variable, welche auf der x-Achse dargestellt wird. Zur Auswahl stehen Store, Department und Zeit.
    operation: Daten als Average oder Sum auswerten und visualisieren
    '''

    # Vordefinierte Farbpaletten
    color_palette_1 = ['#FF6C3E']    # 1 Farbe für Diagramm
    color_palette_2 = ['#FF6C3E','#3ED1FF']    # 2 Farben für Diagramm
    color_palette_3 = ['#FF6C3E','#3ED1FF','#70FF3E']    # 3 Farben für Diagramm
    color_palette_4 = ['#FF6C3E','#3ED1FF','#70FF3E','#CD3EFF']    # 4 Farben für Diagramm
    
    # Vordefinierte Schriftgrößen für Achsen und Titel
    fontsize_title = 20
    fontsize_axes =15

    merge_train, merge_test = data_preprocessing()


    def plot_bar(df, x, y, ax, title, xlabel, ylabel):
        """Zeichnet ein Balkendiagramm."""
        sns.barplot(x=x, y=y, data=df, palette=color_palette_1, ax=ax, order=df.sort_values(by=y, ascending=True)[x])
        ax.set_title(title, fontsize=fontsize_title)
        ax.set_xlabel(xlabel, fontsize = fontsize_axes)
        ax.set_ylabel(ylabel,fontsize = fontsize_axes)
        ax.grid(True, linestyle='-')

    def plot_line(df, x, y, ax, title, xlabel, ylabel, hue=None):
        """Zeichnet ein Liniendiagramm."""
        sns.lineplot(x=x, y=y, hue=hue, data=df, color=color_palette_1[0], ax=ax)
        ax.set_title(title, fontsize=fontsize_title)
        ax.set_xlabel(xlabel, fontsize = fontsize_axes)
        ax.set_ylabel(ylabel, fontsize = fontsize_axes)
        ax.grid(True, linestyle='-')

    # Case1: 1 Achse: var1 ist weekly sales
    if y1 == 'Weekly_Sales' and y2 is None:

        # Temporärer DataFrame für die getätigte Auswahl in der App
        df_choice = pd.DataFrame({
            'x': merge_train[x],   # Variable für die x-Achse
            'y1': merge_train[y1], # Variable für die y1-Achse
        })

        # Case1.1: x != Date -> Balkendiagramm
        if x != 'Date':

            # Wähle die Aggregationsfunktion
            agg_func = df_choice.groupby('x').mean if operation == 'Average' else df_choice.groupby('x').sum
            agg_data = agg_func().reset_index()

            # Zeichne Balkendiagramm
            fig, ax = plt.subplots(figsize=(15,6))
            plot_bar(agg_data, 'x', 'y1', ax, 'Analysis of the desired parameters', x, y1)

            plt.tight_layout()
            st.pyplot(fig)

        # Case1.2: x == Date ->Liniendiagramm
        else:

            # Zeitreihe Plot 2 (Liniendiagramm)
            agg_func = df_choice.groupby('x').mean if operation == 'Average' else df_choice.groupby('x').sum
            agg_data = agg_func().reset_index()

            fig, ax = plt.subplots(figsize=(15,6))
            plot_line(agg_data, 'x', 'y1', ax, 'Analysis of the desired parameters', 'Years', y1)

            plt.tight_layout()
            st.pyplot(fig)

            # Zeitreihe Plot 2 (Liniendiagramm nach Monaten mit 1 Linie pro Jahr)
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
            agg_func = df_datetime.groupby(['Year', 'Month']).mean if operation == 'Average' else df_datetime.groupby(['Year', 'Month']).sum
            datetime_aggregated = agg_func({'Weekly_Sales': 'mean' if operation == 'Average' else 'sum'}).reset_index()


            # Plot erstellen
            sns.lineplot(data=datetime_aggregated, x='Month', y='Weekly_Sales', ax=ax2, hue='Year', palette=color_palette_3)
            ax2.set_title('Analysis of the desired parameters', fontsize = fontsize_title)
            ax2.set_xlabel('Months', fontsize = fontsize_axes)
            ax2.set_ylabel(y1, fontsize = fontsize_axes)
            ax2.grid(True,linestyle='-')

            plt.tight_layout()
            st.pyplot(fig2)


            # Liniendiagramm nach Wochen
            fig3, ax1 = plt.subplots(figsize=(15,6))

            # Data Frame mit Jahren, Wochen, Monaten und Weekly_Sales erstellen
            df_datetime = pd.DataFrame({
                'Date': merge_train['Date'],
                'Year': merge_train['Date'].dt.year, 
                'Month': merge_train['Date'].dt.month,
                'Week': merge_train['Date'].dt.isocalendar().week,
                'Day':merge_train['Date'].dt.day,
                'Weekly_Sales': merge_train['Weekly_Sales']
            })

            # Wähle die Aggregationsfunktion
            agg_func = df_datetime.groupby(['Year', 'Month','Week']).mean if operation == 'Average' else df_datetime.groupby(['Year', 'Month','Week']).sum
            datetime_aggregated = agg_func({'Weekly_Sales': 'mean' if operation == 'Average' else 'sum'}).reset_index()

            # Plot erstellen
            sns.lineplot(data=datetime_aggregated, x='Week', y='Weekly_Sales', ax=ax1, hue='Year', palette=color_palette_3)
            ax1.set_title('Analysis of the desired parameters', fontsize = fontsize_title)
            ax1.set_xlabel('Weeks', fontsize = fontsize_axes)
            ax1.set_ylabel(y1, fontsize = fontsize_axes)
            ax1.grid(True, linestyle='-')

            # Schrittweite der x-Achse auf 5er-Schritte setzen mit xticks
            weeks = datetime_aggregated['Week'].unique()
            ax1.set_xticks(range(min(weeks), max(weeks) + 1, 1))

            plt.tight_layout()
            st.pyplot(fig3)
      


    # Case 2: 2 Achsen, var1 oder var2 sind Weekly Sales
    if (y1 == 'Weekly_Sales' or y2 == 'Weekly_Sales') and y2 is not None and x == 'Date':

        # Temporärer DataFrame für die getätigte Auswahl in der App
        df_choice = pd.DataFrame({
            'Date': merge_train[x],   # Variable für die x-Achse
            'Year': merge_train['Date'].dt.year,
            'Month': merge_train['Date'].dt.month,
            'Week': merge_train['Date'].dt.isocalendar().week,
            'y1': merge_train[y1],    # Variable für die y1-Achse
            'y2': merge_train[y2],    # Variable für die y2-Achse
            'Type': merge_train['Type']
        })

        # Wähle die Aggregationsfunktion
        if operation == 'Average':
            df_choice_aggregated_c2_1 = df_choice.groupby(['Year', 'Month']).agg({'y1': 'mean', 'y2':'mean'}).reset_index()
            df_choice_aggregated_c2_1_date = df_choice.groupby('Date').agg({'y1': 'mean', 'y2':'mean'}).reset_index()
        elif operation == 'Sum':
            df_choice_aggregated_c2_1 = df_choice.groupby(['Year', 'Month']).agg({'y1': 'sum', 'y2':'sum'}).reset_index()
            df_choice_aggregated_c2_1_date = df_choice.groupby('Date').agg({'y1': 'sum', 'y2':'sum'}).reset_index()

        # Plot 1: Lineplot auf Jahresbasis
        if y1 == 'Weekly_Sales' and y2 not in ['Type', 'Size', 'Dept']:
            fig, ax1 = plt.subplots(figsize=(15,6))  

            # Zeichne y1 (Weekly Sales)
            sns.lineplot(x='Date', y='y1', data=df_choice_aggregated_c2_1_date, color=color_palette_2[0], ax=ax1, label=y1)
            ax1.set_title("Analysis of the desired parameters", fontsize=fontsize_title)
            ax1.set_ylabel(y1, fontsize=fontsize_axes)
            ax1.set_xlabel('Year', fontsize=fontsize_axes)  # 'Date' als Label
            ax1.legend(loc='upper left')
            ax1.grid(True, linestyle='-')

            # Zweite y-Achse für y2
            ax2 = ax1.twinx()
            sns.lineplot(x='Date', y='y2', data=df_choice_aggregated_c2_1_date, color=color_palette_2[1], ax=ax2, label=y2)
            ax2.set_ylabel(y2, fontsize=fontsize_axes)
            ax2.legend(loc='upper right')

            plt.tight_layout()
            st.pyplot(fig)

            # Plot 2: Lineplot auf Monatsbasis
            fig, ax1 = plt.subplots(figsize=(15,6))

            # Zeichne y1 (Monatsbasis)
            sns.lineplot(x='Month', y='y1', data=df_choice_aggregated_c2_1, hue='Year', palette=color_palette_3, ax=ax1)
            ax1.set_title("Analysis of the desired parameters", fontsize=fontsize_title)
            ax1.set_ylabel(y1, fontsize=fontsize_axes)
            ax1.set_xlabel('Month', fontsize=fontsize_axes)
            ax1.legend(loc='upper left')
            ax1.grid(True, linestyle='-')

            # Zweite y-Achse für y2
            ax2 = ax1.twinx()
            sns.lineplot(x='Month', y='y2', data=df_choice_aggregated_c2_1, hue='Year', palette='Wistia', ax=ax2)
            ax2.set_ylabel(y2, fontsize=fontsize_axes)
            ax2.legend(loc='upper right')

            plt.tight_layout()
            st.pyplot(fig)

        # Case: Wenn y2 gleich Weekly_Sales ist
        elif y2 == 'Weekly_Sales' and y1 not in ['Type', 'Size', 'Dept']:
            fig, ax1 = plt.subplots(figsize=(15,6))  

            sns.lineplot(x='Date', y='y1', data=df_choice_aggregated_c2_1_date, color=color_palette_2[0], ax=ax1, label=y1)
            ax1.set_title("Analysis of the desired parameters", fontsize=fontsize_title)
            ax1.set_ylabel(y1, fontsize=fontsize_axes)
            ax1.set_xlabel('Date', fontsize=fontsize_axes)
            ax1.legend(loc='upper left')
            ax1.grid(True, linestyle='-')

            ax2 = ax1.twinx()
            sns.lineplot(x='Date', y='y2', data=df_choice_aggregated_c2_1_date, color=color_palette_2[1], ax=ax2, label=y2)
            ax2.set_ylabel(y2, fontsize=fontsize_axes)
            ax2.legend(loc='upper right')

            plt.tight_layout()
            st.pyplot(fig)

        # Falls die x-Achse nicht 'Date' ist und y1/y2 gleich 'Weekly_Sales' ist
        elif (y1 == 'Weekly_Sales' or y2 == 'Weekly_Sales') and x != 'Date' and not (y1 == 'Size' or y2 == 'Size'):
            st.write("Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!")






       




    # Case3: 1 Achse, var1 ist nicht weekly sales

    elif y1 != 'Weekly_Sales' and y2 == None:
            
        # Case3.2: y1 == Store 

        if y1 == 'Store' and x == 'Size':
            st.write("Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!")
            '''
            # Barchart Stores, Size, Typen
        
            plt.subplots(figsize=(15,6))
            sns.barplot(x='Store', y='Size', data=merge_train, hue='Type', palette=color_palette_3, order=merge_train.sort_values('Size')['Store'].tolist())
            plt.title('Größe der Stores', fontsize=fontsize_title)
            plt.xlabel(fontsize=fontsize_axes)
            plt.ylabel(fontsize=fontsize_axes)
            plt.tight_layout()
            st.pyplot(fig)
            '''

            '''
            # Barchart Store, Weekly_Sales
       
            # Wähle die Aggregationsfunktion
            if operation == 'Average':
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
            '''


        # Case 3.3: y1 == Dept 

        
        if y1 == 'Dept':
            st.write("Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!")
            '''   
            # Wähle die Aggregationsfunktion
            if operation == 'Average':
                agg_data_c3_3 = merge_train.groupby('Dept')['Weekly_Sales'].mean().reset_index()
            else:
                agg_data_c3_3 = merge_train.groupby('Dept')['Weekly_Sales'].sum().reset_index()

            # Barplot zeichnen und beschriften
     

            ax, fig = plt.subplots(figsize=(15,6))
            plt.style.use('default')
            sns.barplot(x='Dept', y='Stores',data=agg_data_c3_3, palette='cool', ax=ax)
            plt.grid(True)
            plt.title('Gewünschte Auswertung', fontsize=18)
            plt.ylabel('Sales', fontsize=16)
            plt.xlabel('Departments', fontsize=16)
            st.pyplot(fig)
        '''


        # Case 3.4: y1 == Temperatur 
        if y1 == 'Temperature':

            if x == 'Date':
            
                df_c3_4 = pd.DataFrame({'Date':merge_train['Date'],
                                        'Year':merge_train['Date'].dt.year, 
                                        'Month':merge_train['Date'].dt.month,
                                        'Week':merge_train['Date'].dt.isocalendar().week,
                                        'Temperature':merge_train['Temperature']})
                    
                    
                # Wähle die Aggregationsfunktion
                if operation == 'Average':
                    temperatur_aggregated_c3_4 = df_c3_4.groupby(['Year', 'Month']).agg({'Temperature': 'mean'}).reset_index()
                    temperatur_c3_4 = df_c3_4.groupby('Date').agg({'Temperature': 'mean'}).reset_index()
                else:
                    temperatur_aggregated_c3_4 = df_c3_4.groupby(['Year', 'Month']).agg({'Temperature': 'sum'}).reset_index()
                    temperatur_c3_4 = df_c3_4.groupby('Date').agg({'Temperature': 'sum'}).reset_index()

                    
                # Zeichne Liniendiagramm nach Monaten
       

                # Erstelle eine Figur und Achse
                fig, ax = plt.subplots(figsize=(15,6))

                sns.lineplot(x='Month', y='Temperature', hue='Year', data=temperatur_aggregated_c3_4, palette=color_palette_3,ax=ax)

                # Setze Titel und Achsenbeschriftungen und Raster
                ax.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
                ax.set_xlabel('Months', fontsize=fontsize_axes)
                ax.set_ylabel('Temperature', fontsize=fontsize_axes)
                ax.grid(True, linestyle='-', alpha=0.7)
                plt.tight_layout()
                st.pyplot(fig)


                # Lineplot erstellen auf Jahresbasis
    
                fig2, ax2 = plt.subplots(figsize=(15,6))
                sns.lineplot(x='Date', y='Temperature', data=temperatur_c3_4, color=color_palette_1[0])
                ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
                ax2.set_xlabel('Years', fontsize=fontsize_axes)
                ax2.set_ylabel('Temperature', fontsize=fontsize_axes)
                ax2.grid(True,linestyle='-', alpha=0.7)

                # Trendlinie hinzufügen
                plt.tight_layout()

                st.pyplot(fig2)

            elif x != 'Date':
                st.write('Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!')





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
            if operation == 'Average':
                cpi_aggregated_c3_5 = df_c3_5.groupby(['Year', 'Month']).agg({'CPI': 'mean'}).reset_index()
                cpi_aggregated_c3_5_date = df_c3_5.groupby('Date').agg({'CPI': 'mean'}).reset_index()
            else:
                cpi_aggregated_c3_5 = df_c3_5.groupby(['Year', 'Month']).agg({'CPI': 'sum'}).reset_index()
                cpi_aggregated_c3_5_date = df_c3_5.groupby('Date').agg({'CPI': 'sum'}).reset_index()

            # Zeichne Liniendiagramm nach Monaten
   

            # Erstelle eine Figur und Achse
            fig1, ax1 = plt.subplots(figsize=(15,6))

            # Zeichne das Liniendiagramm
            sns.lineplot(x='Month', y='CPI', hue='Year', data=cpi_aggregated_c3_5, palette=color_palette_3, ax=ax1)

            # Setze Titel und Achsenbeschriftungen 
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.set_xlabel('Months', fontsize=fontsize_axes)
            ax1.set_ylabel('CPI', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')

            # Layout anpassen und Plot anzeigen
            plt.tight_layout()
            st.pyplot(fig1)

            # Lineplot erstellen auf Jahresbasis

            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='CPI', data=cpi_aggregated_c3_5_date, color=color_palette_1[0])
            ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax2.set_xlabel('Years', fontsize=fontsize_axes)
            ax2.set_ylabel('CPI', fontsize=fontsize_axes)
            ax2.grid(True,linestyle='-', alpha=0.7)

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
            if operation == 'Average':
                unemployment_aggregated_c3_6 = df_c3_6.groupby(['Year', 'Month']).agg({'Unemployment': 'mean'}).reset_index()
                unemployment_aggregated_c3_6_date = df_c3_6.groupby('Date').agg({'Unemployment': 'mean'}).reset_index()
            else:
                unemployment_aggregated_c3_6 = df_c3_6.groupby(['Year', 'Month']).agg({'Unemployment': 'sum'}).reset_index()
                unemployment_aggregated_c3_6_date = df_c3_6.groupby('Date').agg({'Unemployment': 'sum'}).reset_index()


            # Zeichne Liniendiagramm nach Monaten
 

            # Erstelle eine Figur und Achse
            fig, ax = plt.subplots(figsize=(15,6))

            sns.lineplot(x='Month', y='Unemployment', hue='Year', data=unemployment_aggregated_c3_6, palette=color_palette_3,ax=ax)

            # Setze Titel und Achsenbeschriftungen 
            ax.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax.set_xlabel('Months', fontsize=fontsize_axes)
            ax.set_ylabel('Unemployment', fontsize=fontsize_axes)
            ax.grid(True, linestyle='-')

            # Layout anpassen und Plots anzeigen
            plt.tight_layout()
            st.pyplot(fig)


            # Lineplot erstellen auf Jahresbasis
       
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Unemployment', data=unemployment_aggregated_c3_6_date, palette=color_palette_1[0])
            ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax2.set_xlabel('Years', fontsize=fontsize_axes)
            ax2.set_ylabel('Unemployment', fontsize=fontsize_axes)
            ax2.grid(True,linestyle='-', alpha=0.7)
            plt.tight_layout()
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

            if operation == 'Average':
                isholiday_aggregated_c3_7 = df_c3_7.groupby(['Year', 'Month']).agg({'IsHoliday': 'mean'}).reset_index()
                isholiday_aggregated_date_c3_7 = df_c3_7.groupby('Date').agg({'IsHoliday': 'mean'}).reset_index()
            elif operation == 'Sum':
                isholiday_aggregated_c3_7 = df_c3_7.groupby(['Year', 'Month']).agg({'IsHoliday': 'sum'}).reset_index()
                isholiday_aggregated_date_c3_7 = df_c3_7.groupby('Date').agg({'IsHoliday': 'sum'}).reset_index()
            

            # Erstelle eine Figur und Achse
            fig, ax = plt.subplots(figsize=(15,6))

            # Lineplot anstelle von Stemplot
 

            # Erstelle den Lineplot
            sns.lineplot(x='Month', y='IsHoliday', data=isholiday_aggregated_c3_7, ax=ax, palette=color_palette_3, hue='Year')

            # Setze Titel und Achsenbeschriftungen
            ax.set_title('Analysis of the desired parameters ', fontsize=fontsize_title)
            ax.set_xlabel('Months', fontsize=fontsize_axes)
            ax.set_ylabel('Holidays', fontsize=fontsize_axes)
            ax.grid(True,linestyle='-')

            # Zeige das Diagramm
            plt.tight_layout()
            st.pyplot(fig)



            # Stemplot erstellen auf Jahresbasis

            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='IsHoliday', data=isholiday_aggregated_date_c3_7, palette=color_palette_1)
            ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax2.set_xlabel('Years', fontsize=fontsize_axes)
            ax2.set_ylabel('Holidays', fontsize=fontsize_axes)
            ax2.grid(True,linestyle='-', alpha=0.7)
            plt.tight_layout()
            st.pyplot(fig2)

        elif y1 == 'IsHoliday' and x != 'Date':
            st.write('Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!')




        # Case 3.8: y1 == Size  
        if y1 == 'Size' and x == 'Store':

     
            # Barplot Size, Store, Type
        

            fig,ax = plt.subplots(figsize=(15,6))
            sns.barplot(x='Store',y='Size',data=merge_train,hue=merge_train['Type'], palette=color_palette_4,order=merge_train.sort_values('Size')['Store'].tolist())
            ax.set_title('Analysis of the desired parameters',fontsize=fontsize_title)
            ax.set_xlabel('Stores', fontsize=fontsize_axes)
            ax.set_ylabel('Size', fontsize=fontsize_axes)
            ax.grid(True,linestyle='-')
            plt.tight_layout()
            st.pyplot(fig)

        elif y1 == 'Size' and x != 'Store':
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

            # Wähle die Aggregationsfunktion 
            if operation == 'Average':
                fuelprice_aggregated_c3_9_1 = df_c3_9.groupby(['Date']).agg({'Fuel_Price': 'mean'}).reset_index() 
                fuelprice_aggregated_c3_9_2 = df_c3_9.groupby(['Year', 'Month']).agg({'Fuel_Price': 'mean'}).reset_index()  
            else:
                fuelprice_aggregated_c3_9_1 = df_c3_9.groupby(['Date']).agg({'Fuel_Price': 'sum'}).reset_index() 
                fuelprice_aggregated_c3_9_2 = df_c3_9.groupby(['Year', 'Month']).agg({'Fuel_Price': 'sum'}).reset_index()  

           
           # Zeichne Liniendiagramm nach Monaten
       
            fig, ax = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='Fuel_Price', hue='Year', data=fuelprice_aggregated_c3_9_2, palette=color_palette_3, ax=ax)
            ax.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax.set_xlabel('Months', fontsize=fontsize_axes)
            ax.set_ylabel('Fuel Price', fontsize=fontsize_axes)
            plt.tight_layout()
            ax.grid(True,linestyle='-')
            st.pyplot(fig)  
           
            # Zeichne Liniendiagramm nach Jahren
  
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Fuel_Price', data=fuelprice_aggregated_c3_9_1, ax=ax1,color=color_palette_1[0])
            ax1.set_title('Auswertung gewünschter Parameter', fontsize=fontsize_title)
            ax1.set_xlabel('Years', fontsize=fontsize_axes)
            ax1.set_ylabel('Fuel Price', fontsize=fontsize_axes)
            plt.tight_layout()
            st.pyplot(fig1)  # Zeige das erste Diagramm

            

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
            
            # Wähle die Aggregationsfunktion 
            if operation == 'Average':
                MD1_aggregated_c3_10_date = df_c3_10.groupby(['Date']).agg({'MarkDown1': 'mean'}).reset_index() 
                MD1_aggregated_c3_10 = df_c3_10.groupby(['Year', 'Month']).agg({'MarkDown1': 'mean'}).reset_index()  
            else:
                MD1_aggregated_c3_10_date = df_c3_10.groupby(['Date']).agg({'MarkDown1': 'sum'}).reset_index() 
                MD1_aggregated_c3_10 = df_c3_10.groupby(['Year', 'Month']).agg({'MarkDown1': 'sum'}).reset_index()


            # Erstelle das Diagramm1 - Nur MarkDown1 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown1', hue='Year', data=MD1_aggregated_c3_10, palette=color_palette_3, ax=ax1)
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.set_xlabel('Months', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown1', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            
            # Erstelle Diagramm 2 - MarkDown1 im Jahresverlauf
            
          
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='MarkDown1', data=MD1_aggregated_c3_10_date, ax=ax2, palette=color_palette_1)
            ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax2.set_xlabel('Years', fontsize=fontsize_axes)
            ax2.set_ylabel('MarkDown1', fontsize=fontsize_axes)
            plt.tight_layout()
            ax2.grid(True,linestyle='-')
            st.pyplot(fig2)  

            
            if operation == 'Average':
                df_c3_10_agg = df_c3_10.groupby('Date').agg({
                    'MarkDown1': 'mean',
                    'MarkDown2': 'mean',
                    'MarkDown3': 'mean',
                    'MarkDown4': 'mean',
                    'MarkDown5': 'mean'
                }).reset_index()
            else:
                df_c3_10_agg = df_c3_10.groupby('Date').agg({
                    'MarkDown1': 'sum',
                    'MarkDown2': 'sum',
                    'MarkDown3': 'sum',
                    'MarkDown4': 'sum',
                    'MarkDown5': 'sum'
                }).reset_index()

            # Bereite Daten für Diagramm2 vor - Alle MarkDowns im Jahresverlauf
            df_c3_10_long = df_c3_10_agg.melt(id_vars=['Date'], 
                                            value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                            var_name='MarkDown', 
                                            value_name='Value')

            # Erstelle Diagramm2 - Alle MarkDowns im Jahresverlauf
            fig3, ax3 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_10_long, palette='cool', ax=ax3)
            ax3.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax3.set_xlabel('Years', fontsize=fontsize_axes)
            ax3.set_ylabel('MarkDowns 1-5', fontsize=fontsize_axes)
            ax3.grid(True,linestyle='-')
            plt.tight_layout()

            # Zeige Diagramm2 an
            st.pyplot(fig3)

        elif y1 == 'MarkDown1' and x != 'Date':
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
            
            # Wähle die Aggregationsfunktion 
            if operation == 'Average':
                MD2_aggregated_c3_11_date = df_c3_11.groupby(['Date']).agg({'MarkDown2': 'mean'}).reset_index() 
                MD2_aggregated_c3_11 = df_c3_11.groupby(['Year', 'Month']).agg({'MarkDown2': 'mean'}).reset_index()  
            else:
                MD2_aggregated_c3_11_date = df_c3_11.groupby(['Date']).agg({'MarkDown2': 'sum'}).reset_index() 
                MD2_aggregated_c3_11 = df_c3_11.groupby(['Year', 'Month']).agg({'MarkDown2': 'sum'}).reset_index()


            # Erstelle das Diagramm1 - Nur MarkDown2 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown2', hue='Year', data=MD2_aggregated_c3_11, palette=color_palette_3, ax=ax1)
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.set_xlabel('Months', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown2', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            
            # Erstelle Diagramm 2 - MarkDown2 im Jahresverlauf
        
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='MarkDown2', data=MD2_aggregated_c3_11_date, ax=ax2, palette=color_palette_1)
            ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax2.set_xlabel('Years', fontsize=fontsize_axes)
            ax2.set_ylabel('MarkDown2', fontsize=fontsize_axes)
            plt.tight_layout()
            ax2.grid(True,linestyle='-')
            st.pyplot(fig2)  

            
            if operation == 'Average':
                df_c3_11_agg = df_c3_11.groupby('Date').agg({
                    'MarkDown1': 'mean',
                    'MarkDown2': 'mean',
                    'MarkDown3': 'mean',
                    'MarkDown4': 'mean',
                    'MarkDown5': 'mean'
                }).reset_index()
            else:
                df_c3_11_agg = df_c3_11.groupby('Date').agg({
                    'MarkDown1': 'sum',
                    'MarkDown2': 'sum',
                    'MarkDown3': 'sum',
                    'MarkDown4': 'sum',
                    'MarkDown5': 'sum'
                }).reset_index()

            # Bereite Daten für Diagramm2 vor - Alle MarkDowns im Jahresverlauf
            df_c3_11_long = df_c3_11_agg.melt(id_vars=['Date'], 
                                            value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                            var_name='MarkDown', 
                                            value_name='Value')

            # Erstelle Diagramm2 - Alle MarkDowns im Jahresverlauf
            fig3, ax3 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_11_long, palette='cool', ax=ax3)
            ax3.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax3.set_xlabel('Years', fontsize=fontsize_axes)
            ax3.set_ylabel('MarkDowns 1-5', fontsize=fontsize_axes)
            ax3.grid(True,linestyle='-')
            plt.tight_layout()

            # Zeige Diagramm2 an
            st.pyplot(fig3)

        elif y1 == 'MarkDown2' and x != 'Date':
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
            
            # Wähle die Aggregationsfunktion 
            if operation == 'Average':
                MD3_aggregated_c3_12_date = df_c3_12.groupby(['Date']).agg({'MarkDown3': 'mean'}).reset_index() 
                MD3_aggregated_c3_12 = df_c3_12.groupby(['Year', 'Month']).agg({'MarkDown3': 'mean'}).reset_index()  
            else:
                MD3_aggregated_c3_12_date = df_c3_12.groupby(['Date']).agg({'MarkDown3': 'sum'}).reset_index() 
                MD3_aggregated_c3_12 = df_c3_12.groupby(['Year', 'Month']).agg({'MarkDown3': 'sum'}).reset_index()


            # Erstelle das Diagramm1 - Nur MarkDown3 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown3', hue='Year', data=MD3_aggregated_c3_12, palette=color_palette_3, ax=ax1)
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.set_xlabel('Months', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown3', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            
            # Erstelle Diagramm 2 - MarkDown3 im Jahresverlauf
            
    
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='MarkDown3', data=MD3_aggregated_c3_12_date, ax=ax2, palette=color_palette_1)
            ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax2.set_xlabel('Years', fontsize=fontsize_axes)
            ax2.set_ylabel('MarkDown3', fontsize=fontsize_axes)
            plt.tight_layout()
            ax2.grid(True,linestyle='-')
            st.pyplot(fig2)  

            
            if operation == 'Average':
                df_c3_12_agg = df_c3_12.groupby('Date').agg({
                    'MarkDown1': 'mean',
                    'MarkDown2': 'mean',
                    'MarkDown3': 'mean',
                    'MarkDown4': 'mean',
                    'MarkDown5': 'mean'
                }).reset_index()
            else:
                df_c3_12_agg = df_c3_12.groupby('Date').agg({
                    'MarkDown1': 'sum',
                    'MarkDown2': 'sum',
                    'MarkDown3': 'sum',
                    'MarkDown4': 'sum',
                    'MarkDown5': 'sum'
                }).reset_index()

            # Bereite Daten für Diagramm2 vor - Alle MarkDowns im Jahresverlauf
            df_c3_12_long = df_c3_12_agg.melt(id_vars=['Date'], 
                                            value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                            var_name='MarkDown', 
                                            value_name='Value')

            # Erstelle Diagramm2 - Alle MarkDowns im Jahresverlauf
            fig3, ax3 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_12_long, palette='cool', ax=ax3)
            ax3.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax3.set_xlabel('Years', fontsize=fontsize_axes)
            ax3.set_ylabel('MarkDowns 1-5', fontsize=fontsize_axes)
            ax3.grid(True,linestyle='-')
            plt.tight_layout()

            # Zeige Diagramm2 an
            st.pyplot(fig3)

        elif y1 == 'MarkDown3' and x != 'Date':
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
            
            # Wähle die Aggregationsfunktion 
            if operation == 'Average':
                MD4_aggregated_c3_13_date = df_c3_13.groupby(['Date']).agg({'MarkDown4': 'mean'}).reset_index() 
                MD4_aggregated_c3_13 = df_c3_13.groupby(['Year', 'Month']).agg({'MarkDown4': 'mean'}).reset_index()  
            else:
                MD4_aggregated_c3_13_date = df_c3_13.groupby(['Date']).agg({'MarkDown4': 'sum'}).reset_index() 
                MD4_aggregated_c3_13 = df_c3_13.groupby(['Year', 'Month']).agg({'MarkDown4': 'sum'}).reset_index()


            # Erstelle das Diagramm1 - Nur MarkDown4 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown4', hue='Year', data=MD4_aggregated_c3_13, palette=color_palette_3, ax=ax1)
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.set_xlabel('Months', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown4', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            
            # Erstelle Diagramm 2 - MarkDown4 im Jahresverlauf
      
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='MarkDown4', data=MD4_aggregated_c3_13_date, ax=ax2, palette=color_palette_1)
            ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax2.set_xlabel('Years', fontsize=fontsize_axes)
            ax2.set_ylabel('MarkDown4', fontsize=fontsize_axes)
            plt.tight_layout()
            ax2.grid(True,linestyle='-')
            st.pyplot(fig2)  

            
            if operation == 'Average':
                df_c3_13_agg = df_c3_13.groupby('Date').agg({
                    'MarkDown1': 'mean',
                    'MarkDown2': 'mean',
                    'MarkDown3': 'mean',
                    'MarkDown4': 'mean',
                    'MarkDown5': 'mean'
                }).reset_index()
            else:
                df_c3_13_agg = df_c3_13.groupby('Date').agg({
                    'MarkDown1': 'sum',
                    'MarkDown2': 'sum',
                    'MarkDown3': 'sum',
                    'MarkDown4': 'sum',
                    'MarkDown5': 'sum'
                }).reset_index()

            # Bereite Daten für Diagramm2 vor - Alle MarkDowns im Jahresverlauf
            df_c3_13_long = df_c3_13_agg.melt(id_vars=['Date'], 
                                            value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                            var_name='MarkDown', 
                                            value_name='Value')

            # Erstelle Diagramm2 - Alle MarkDowns im Jahresverlauf
            fig3, ax3 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_13_long, palette='cool', ax=ax3)
            ax3.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax3.set_xlabel('Years', fontsize=fontsize_axes)
            ax3.set_ylabel('MarkDowns 1-5', fontsize=fontsize_axes)
            ax3.grid(True,linestyle='-')
            plt.tight_layout()

            # Zeige Diagramm2 an
            st.pyplot(fig3)

        elif y1 == 'MarkDown4' and x != 'Date':
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
            
            # Wähle die Aggregationsfunktion 
            if operation == 'Average':
                MD5_aggregated_c3_14_date = df_c3_14.groupby(['Date']).agg({'MarkDown5': 'mean'}).reset_index() 
                MD5_aggregated_c3_14 = df_c3_14.groupby(['Year', 'Month']).agg({'MarkDown5': 'mean'}).reset_index()  
            else:
                MD5_aggregated_c3_14_date = df_c3_14.groupby(['Date']).agg({'MarkDown5': 'sum'}).reset_index() 
                MD5_aggregated_c3_14 = df_c3_14.groupby(['Year', 'Month']).agg({'MarkDown5': 'sum'}).reset_index()


            # Erstelle das Diagramm1 - Nur MarkDown5 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown5', hue='Year', data=MD5_aggregated_c3_14, palette=color_palette_3, ax=ax1)
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.set_xlabel('Months', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown5', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            
            # Erstelle Diagramm 2 - MarkDown5 im Jahresverlauf
            
           
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='MarkDown5', data=MD5_aggregated_c3_14_date, ax=ax2, palette=color_palette_1)
            ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax2.set_xlabel('Years', fontsize=fontsize_axes)
            ax2.set_ylabel('MarkDown5', fontsize=fontsize_axes)
            plt.tight_layout()
            ax2.grid(True,linestyle='-')
            st.pyplot(fig2)  

            
            if operation == 'Average':
                df_c3_14_agg = df_c3_14.groupby('Date').agg({
                    'MarkDown1': 'mean',
                    'MarkDown2': 'mean',
                    'MarkDown3': 'mean',
                    'MarkDown4': 'mean',
                    'MarkDown5': 'mean'
                }).reset_index()
            else:
                df_c3_14_agg = df_c3_14.groupby('Date').agg({
                    'MarkDown1': 'sum',
                    'MarkDown2': 'sum',
                    'MarkDown3': 'sum',
                    'MarkDown4': 'sum',
                    'MarkDown5': 'sum'
                }).reset_index()

            # Bereite Daten für Diagramm2 vor - Alle MarkDowns im Jahresverlauf
            df_c3_14_long = df_c3_14_agg.melt(id_vars=['Date'], 
                                            value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                            var_name='MarkDown', 
                                            value_name='Value')

            # Erstelle Diagramm2 - Alle MarkDowns im Jahresverlauf
            fig3, ax3 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_14_long, palette='cool', ax=ax3)
            ax3.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax3.set_xlabel('Years', fontsize=fontsize_axes)
            ax3.set_ylabel('MarkDowns 1-5', fontsize=fontsize_axes)
            ax3.grid(True,linestyle='-')
            plt.tight_layout()

            # Zeige Diagramm2 an
            st.pyplot(fig3)

        elif y1 == 'MarkDown5' and x != 'Date':
            st.write('Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!')





    # Case4: 2 y-Achsen, var1 und var2 sind nicht weekly sales
    if y1 != 'Weekly_Sales' and y2 != 'Weekly_Sales' and x == 'Date' and y2 is not None:
        
        # DataFrame erstellen
        df_c4 = pd.DataFrame({
            'Date': merge_train['Date'],
            'Year': merge_train['Date'].dt.year, 
            'Month': merge_train['Date'].dt.month,
            'Week': merge_train['Date'].dt.isocalendar().week,
            y1: merge_train[y1],
            y2: merge_train[y2]
        })

        # Wähle die Aggregationsfunktion
        if operation == 'Average':
            agg_c4_month = df_c4.groupby(['Year', 'Month']).agg({y1: 'mean', y2: 'mean'}).reset_index()
            agg_c4_year = df_c4.groupby('Date').agg({y1: 'mean', y2: 'mean'}).reset_index()
        else:
            agg_c4_month = df_c4.groupby(['Year', 'Month']).agg({y1: 'sum', y2: 'sum'}).reset_index()
            agg_c4_year = df_c4.groupby(['Date']).agg({y1: 'sum', y2: 'sum'}).reset_index()

        if x == 'Date' and (y1 == 'Size' or y1 == 'Type' or y1 == 'Dept' or y2 == 'Size' or y2 == 'Type' or y2 == 'Dept'):
            st.write("Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!")
        
        else:
            # Zeichne Diagramm 1 - Jährliche Übersicht
       
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y=y1, data=agg_c4_year, color='blue', ax=ax1, label=y1)
            ax1.set_ylabel(y1, fontsize=fontsize_axes)
            ax1.set_xlabel('Years', fontsize=fontsize_axes)
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.legend(loc='upper left')
            ax1.grid(True,linestyle='-')

            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()
            sns.lineplot(x='Date', y=y2, data=agg_c4_year, color='red', ax=ax2, label=y2)
            ax2.set_ylabel(y2, fontsize=fontsize_axes)
            ax2.legend(loc='upper right')

            # Layout anpassen und anzeigen
            plt.tight_layout()
            st.pyplot(fig1)

            # Zeichne Diagramm 2 - Monatliche Übersicht
         
            fig2, ax3 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y=y1, data=agg_c4_month, color='blue', ax=ax3, hue='Year', palette=color_palette_3)
            ax3.set_ylabel(y1, fontsize=fontsize_axes)
            ax3.set_xlabel('Months', fontsize=fontsize_axes)
            ax3.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax3.legend(loc='upper left')
            ax3.grid(True,linestyle='-')

            # Erstelle zweite y-Achse für das zweite Diagramm
            ax4 = ax3.twinx()
            sns.lineplot(x='Month', y=y2, data=agg_c4_month, color='red', ax=ax4, hue='Year', palette='Wistia')
            ax4.set_ylabel(y2, fontsize=fontsize_axes)
            ax4.legend(loc='upper right')

            plt.tight_layout()
            st.pyplot(fig2)

    elif y1 != 'Weekly_Sales' and y2 != 'Weekly_Sales' and x != 'Date' and y2 is not None:   
    
        st.write("Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!")



# Korrelationsanalyse
def show_corr():
    merge_train, merge_test = data_preprocessing()

    # Vordefinierte Farbpaletten
    color_palette_1 = ['#FF6C3E']    # 1 Farbe für Diagramm
    color_palette_2 = ['#FF6C3E','#3ED1FF']    # 2 Farben für Diagramm
    color_palette_3 = ['#FF6C3E','#3ED1FF','#70FF3E']    # 3 Farben für Diagramm
    color_palette_4 = ['#FF6C3E','#3ED1FF','#70FF3E','#CD3EFF']    # 4 Farben für Diagramm

    fontsize_title = 20
    fontsize_axes =15
    
    # Erstelle Barplot
    fig1, ax1 = plt.subplots(figsize=(15,6))
    merge_train.corr()['Weekly_Sales'].abs().sort_values()[:-1].plot(kind='bar', ax=ax1, color=color_palette_1)
    ax1.set_title('Correlation Analysis:', fontsize=fontsize_title)
    ax1.set_ylabel('Correlation Coefficients')
    
    # Zeige das Diagramm in Streamlit an
    st.pyplot(fig1)


# Heatmap Store-Department-Weekly_Sales - Kombinationen
def get_store_department_sales_heatmap():
    merge_train, merge_test = data_preprocessing()

    # Berechne die Sum der Weekly_Sales pro Store
    store_sales_summary = merge_train.groupby('Store')['Weekly_Sales'].sum().reset_index()

    # Sortiere Stores nach den Umsätzen
    sorted_stores = store_sales_summary.sort_values('Weekly_Sales', ascending=False)['Store']

    # Store - Department - Weekly_Sales
    pivot_table = merge_train.pivot_table(index='Dept', columns='Store', values='Weekly_Sales', aggfunc='sum')
    pivot_table = pivot_table[sorted_stores]

    fig1, ax1 = plt.subplots(figsize=(120,60))
    sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt=".1f")
    plt.title('Sales Heatmap by Store and Department', fontsize=100)
    plt.xlabel('Store', fontsize=70)
    plt.ylabel('Department', fontsize=70)
    st.pyplot(fig1)

# Heatmap Type-Department-Weekly_Sales - Kombinationen
def get_type_department_sales_heatmap():
    merge_train, merge_test = data_preprocessing()

    # Type - Department - Weekly_Sales
    pivot_table = merge_train.pivot_table(index='Dept', columns='Type', values='Weekly_Sales', aggfunc='sum')


    fig2, ax1 = plt.subplots(figsize=(20,100))
    sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt=".1f")
    plt.title('Sales Heatmap by Type and Department', fontsize=20)
    plt.xlabel('Type', fontsize=15)
    plt.ylabel('Department', fontsize=15)
    st.pyplot(fig2)


# Feiertagsanalyse
def get_holiday():

    # Schriftgrößen
    fontsize_title = 20
    fontsize_axes =15

    # Plot1: Overview over Holidays (Balkendiagramm für jeden Feiertag mit Total Sales)
    image_path=r"C:\Users\mail\OneDrive\Desktop\Privat\Data Science Institut\Abschlussprojekt\Versatile Production System\Daten_Walmart\Github\Final_Project\Final_Project\pictures_Holiday_MarkDown\Holiday_MarkDown_pic1_Overview_Holidays.png"

    st.image(image_path,use_column_width=True)

    '''
    # Vordefinierte Farbpaletten
    colors = ['#FF6C3E', '#3ED1FF', '#70FF3E', '#CD3EFF', '#FFDB3E']  # 5 Farben für 5 Feiertage
    
    # Funktion aus preprocessing.py importieren
    merge_train, merge_test = data_preprocessing()
    
    # Erstelle das Plot-Layout
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
    ax = ax.flatten()  # Um die 2D-Achsen zu einer 1D-Liste zu machen
    
    # Feiertags-Spalten und Farben
    holidays = ['Christmas', 'Labor_Day', 'Super_Bowl', 'Thanksgiving', 'Easter']  # Nur 5 Feiertage
    
    # Für jeden Feiertag eine Balkendarstellung der Weekly_Sales plotten
    for i, holiday in enumerate(holidays):
        # Filtere nach dem aktuellen Feiertag
        holiday_data = merge_train[merge_train[holiday] == 1]
        
        # Zeichne ein Balkendiagramm für Weekly_Sales basierend auf dem Jahr
        holiday_data.groupby('Year')['Weekly_Sales'].sum().plot(kind='bar', ax=ax[i], color=colors[i])
        
        # Setze den Titel des Subplots
        ax[i].set_title(f'{holiday}', fontsize=fontsize_title)
        ax[i].set_xlabel('')
        ax[i].set_ylabel('Sum of Sales', fontsize=fontsize_axes)
    
    # Letztes (leeres) Subplot entfernen, wenn es nur 5 Plots gibt
    fig.delaxes(ax[-1])  # Entfernt die überflüssige Achse, da wir nur 5 Plots benötigen
    
    # Layout anpassen
    plt.tight_layout()

    # Überschrift einfügen
    st.markdown("<h5 style='text-align: center;'>Overview over Holiday Sales</h5>", unsafe_allow_html=True)
    
    # Plot in Streamlit anzeigen
    st.pyplot(fig)
    '''

    # Plot2: 
    image_path=r"C:\Users\mail\OneDrive\Desktop\Privat\Data Science Institut\Abschlussprojekt\Versatile Production System\Daten_Walmart\Github\Final_Project\Final_Project\pictures_Holiday_MarkDown\Holiday_MarkDown_pic2.png"

    st.image(image_path,use_column_width=True)

    '''
    # Schriftgrößen
    fontsize_title = 20
    fontsize_axes = 15

    # Liniendiagramm nach Wochen
    fig, ax1 = plt.subplots(figsize=(15, 6))

    # Data Frame mit Jahren, Wochen, Monaten und Weekly_Sales erstellen
    df_datetime = pd.DataFrame({
        'Date': merge_train['Date'],
        'Year': merge_train['Date'].dt.year,
        'Month': merge_train['Date'].dt.month,
        'Week': merge_train['Date'].dt.isocalendar().week,
        'Day': merge_train['Date'].dt.day,
        'Weekly_Sales': merge_train['Weekly_Sales']
    })

    # Wähle die Aggregationsfunktion und reset den Index
    agg_func = df_datetime.groupby(['Date'])['Weekly_Sales'].mean().reset_index()

    # Plot für die durchschnittlichen Verkäufe erstellen
    sns.lineplot(data=agg_func, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average of Sales', fontsize=fontsize_axes)
    ax1.grid(True, linestyle='-')

    # Feiertagsverkäufe hinzufügen
    holidays = ['Christmas', 'Labor_Day', 'Super_Bowl', 'Thanksgiving', 'Easter']
    colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#FFC300']  # Kräftigere Farbpalette für Feiertage

    # Zweite Y-Achse für die Feiertagsverkäufe
    ax2 = ax1.twinx()

    for i, holiday in enumerate(holidays):
        # Filtere nach dem aktuellen Feiertag
        holiday_data = merge_train[merge_train[holiday] == 1]
        
        # Berechne die durchschnittlichen Verkaufszahlen für den Feiertag
        holiday_sales = holiday_data.groupby('Date')['Weekly_Sales'].mean().reset_index()

        # Füge Balkendiagramm für den Feiertag hinzu mit breiteren Balken
        ax2.bar(holiday_sales['Date'], holiday_sales['Weekly_Sales'], color=colors[i], alpha=0.3, width=10, label=holiday, linestyle='--')

    # Beschriftungen für die zweite Y-Achse
    ax2.set_ylabel('Average of Holiday Sales', fontsize=fontsize_axes)

    # Legend hinzufügen
    ax1.legend(title='Average Weekly Sales', fontsize=fontsize_axes)
    ax2.legend(holidays, title='Holidays', fontsize=fontsize_axes, loc='upper left')

    plt.tight_layout()
    st.pyplot(fig)
    '''


    # Plot3: Alle Markdowns + Feiertage + Weekly_Sales
    image_path=r"C:\Users\mail\OneDrive\Desktop\Privat\Data Science Institut\Abschlussprojekt\Versatile Production System\Daten_Walmart\Github\Final_Project\Final_Project\pictures_Holiday_MarkDown\Holiday_MarkDown_pic3.png"

    st.image(image_path,use_column_width=True)

    '''
    # Schritt 1: DataFrame mit den notwendigen Spalten erstellen
    df_datetime = pd.DataFrame({
        'Date': merge_train['Date'],
        'Weekly_Sales': merge_train['Weekly_Sales'],
        'MarkDown1': merge_train['MarkDown1'],
        'MarkDown2': merge_train['MarkDown2'],
        'MarkDown3': merge_train['MarkDown3'],
        'MarkDown4': merge_train['MarkDown4'],
        'MarkDown5': merge_train['MarkDown5'],
        'IsHoliday': merge_train['IsHoliday']  
    })

    # Schritt 2: Feiertage filtern
    holidays = df_datetime[df_datetime['IsHoliday'] == 1]

    # Schritt 3: Durchschnittliche Weekly_Sales pro Datum berechnen
    agg_df = df_datetime.groupby('Date').agg({
        'Weekly_Sales': 'mean',
        'MarkDown1': 'mean',
        'MarkDown2': 'mean',
        'MarkDown3': 'mean',
        'MarkDown4': 'mean',
        'MarkDown5': 'mean'
    }).reset_index()

    # Schritt 4: DataFrame auf Datumsbereich ab Juli 2011 filtern
    agg_df = agg_df[agg_df['Date'] >= '2011-07-01']

    # Schriftgrößen
    fontsize_title = 20
    fontsize_axes = 15

    # Schritt 5: Plot erstellen
    fig3, ax1 = plt.subplots(figsize=(15, 6))

    # Schritt 6: Durchschnittliche Weekly Sales auf der ersten Y-Achse plotten
    sns.lineplot(data=agg_df, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Average Weekly Sales and Markdowns Over Time', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average Weekly Sales', fontsize=fontsize_axes)
    ax1.grid(True)

    # Schritt 7: MarkDowns auf der zweiten Y-Achse plotten
    ax2 = ax1.twinx()  # Zweite Y-Achse erstellen
    for i in range(1, 6):
        markdown_col = f'MarkDown{i}'
        sns.lineplot(data=agg_df, x='Date', y=markdown_col, ax=ax2, label=markdown_col, alpha=0.6)

    ax2.set_ylabel('Markdowns', fontsize=fontsize_axes)

    # Schritt 8: Feiertage markieren
    for index, row in holidays.iterrows():
        if row['Date'] >= pd.Timestamp('2011-07-01'):  # Feiertage nur anzeigen, wenn sie nach dem Filterdatum liegen
            ax1.axvline(x=row['Date'], color='red', linestyle='--', alpha=0.5)

    # Schritt 9: Legende und Layout anpassen
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    st.pyplot(fig3) 
    '''

    # Plot4: Nur MarkDown1 + Feiertage + Weekly_Sales
    image_path=r"C:\Users\mail\OneDrive\Desktop\Privat\Data Science Institut\Abschlussprojekt\Versatile Production System\Daten_Walmart\Github\Final_Project\Final_Project\pictures_Holiday_MarkDown\Holiday_MarkDown_pic4_MD1.png"

    st.image(image_path,use_column_width=True)

    '''
    # Schritt 1: DataFrame mit den notwendigen Spalten erstellen
    df_datetime = pd.DataFrame({
        'Date': merge_train['Date'],
        'Weekly_Sales': merge_train['Weekly_Sales'],
        'MarkDown1': merge_train['MarkDown1'],
        'IsHoliday': merge_train['IsHoliday']  
    })

    # Schritt 2: Feiertage filtern
    holidays = df_datetime[df_datetime['IsHoliday'] == 1]

    # Schritt 3: Durchschnittliche Weekly_Sales pro Datum berechnen
    agg_df = df_datetime.groupby('Date').agg({
        'Weekly_Sales': 'mean',
        'MarkDown1': 'mean'
    }).reset_index()

    # Schritt 4: DataFrame auf Datumsbereich ab Juli 2011 filtern
    agg_df = agg_df[agg_df['Date'] >= '2011-07-01']

    # Schriftgrößen
    fontsize_title = 20
    fontsize_axes = 15

    # Schritt 5: Plot erstellen
    fig4, ax1 = plt.subplots(figsize=(15, 6))

    # Schritt 6: Durchschnittliche Weekly Sales auf der ersten Y-Achse plotten
    sns.lineplot(data=agg_df, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Average Weekly Sales and MarkDown1 Over Time', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average Weekly Sales', fontsize=fontsize_axes)
    ax1.grid(True)

    # Schritt 7: Nur MarkDown1 auf der zweiten Y-Achse plotten
    ax2 = ax1.twinx()  # Zweite Y-Achse erstellen
    sns.lineplot(data=agg_df, x='Date', y='MarkDown1', ax=ax2, color='orange', label='MarkDown1', alpha=0.6)
    ax2.set_ylabel('MarkDown1', fontsize=fontsize_axes)

    # Schritt 8: Feiertage markieren
    for index, row in holidays.iterrows():
        if row['Date'] >= pd.Timestamp('2011-07-01'):  # Feiertage nur anzeigen, wenn sie nach dem Filterdatum liegen
            ax1.axvline(x=row['Date'], color='red', linestyle='--', alpha=0.5)

    # Schritt 9: Legende und Layout anpassen
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    st.pyplot(fig4)
    '''

    # Plot5: Nur MarkDown2 + Feiertage + Weekly_Sales
    image_path=r"C:\Users\mail\OneDrive\Desktop\Privat\Data Science Institut\Abschlussprojekt\Versatile Production System\Daten_Walmart\Github\Final_Project\Final_Project\pictures_Holiday_MarkDown\Holiday_MarkDown_pic5_MD2.png"

    st.image(image_path,use_column_width=True)

    '''
    # Schritt 1: DataFrame mit den notwendigen Spalten erstellen
    df_datetime = pd.DataFrame({
        'Date': merge_train['Date'],
        'Weekly_Sales': merge_train['Weekly_Sales'],
        'MarkDown2': merge_train['MarkDown2'],
        'IsHoliday': merge_train['IsHoliday']  
    })

    # Schritt 2: Feiertage filtern
    holidays = df_datetime[df_datetime['IsHoliday'] == 1]

    # Schritt 3: Durchschnittliche Weekly_Sales pro Datum berechnen
    agg_df = df_datetime.groupby('Date').agg({
        'Weekly_Sales': 'mean',
        'MarkDown2': 'mean'
    }).reset_index()

    # Schritt 4: DataFrame auf Datumsbereich ab Juli 2011 filtern
    agg_df = agg_df[agg_df['Date'] >= '2011-07-01']

    # Schriftgrößen
    fontsize_title = 20
    fontsize_axes = 15

    # Schritt 5: Plot erstellen
    fig5, ax1 = plt.subplots(figsize=(15, 6))

    # Schritt 6: Durchschnittliche Weekly Sales auf der ersten Y-Achse plotten
    sns.lineplot(data=agg_df, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Average Weekly Sales and MarkDown2 Over Time', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average Weekly Sales', fontsize=fontsize_axes)
    ax1.grid(True)

    # Schritt 7: Nur MarkDown2 auf der zweiten Y-Achse plotten
    ax2 = ax1.twinx()  # Zweite Y-Achse erstellen
    sns.lineplot(data=agg_df, x='Date', y='MarkDown2', ax=ax2, color='orange', label='MarkDown2', alpha=0.6)
    ax2.set_ylabel('MarkDown2', fontsize=fontsize_axes)

    # Schritt 8: Feiertage markieren
    for index, row in holidays.iterrows():
        if row['Date'] >= pd.Timestamp('2011-07-01'):  # Feiertage nur anzeigen, wenn sie nach dem Filterdatum liegen
            ax1.axvline(x=row['Date'], color='red', linestyle='--', alpha=0.5)

    # Schritt 9: Legende und Layout anpassen
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    st.pyplot(fig5) 
    '''

    # Plot6: Nur MarkDown3 + Feiertage + Weekly_Sales
    image_path=r"C:\Users\mail\OneDrive\Desktop\Privat\Data Science Institut\Abschlussprojekt\Versatile Production System\Daten_Walmart\Github\Final_Project\Final_Project\pictures_Holiday_MarkDown\Holiday_MarkDown_pic6_MD3.png"

    st.image(image_path,use_column_width=True)

    '''
    # Schritt 1: DataFrame mit den notwendigen Spalten erstellen
    df_datetime = pd.DataFrame({
        'Date': merge_train['Date'],
        'Weekly_Sales': merge_train['Weekly_Sales'],
        'MarkDown3': merge_train['MarkDown3'],  # Nur MarkDown3 verwenden
        'IsHoliday': merge_train['IsHoliday']  
    })

    # Schritt 2: Feiertage filtern
    holidays = df_datetime[df_datetime['IsHoliday'] == 1]

    # Schritt 3: Durchschnittliche Weekly_Sales pro Datum berechnen
    agg_df = df_datetime.groupby('Date').agg({
        'Weekly_Sales': 'mean',
        'MarkDown3': 'mean'  # Nur MarkDown3 aggregieren
    }).reset_index()

    # Schritt 4: DataFrame auf Datumsbereich ab Juli 2011 filtern
    agg_df = agg_df[agg_df['Date'] >= '2011-07-01']

    # Schriftgrößen
    fontsize_title = 20
    fontsize_axes = 15

    # Schritt 5: Plot erstellen
    fig6, ax1 = plt.subplots(figsize=(15, 6))

    # Schritt 6: Durchschnittliche Weekly Sales auf der ersten Y-Achse plotten
    sns.lineplot(data=agg_df, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Average Weekly Sales and MarkDown3 Over Time', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average Weekly Sales', fontsize=fontsize_axes)
    ax1.grid(True)

    # Schritt 7: Nur MarkDown3 auf der zweiten Y-Achse plotten
    ax2 = ax1.twinx()  # Zweite Y-Achse erstellen
    sns.lineplot(data=agg_df, x='Date', y='MarkDown3', ax=ax2, color='orange', label='MarkDown3', alpha=0.6)
    ax2.set_ylabel('MarkDown3', fontsize=fontsize_axes)

    # Schritt 8: Feiertage markieren
    for index, row in holidays.iterrows():
        if row['Date'] >= pd.Timestamp('2011-07-01'):  # Feiertage nur anzeigen, wenn sie nach dem Filterdatum liegen
            ax1.axvline(x=row['Date'], color='red', linestyle='--', alpha=0.5)

    # Schritt 9: Legende und Layout anpassen
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    st.pyplot(fig6)
    '''

    # Plot7: Nur MarkDown4 + Feiertage + Weekly_Sales
    image_path=r"C:\Users\mail\OneDrive\Desktop\Privat\Data Science Institut\Abschlussprojekt\Versatile Production System\Daten_Walmart\Github\Final_Project\Final_Project\pictures_Holiday_MarkDown\Holiday_MarkDown_pic7_MD4.png"

    st.image(image_path,use_column_width=True)

    '''
    # Schritt 1: DataFrame mit den notwendigen Spalten erstellen
    df_datetime = pd.DataFrame({
        'Date': merge_train['Date'],
        'Weekly_Sales': merge_train['Weekly_Sales'],
        'MarkDown4': merge_train['MarkDown4'],  # MarkDown4 verwenden
        'IsHoliday': merge_train['IsHoliday']  
    })

    # Schritt 2: Feiertage filtern
    holidays = df_datetime[df_datetime['IsHoliday'] == 1]

    # Schritt 3: Durchschnittliche Weekly_Sales pro Datum berechnen
    agg_df = df_datetime.groupby('Date').agg({
        'Weekly_Sales': 'mean',
        'MarkDown4': 'mean'  # MarkDown4 aggregieren
    }).reset_index()

    # Schritt 4: DataFrame auf Datumsbereich ab Juli 2011 filtern
    agg_df = agg_df[agg_df['Date'] >= '2011-07-01']

    # Schriftgrößen
    fontsize_title = 20
    fontsize_axes = 15

    # Schritt 5: Plot erstellen
    fig7, ax1 = plt.subplots(figsize=(15, 6))

    # Schritt 6: Durchschnittliche Weekly Sales auf der ersten Y-Achse plotten
    sns.lineplot(data=agg_df, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Average Weekly Sales and MarkDown4 Over Time', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average Weekly Sales', fontsize=fontsize_axes)
    ax1.grid(True)

    # Schritt 7: Nur MarkDown4 auf der zweiten Y-Achse plotten
    ax2 = ax1.twinx()  # Zweite Y-Achse erstellen
    sns.lineplot(data=agg_df, x='Date', y='MarkDown4', ax=ax2, color='orange', label='MarkDown4', alpha=0.6)
    ax2.set_ylabel('MarkDown4', fontsize=fontsize_axes)

    # Schritt 8: Feiertage markieren
    for index, row in holidays.iterrows():
        if row['Date'] >= pd.Timestamp('2011-07-01'):  # Feiertage nur anzeigen, wenn sie nach dem Filterdatum liegen
            ax1.axvline(x=row['Date'], color='red', linestyle='--', alpha=0.5)

    # Schritt 9: Legende und Layout anpassen
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    st.pyplot(fig7)
    '''

    # Plot8: Nur MarkDown5 + Feiertage + Weekly_Sales
    image_path=r"C:\Users\mail\OneDrive\Desktop\Privat\Data Science Institut\Abschlussprojekt\Versatile Production System\Daten_Walmart\Github\Final_Project\Final_Project\pictures_Holiday_MarkDown\Holiday_MarkDown_pic8_MD5.png"

    st.image(image_path,use_column_width=True)

    '''
    # Schritt 1: DataFrame mit den notwendigen Spalten erstellen
    df_datetime = pd.DataFrame({
        'Date': merge_train['Date'],
        'Weekly_Sales': merge_train['Weekly_Sales'],
        'MarkDown5': merge_train['MarkDown5'],  # MarkDown5 verwenden
        'IsHoliday': merge_train['IsHoliday']  
    })

    # Schritt 2: Feiertage filtern
    holidays = df_datetime[df_datetime['IsHoliday'] == 1]

    # Schritt 3: Durchschnittliche Weekly_Sales pro Datum berechnen
    agg_df = df_datetime.groupby('Date').agg({
        'Weekly_Sales': 'mean',
        'MarkDown5': 'mean'  # MarkDown5 aggregieren
    }).reset_index()

    # Schritt 4: DataFrame auf Datumsbereich ab Juli 2011 filtern
    agg_df = agg_df[agg_df['Date'] >= '2011-07-01']

    # Schriftgrößen
    fontsize_title = 20
    fontsize_axes = 15

    # Schritt 5: Plot erstellen
    fig8, ax1 = plt.subplots(figsize=(15, 6))

    # Schritt 6: Durchschnittliche Weekly Sales auf der ersten Y-Achse plotten
    sns.lineplot(data=agg_df, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Average Weekly Sales and MarkDown5 Over Time', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average Weekly Sales', fontsize=fontsize_axes)
    ax1.grid(True)

    # Schritt 7: Nur MarkDown5 auf der zweiten Y-Achse plotten
    ax2 = ax1.twinx()  # Zweite Y-Achse erstellen
    sns.lineplot(data=agg_df, x='Date', y='MarkDown5', ax=ax2, color='orange', label='MarkDown5', alpha=0.6)
    ax2.set_ylabel('MarkDown5', fontsize=fontsize_axes)

    # Schritt 8: Feiertage markieren
    for index, row in holidays.iterrows():
        if row['Date'] >= pd.Timestamp('2011-07-01'):  # Feiertage nur anzeigen, wenn sie nach dem Filterdatum liegen
            ax1.axvline(x=row['Date'], color='red', linestyle='--', alpha=0.5)

    # Schritt 9: Legende und Layout anpassen
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    st.pyplot(fig8)
    '''
  

  






    
#MarkDownanalyse
def get_markdown():
    # Vordefinierte Farbpaletten
    color_palette_1 = ['#FF6C3E']    # 1 Farbe für Diagramm
    color_palette_2 = ['#FF6C3E','#3ED1FF']    # 2 Farben für Diagramm
    color_palette_3 = ['#FF6C3E','#3ED1FF','#70FF3E']    # 3 Farben für Diagramm
    color_palette_4 = ['#FF6C3E','#3ED1FF','#70FF3E','#CD3EFF']    # 4 Farben für Diagramm

    # Funktion aus preprocessing.py importieren
    merge_train, merge_test = data_preprocessing()
    pass





# Dashboard
def get_dashboard():
   
    st.write("Klicke [hier](https://public.tableau.com/views/DashboardFlughafen-Projekt_neu/Dashboard1?:language=de-DE&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link), um das Dashboard zu öffnen.")


    
    


