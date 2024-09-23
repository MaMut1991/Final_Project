# Funktion für Dashboard; Parameter werden per Auswahlmöglichkeiten in App übergeben
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st
import matplotlib.ticker as mticker
import streamlit.components.v1 as components
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from preprocessing import data_preprocessing



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

    # Vordefinierte Farbpaletten
    color_palette_1 = ['#70FF3E']    # 1 Farbe für Diagramm
    color_palette_2 = ['#70FF3E','#FF6C3E']    # 2 Farben für Diagramm
    color_palette_3 = ['#70FF3E','#FF6C3E','#3ED1FF']    # 3 Farben für Diagramm
    color_palette_4 = ['#70FF3E','#FF6C3E','#3ED1FF','#CD3EFF']    # 4 Farben für Diagramm
    
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
        sns.lineplot(x=x, y=y, hue=hue, data=df, palette=color_palette_1, ax=ax)
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
            agg_func = df_choice.groupby('x').mean if operation == 'Mittelwert' else df_choice.groupby('x').sum
            agg_data = agg_func().reset_index()

            # Zeichne Balkendiagramm
            fig, ax = plt.subplots(figsize=(15,6))
            plot_bar(agg_data, 'x', 'y1', ax, 'Gewünschte Auswertung', x, y1)

            plt.tight_layout()
            st.pyplot(fig)

        # Case1.2: x == Date -> Zeitreihenanalyse per Liniendiagramm
        else:

            # Zeitreihe Plot 2 (Liniendiagramm)
            agg_func = df_choice.groupby('x').mean if operation == 'Mittelwert' else df_choice.groupby('x').sum
            agg_data = agg_func().reset_index()

            fig, ax = plt.subplots(figsize=(15,6))
            plot_line(agg_data, 'x', 'y1', ax, 'Gewünschte Auswertung', x, y1)

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


            # Plot erstellen
            sns.lineplot(data=datetime_aggregated, x='Month', y='Weekly_Sales', ax=ax2, hue='Year', palette=color_palette_3)
            ax2.set_title('Gewünschte Auswertung', fontsize = fontsize_title)
            ax2.set_xlabel(x, fontsize = fontsize_axes)
            ax2.set_ylabel(y1, fontsize = fontsize_axes)
            ax2.grid(True,linestyle='-')

            plt.tight_layout()
            st.pyplot(fig2)




            


    # Case2: 2 Achsen, var1 oder var2 sind weekly sales

    if (y1 == 'Weekly_Sales' or y2 == 'Weekly_Sales') and y2 is not None:
        
        
        # Temporärer DataFrame für die getätigte Auswahl in der App
        df_choice = pd.DataFrame({
            'x': merge_train[x],   # Variable für die x-Achse
            'Year':merge_train['Date'].dt.year,
            'Month': merge_train['Date'].dt.month,
            'Week': merge_train['Date'].dt.isocalendar().week,
            'y1': merge_train[y1], # Variable für die y1-Achse
            'y2': merge_train[y2],  # Variable für die y2-Achse
            'Type':merge_train['Type']
        })

        # Wähle die Aggregationsfunktion
        if operation == 'Mittelwert' and x == 'Date':
            df_choice_aggregated_c2_1 = df_choice.groupby(['Year', 'Month']).agg({'y1': 'mean', 'y2':'mean'}).reset_index()
            df_choice_aggregated_c2_1_date = df_choice.groupby('x').agg({'y1':'mean', 'y2':'mean'}).reset_index()
        elif operation == 'Summe' and x == 'Date':
            df_choice_aggregated_c2_1 = df_choice.groupby(['Year', 'Month']).agg({'y1': 'sum', 'y2':'sum'}).reset_index()
            df_choice_aggregated_c2_1_date = df_choice.groupby('x').agg({'y1':'sum', 'y2':'sum'}).reset_index()


        if y1 == 'Weekly_Sales' and x == 'Date' and y2 not in ['Type', 'Size', 'Dept']:   # Falls y1 gleich Weekly_Sales ist
           
            
            # Plot 1: Lineplot auf Jahresbasis

            # Erstelle Figur und die erste Achse
            fig, ax1 = plt.subplots(figsize=(15,6))  

            sns.lineplot(x='x', y='y1', data=df_choice_aggregated_c2_1_date, color=color_palette_2[0], ax=ax1, label=y1)
            ax1.set_title(f"Auswertung der gewünschten Parameter", fontsize=fontsize_title)
            ax1.set_ylabel(y1, fontsize=fontsize_axes)
            ax1.set_xlabel('Year', fontsize=fontsize_axes)  # 'Date' als Label
            ax1.legend(loc='upper left')
            ax1.grid(True, linestyle='-')
           
            
            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()

                      
            # Zeichne y2 als Linie auf ax2
            sns.lineplot(x='x', y='y2', data=df_choice_aggregated_c2_1_date, color=color_palette_2[1], ax=ax2, label=y2)
            ax2.set_ylabel(y2, fontsize=fontsize_axes)
            ax2.legend(loc='upper right')
            
            
            # Layout anpassen und anzeigen
            plt.tight_layout()
            st.pyplot(fig)



            # Plot 2: Lineplot auf Monatsbasis

            # Erstelle Figur und die erste Achse
            fig, ax1 = plt.subplots(figsize=(15,6))  

            sns.lineplot(x='Month', y='y1', data=df_choice_aggregated_c2_1, palette=color_palette_3, ax=ax1, hue='Year')
            ax1.set_title(f"Auswertung der gewünschten Parameter", fontsize=fontsize_title)
            ax1.set_ylabel(y1, fontsize=fontsize_axes)
            ax1.set_xlabel('Month', fontsize=fontsize_axes)  # 'Month' als Label
            ax1.legend(loc='upper left')
            ax1.grid(True, linestyle='-')
           
            
            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()

                      
            # Zeichne y2 als Linie auf ax2
            sns.lineplot(x='Month', y='y2', data=df_choice_aggregated_c2_1, palette='Wistia', ax=ax2, hue='Year')
            ax2.set_ylabel(y2, fontsize=fontsize_axes)
            ax2.legend(loc='upper right')
            
            
            # Layout anpassen und anzeigen
            plt.tight_layout()
            st.pyplot(fig)



        elif y2 == 'Weekly_Sales' and x == 'Date' and y1 not in ['Type', 'Size', 'Dept']:  # Falls y2 gleich Weekly_Sales ist
     

            # Erstelle Figur und die erste Achse
            fig, ax1 = plt.subplots(figsize=(15,6))  

            sns.lineplot(x='x', y='y1', data=df_choice_aggregated_c2_1_date, color=color_palette_2[0], ax=ax1, label=y1)
            ax1.set_title(f"Auswertung der gewünschten Parameter", fontsize=fontsize_title)
            ax1.set_ylabel(y1, fontsize=fontsize_axes)
            ax1.set_xlabel('Date', fontsize=fontsize_axes)  # 'Date' als Label
            ax1.legend(loc='upper left')
            ax1.grid(True, linestyle='-')
            
            
            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()

                        
            # Zeichne y2 als Linie auf ax2
            sns.lineplot(x='x', y='y2', data=df_choice_aggregated_c2_1_date, color=color_palette_2[1], ax=ax2, label=y2)
            ax2.set_ylabel(y2, fontsize=fontsize_axes)
            ax2.legend(loc='upper right')
            
            
            # Layout anpassen und anzeigen
            plt.tight_layout()
            st.pyplot(fig)



        elif (y1 == 'Weekly_Sales' or y2 == 'Weekly_Sales') and x != 'Date' and not (y1 == 'Size' or y2 == 'Size'):
     
            st.write("Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!")



        elif (y1 == 'Weekly_Sales' or y2 == 'Weekly_Sales') and x != 'Date' and (y1 == 'Size' or y2 == 'Size'):
     

            # Plot 1

            # Erstelle Figur und die erste Achse
            fig1, ax1 = plt.subplots(figsize=(15,6))

            # Zeichne Balkendiagramm (x und y1)

            
            sns.barplot(x='x', y='y1', data=df_choice, color=color_palette_2[0], ax=ax1)
            ax1.set_title(f"Auswertung der gewünschten Parameter", fontsize=fontsize_title)
            ax1.set_ylabel(y1, fontsize=fontsize_axes)
            ax1.set_xlabel(x, fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-', alpha=0.7)
            

            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()

            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                agg_data = df_choice.groupby('x').mean().reset_index()
            else:
                agg_data = df_choice.groupby('x').sum().reset_index()

            # Zeichne y2 als Linie auf ax2
            ax2.plot(ax1.get_xticks(), agg_data['y2'], color=color_palette_4[-1],label=y2)
            ax2.set_ylabel(y2, fontsize=fontsize_axes)
            ax2.legend(loc='upper right')
            

            # Layout anpassen und anzeigen
            plt.tight_layout()
            st.pyplot(fig1)


            # Plot 2

            # Erstelle Figur und die erste Achse
            fig2, ax1 = plt.subplots(figsize=(15,6))

            # Zeichne Balkendiagramm (x und y1)

            sns.barplot(x='x', y='y1', data=df_choice, palette=color_palette_3, ax=ax1, hue='Type')
            ax1.set_title(f"Auswertung der gewünschten Parameter", fontsize=fontsize_title)
            ax1.set_ylabel(y1,fontsize=fontsize_axes)
            ax1.set_xlabel(x, fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-', alpha=0.7)
            

            # Erstelle zweite y-Achse
            ax2 = ax1.twinx()

            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
                agg_data = df_choice.groupby('x').mean().reset_index()
            else:
                agg_data = df_choice.groupby('x').sum().reset_index()

            # Zeichne y2 als Linie auf ax2
            ax2.plot(ax1.get_xticks(), agg_data['y2'], color=color_palette_4[-1],label=y2)
            ax2.set_ylabel(y2, fontsize=fontsize_axes)
            ax2.legend(loc='upper right')
            

            # Layout anpassen und anzeigen
            plt.tight_layout()
            st.pyplot(fig2)



       




    # Case3: 1 Achse, var1 ist nicht weekly sales

    elif y1 != 'Weekly_Sales' and y2 == None:
            
        # Case3.2: y1 == Store 

        if y1 == 'Store' and x == 'Size':
            
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
            '''


        # Case 3.3: y1 == Dept 

        '''
        if y1 == 'Dept':
            
            # Wähle die Aggregationsfunktion
            if operation == 'Mittelwert':
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
                if operation == 'Mittelwert':
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
                ax.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
                ax.set_xlabel('Months', fontsize=fontsize_axes)
                ax.set_ylabel(y1, fontsize=fontsize_axes)
                ax.grid(True, linestyle='-', alpha=0.7)
                plt.tight_layout()
                st.pyplot(fig)


                # Lineplot erstellen auf Jahresbasis
    
                fig2, ax2 = plt.subplots(figsize=(15,6))
                sns.lineplot(x='Date', y='Temperature', data=temperatur_c3_4, palette=color_palette_1)
                ax2.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
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
            if operation == 'Mittelwert':
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
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax1.set_xlabel('Month', fontsize=fontsize_axes)
            ax1.set_ylabel('CPI', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')

            # Layout anpassen und Plot anzeigen
            plt.tight_layout()
            st.pyplot(fig1)

            # Lineplot erstellen auf Jahresbasis

            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='CPI', data=cpi_aggregated_c3_5_date, palette=color_palette_1)
            ax2.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax2.set_xlabel('Years', fontsize=fontsize_axes)
            ax2.set_ylabel('Temperature', fontsize=fontsize_axes)
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
            if operation == 'Mittelwert':
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
            ax.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax.set_xlabel('Months', fontsize=fontsize_axes)
            ax.set_ylabel('Unemployment', fontsize=fontsize_axes)
            ax.grid(True, linestyle='-')

            # Layout anpassen und Plots anzeigen
            plt.tight_layout()
            st.pyplot(fig)


            # Lineplot erstellen auf Jahresbasis
       
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Unemployment', data=unemployment_aggregated_c3_6_date, palette=color_palette_1)
            ax2.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
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

            if operation == 'Mittelwert':
                isholiday_aggregated_c3_7 = df_c3_7.groupby(['Year', 'Month']).agg({'IsHoliday': 'mean'}).reset_index()
                isholiday_aggregated_date_c3_7 = df_c3_7.groupby('Date').agg({'IsHoliday': 'mean'}).reset_index()
            elif operation == 'Summe':
                isholiday_aggregated_c3_7 = df_c3_7.groupby(['Year', 'Month']).agg({'IsHoliday': 'sum'}).reset_index()
                isholiday_aggregated_date_c3_7 = df_c3_7.groupby('Date').agg({'IsHoliday': 'sum'}).reset_index()
            

            # Erstelle eine Figur und Achse
            fig, ax = plt.subplots(figsize=(15,6))

            # Lineplot anstelle von Stemplot
 

            # Erstelle den Lineplot
            sns.lineplot(x='Month', y='IsHoliday', data=isholiday_aggregated_c3_7, ax=ax, palette=color_palette_3, hue='Year')

            # Setze Titel und Achsenbeschriftungen
            ax.set_title('Auswertung der gewünschten Parameter ', fontsize=fontsize_title)
            ax.set_xlabel('Months', fontsize=fontsize_axes)
            ax.set_ylabel('Holidays', fontsize=fontsize_axes)
            ax.grid(True,linestyle='-')

            # Zeige das Diagramm
            plt.tight_layout()
            st.pyplot(fig)



            # Stemplot erstellen auf Jahresbasis

            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='IsHoliday', data=isholiday_aggregated_date_c3_7, palette=color_palette_1)
            ax2.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
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
            sns.barplot(x='Store',y='Size',data=merge_train,hue=merge_train['Type'], palette='cool',order=merge_train.sort_values('Size')['Store'].tolist())
            ax.set_title('Auswertung der gewünschten Parameter',fontsize=fontsize_title)
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
            if operation == 'Mittelwert':
                fuelprice_aggregated_c3_9_1 = df_c3_9.groupby(['Date']).agg({'Fuel_Price': 'mean'}).reset_index() 
                fuelprice_aggregated_c3_9_2 = df_c3_9.groupby(['Year', 'Month']).agg({'Fuel_Price': 'mean'}).reset_index()  
            else:
                fuelprice_aggregated_c3_9_1 = df_c3_9.groupby(['Date']).agg({'Fuel_Price': 'sum'}).reset_index() 
                fuelprice_aggregated_c3_9_2 = df_c3_9.groupby(['Year', 'Month']).agg({'Fuel_Price': 'sum'}).reset_index()  

           
           # Zeichne Liniendiagramm nach Monaten
       
            fig, ax = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='Fuel_Price', hue='Year', data=fuelprice_aggregated_c3_9_2, palette=color_palette_3, ax=ax)
            ax.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax.set_xlabel('Monate', fontsize=fontsize_axes)
            ax.set_ylabel('Fuel_Price', fontsize=fontsize_axes)
            plt.tight_layout()
            ax.grid(True,linestyle='-')
            st.pyplot(fig)  
           
            # Zeichne Liniendiagramm nach Jahren
  
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Fuel_Price', data=fuelprice_aggregated_c3_9_1, ax=ax1)
            ax1.set_title('Durchschnittlicher Fuel Price pro Jahr', fontsize=fontsize_title)
            ax1.set_xlabel('Jahre', fontsize=fontsize_axes)
            ax1.set_ylabel('Fuel_Price', fontsize=fontsize_axes)
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
            if operation == 'Mittelwert':
                MD1_aggregated_c3_10_date = df_c3_10.groupby(['Date']).agg({'MarkDown1': 'mean'}).reset_index() 
                MD1_aggregated_c3_10 = df_c3_10.groupby(['Year', 'Month']).agg({'MarkDown1': 'mean'}).reset_index()  
            else:
                MD1_aggregated_c3_10_date = df_c3_10.groupby(['Date']).agg({'MarkDown1': 'sum'}).reset_index() 
                MD1_aggregated_c3_10 = df_c3_10.groupby(['Year', 'Month']).agg({'MarkDown1': 'sum'}).reset_index()


            # Erstelle das Diagramm1 - Nur MarkDown1 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown1', hue='Year', data=MD1_aggregated_c3_10, palette=color_palette_3, ax=ax1)
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax1.set_xlabel('Month', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown1', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            
            # Erstelle Diagramm 2 - MarkDown1 im Jahresverlauf
            
          
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='MarkDown1', data=MD1_aggregated_c3_10_date, ax=ax2, palette=color_palette_1)
            ax2.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax2.set_xlabel('Year', fontsize=fontsize_axes)
            ax2.set_ylabel('MarkDown1', fontsize=fontsize_axes)
            plt.tight_layout()
            ax2.grid(True,linestyle='-')
            st.pyplot(fig2)  

            
            if operation == 'Mittelwert':
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
            ax3.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax3.set_xlabel('Year', fontsize=fontsize_axes)
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
            if operation == 'Mittelwert':
                MD2_aggregated_c3_11_date = df_c3_11.groupby(['Date']).agg({'MarkDown2': 'mean'}).reset_index() 
                MD2_aggregated_c3_11 = df_c3_11.groupby(['Year', 'Month']).agg({'MarkDown2': 'mean'}).reset_index()  
            else:
                MD2_aggregated_c3_11_date = df_c3_11.groupby(['Date']).agg({'MarkDown2': 'sum'}).reset_index() 
                MD2_aggregated_c3_11 = df_c3_11.groupby(['Year', 'Month']).agg({'MarkDown2': 'sum'}).reset_index()


            # Erstelle das Diagramm1 - Nur MarkDown2 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown2', hue='Year', data=MD2_aggregated_c3_11, palette=color_palette_3, ax=ax1)
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax1.set_xlabel('Month', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown2', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            
            # Erstelle Diagramm 2 - MarkDown2 im Jahresverlauf
        
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='MarkDown2', data=MD2_aggregated_c3_11_date, ax=ax2, palette=color_palette_1)
            ax2.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax2.set_xlabel('Year', fontsize=fontsize_axes)
            ax2.set_ylabel('MarkDown2', fontsize=fontsize_axes)
            plt.tight_layout()
            ax2.grid(True,linestyle='-')
            st.pyplot(fig2)  

            
            if operation == 'Mittelwert':
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
            ax3.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax3.set_xlabel('Year', fontsize=fontsize_axes)
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
            if operation == 'Mittelwert':
                MD3_aggregated_c3_12_date = df_c3_12.groupby(['Date']).agg({'MarkDown3': 'mean'}).reset_index() 
                MD3_aggregated_c3_12 = df_c3_12.groupby(['Year', 'Month']).agg({'MarkDown3': 'mean'}).reset_index()  
            else:
                MD3_aggregated_c3_12_date = df_c3_12.groupby(['Date']).agg({'MarkDown3': 'sum'}).reset_index() 
                MD3_aggregated_c3_12 = df_c3_12.groupby(['Year', 'Month']).agg({'MarkDown3': 'sum'}).reset_index()


            # Erstelle das Diagramm1 - Nur MarkDown3 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown3', hue='Year', data=MD3_aggregated_c3_12, palette=color_palette_3, ax=ax1)
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax1.set_xlabel('Month', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown3', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            
            # Erstelle Diagramm 2 - MarkDown3 im Jahresverlauf
            
    
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='MarkDown3', data=MD3_aggregated_c3_12_date, ax=ax2, palette=color_palette_1)
            ax2.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax2.set_xlabel('Year', fontsize=fontsize_axes)
            ax2.set_ylabel('MarkDown3', fontsize=fontsize_axes)
            plt.tight_layout()
            ax2.grid(True,linestyle='-')
            st.pyplot(fig2)  

            
            if operation == 'Mittelwert':
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
            ax3.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax3.set_xlabel('Year', fontsize=fontsize_axes)
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
            if operation == 'Mittelwert':
                MD4_aggregated_c3_13_date = df_c3_13.groupby(['Date']).agg({'MarkDown4': 'mean'}).reset_index() 
                MD4_aggregated_c3_13 = df_c3_13.groupby(['Year', 'Month']).agg({'MarkDown4': 'mean'}).reset_index()  
            else:
                MD4_aggregated_c3_13_date = df_c3_13.groupby(['Date']).agg({'MarkDown4': 'sum'}).reset_index() 
                MD4_aggregated_c3_13 = df_c3_13.groupby(['Year', 'Month']).agg({'MarkDown4': 'sum'}).reset_index()


            # Erstelle das Diagramm1 - Nur MarkDown4 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown4', hue='Year', data=MD4_aggregated_c3_13, palette=color_palette_3, ax=ax1)
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax1.set_xlabel('Month', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown4', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            
            # Erstelle Diagramm 2 - MarkDown4 im Jahresverlauf
      
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='MarkDown4', data=MD4_aggregated_c3_13_date, ax=ax2, palette=color_palette_1)
            ax2.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax2.set_xlabel('Year', fontsize=fontsize_axes)
            ax2.set_ylabel('MarkDown4', fontsize=fontsize_axes)
            plt.tight_layout()
            ax2.grid(True,linestyle='-')
            st.pyplot(fig2)  

            
            if operation == 'Mittelwert':
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
            ax3.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax3.set_xlabel('Year', fontsize=fontsize_axes)
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
            if operation == 'Mittelwert':
                MD5_aggregated_c3_14_date = df_c3_14.groupby(['Date']).agg({'MarkDown5': 'mean'}).reset_index() 
                MD5_aggregated_c3_14 = df_c3_14.groupby(['Year', 'Month']).agg({'MarkDown5': 'mean'}).reset_index()  
            else:
                MD5_aggregated_c3_14_date = df_c3_14.groupby(['Date']).agg({'MarkDown5': 'sum'}).reset_index() 
                MD5_aggregated_c3_14 = df_c3_14.groupby(['Year', 'Month']).agg({'MarkDown5': 'sum'}).reset_index()


            # Erstelle das Diagramm1 - Nur MarkDown5 im Monatsverlauf
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown5', hue='Year', data=MD5_aggregated_c3_14, palette=color_palette_3, ax=ax1)
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax1.set_xlabel('Month', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown5', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Zeige Diagramm1 an
            st.pyplot(fig1)

            
            # Erstelle Diagramm 2 - MarkDown5 im Jahresverlauf
            
           
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='MarkDown5', data=MD5_aggregated_c3_14_date, ax=ax2, palette=color_palette_1)
            ax2.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax2.set_xlabel('Year', fontsize=fontsize_axes)
            ax2.set_ylabel('MarkDown5', fontsize=fontsize_axes)
            plt.tight_layout()
            ax2.grid(True,linestyle='-')
            st.pyplot(fig2)  

            
            if operation == 'Mittelwert':
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
            ax3.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
            ax3.set_xlabel('Year', fontsize=fontsize_axes)
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
       
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y=y1, data=agg_c4_year, color='blue', ax=ax1, label=y1)
            ax1.set_ylabel(y1, fontsize=fontsize_axes)
            ax1.set_xlabel(x, fontsize=fontsize_axes)
            ax1.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
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
            ax3.set_xlabel('Month', fontsize=fontsize_axes)
            ax3.set_title('Auswertung der gewünschten Parameter', fontsize=fontsize_title)
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
    color_palette_1 = ['#70FF3E']    # 1 Farbe für Diagramm
    color_palette_2 = ['#70FF3E','#FF6C3E']    # 2 Farben für Diagramm
    color_palette_3 = ['#70FF3E','#FF6C3E','#3ED1FF']    # 3 Farben für Diagramm
    color_palette_4 = ['#70FF3E','#FF6C3E','#3ED1FF','#CD3EFF']    # 4 Farben für Diagramm

    fontsize_title = 20
    fontsize_axes =15
    
    # Erstelle Barplot
    fig1, ax1 = plt.subplots(figsize=(15,6))
    merge_train.corr()['Weekly_Sales'].abs().sort_values()[:-1].plot(kind='bar', ax=ax1, color=color_palette_1)
    ax1.set_title('Feature Korrelationen:', fontsize=fontsize_title)
    
    # Zeige das Diagramm in Streamlit an
    st.pyplot(fig1)


# Heatmap Store-Department-Weekly_Sales - Kombinationen
def get_store_department_sales_heatmap():
    merge_train, merge_test = data_preprocessing()

    # Berechne die Summe der Weekly_Sales pro Store
    store_sales_summary = merge_train.groupby('Store')['Weekly_Sales'].sum().reset_index()

    # Sortiere Stores nach den Umsätzen
    sorted_stores = store_sales_summary.sort_values('Weekly_Sales', ascending=False)['Store']

    # Store - Department - Weekly_Sales
    pivot_table = merge_train.pivot_table(index='Dept', columns='Store', values='Weekly_Sales', aggfunc='sum')
    pivot_table = pivot_table[sorted_stores]

    fig1, ax1 = plt.subplots(figsize=(120,60))
    sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt=".1f")
    plt.title('Weekly Sales Heatmap by Store and Department (sorted by sales)', fontsize=70)
    plt.xlabel('Store', fontsize=50)
    plt.ylabel('Department', fontsize=50)
    st.pyplot(fig1)

# Heatmap Type-Department-Weekly_Sales - Kombinationen
def get_type_department_sales_heatmap():
    merge_train, merge_test = data_preprocessing()

    # Type - Department - Weekly_Sales
    pivot_table = merge_train.pivot_table(index='Dept', columns='Type', values='Weekly_Sales', aggfunc='sum')


    fig2, ax1 = plt.subplots(figsize=(20,120))
    sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt=".1f")
    plt.title('Weekly Sales Heatmap by Type and Department', fontsize=70)
    plt.xlabel('Type', fontsize=50)
    plt.ylabel('Department', fontsize=50)
    st.pyplot(fig2)

# Feiertagsanalyse
def get_holiday():
    # Vordefinierte Farbpaletten
    
    color_palette_1 = ['#70FF3E']    # 1 Farbe für Diagramm
    color_palette_2 = ['#70FF3E','#FF6C3E']    # 2 Farben für Diagramm
    color_palette_3 = ['#70FF3E','#FF6C3E','#3ED1FF']    # 3 Farben für Diagramm
    color_palette_4 = ['#70FF3E','#FF6C3E','#3ED1FF','#CD3EFF']    # 4 Farben für Diagramm

    

    # Funktion aus preprocessing.py importieren
    merge_train, merge_test = data_preprocessing()

    # Gruppiere nach Feiertagen/Nicht-Feiertagen
    holiday_sales = merge_train.groupby('IsHoliday')['Weekly_Sales'].mean()
    holiday_counts = merge_train['IsHoliday'].value_counts()

    # Erstelle Subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Holidays/Nonholidays Sales AVG", "Holidays/Nonholidays Counts"))

    # Farben definieren
    color_palette_2 = ['#763DFF', '#FF3D65']

    # Hinzufügen der Balkendiagramme mit Farben
    fig.add_trace(go.Bar(x=holiday_sales.values, y=holiday_sales.index, 
                        orientation='h', marker_color=color_palette_2), 1, 1)

    fig.add_trace(go.Bar(x=holiday_counts.values, y=holiday_counts.index, 
                        orientation='h', marker_color=color_palette_2), 1, 2)

    # Layout anpassen
    fig.update_layout(showlegend=False)

    # Zeige die Diagramme
    fig.show()





# Dashboard
def get_dashboard():
   
    st.write("Klicke [hier](https://public.tableau.com/views/DashboardFlughafen-Projekt_neu/Dashboard1?:language=de-DE&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link), um das Dashboard zu öffnen.")


    
    


