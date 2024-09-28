# Function for Dashboard; parameters are passed through selection options in the app
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

import streamlit as st
from preprocessing import data_preprocessing, get_holiday_without_Easter


@st.cache_resource
def create_diagram(y1=None, y2=None, x=None, operation=None):
    '''
    This function is designed to receive parameters from the web app and return the corresponding diagrams based on the input.
    
    Parameters:

    y1: Variable for the left y-axis 
    y2: Variable for the right y-axis
    x: Variable for the x-axis. The available options are Store, Department, and Time.
    operation: Evaluate and visualize data as Average or Sum
    '''

    # Predefined color palettes
    color_palette_1 = ['#FF6C3E']    # 1 color for the diagram
    color_palette_2 = ['#FF6C3E','#3ED1FF']    # 2 colors for the diagram
    color_palette_3 = ['#FF6C3E','#3ED1FF','#70FF3E']    # 3 colors for the diagram
    color_palette_4 = ['#FF6C3E','#3ED1FF','#70FF3E','#CD3EFF']    # 4 colors for the diagram
    
    # Predefined font sizes for axes and titles
    fontsize_title = 20
    fontsize_axes = 15

    merge_train, merge_test = data_preprocessing()


    def plot_bar(df, x, y, ax, title, xlabel, ylabel):
        """Draws a bar chart."""
        sns.barplot(x=x, y=y, data=df, palette=color_palette_1, ax=ax, order=df.sort_values(by=y, ascending=True)[x])
        ax.set_title(title, fontsize=fontsize_title)
        ax.set_xlabel(xlabel, fontsize=fontsize_axes)
        ax.set_ylabel(ylabel, fontsize=fontsize_axes)
        ax.grid(True, linestyle='-')

    def plot_line(df, x, y, ax, title, xlabel, ylabel, hue=None):
        """Draws a line chart."""
        sns.lineplot(x=x, y=y, hue=hue, data=df, color=color_palette_1[0], ax=ax)
        ax.set_title(title, fontsize=fontsize_title)
        ax.set_xlabel(xlabel, fontsize=fontsize_axes)
        ax.set_ylabel(ylabel, fontsize=fontsize_axes)
        ax.grid(True, linestyle='-')

    # Case 1: 1 axis: var1 is weekly sales
    if y1 == 'Weekly_Sales' and y2 is None:

        # Temporary DataFrame for the selected option in the app
        df_choice = pd.DataFrame({
            'x': merge_train[x],   # Variable for the x-axis
            'y1': merge_train[y1], # Variable for the y1-axis
        })

        # Case 1.1: x != Date -> Bar chart
        if x != 'Date':

            # Choose the aggregation function
            agg_func = df_choice.groupby('x').mean if operation == 'Average' else df_choice.groupby('x').sum
            agg_data = agg_func().reset_index()

            # Draw the bar chart
            fig, ax = plt.subplots(figsize=(15,6))
            plot_bar(agg_data, 'x', 'y1', ax, 'Analysis of the desired parameters', x, y1)

            plt.tight_layout()
            st.pyplot(fig)

        # Case 1.2: x == Date -> Line chart
        else:
            # Time series plot 2 (line chart)
            agg_func = df_choice.groupby('x').mean if operation == 'Average' else df_choice.groupby('x').sum
            agg_data = agg_func().reset_index()

            fig, ax = plt.subplots(figsize=(15,6))
            plot_line(agg_data, 'x', 'y1', ax, 'Analysis of the desired parameters', 'Years', y1)

            plt.tight_layout()
            st.pyplot(fig)

            # Time series plot 2 (line chart by months with 1 line per year)
            fig2, ax2 = plt.subplots(figsize=(15,6))

            # Create DataFrame with years, weeks, months, and Weekly_Sales
            df_datetime = pd.DataFrame({
                'Date': merge_train['Date'],
                'Year': merge_train['Date'].dt.year, 
                'Month': merge_train['Date'].dt.month,
                'Week': merge_train['Date'].dt.isocalendar().week,
                'Weekly_Sales': merge_train['Weekly_Sales']
            })

            # Choose the aggregation function
            agg_func = df_datetime.groupby(['Year', 'Month']).mean if operation == 'Average' else df_datetime.groupby(['Year', 'Month']).sum
            datetime_aggregated = agg_func({'Weekly_Sales': 'mean' if operation == 'Average' else 'sum'}).reset_index()

            # Create the plot
            sns.lineplot(data=datetime_aggregated, x='Month', y='Weekly_Sales', ax=ax2, hue='Year', palette=color_palette_3)
            ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax2.set_xlabel('Months', fontsize=fontsize_axes)
            ax2.set_ylabel(y1, fontsize=fontsize_axes)
            ax2.grid(True, linestyle='-')

            plt.tight_layout()
            st.pyplot(fig2)

            # Line chart by weeks
            fig3, ax1 = plt.subplots(figsize=(15,6))

            # Create DataFrame with years, weeks, months, and Weekly_Sales
            df_datetime = pd.DataFrame({
                'Date': merge_train['Date'],
                'Year': merge_train['Date'].dt.year, 
                'Month': merge_train['Date'].dt.month,
                'Week': merge_train['Date'].dt.isocalendar().week,
                'Day': merge_train['Date'].dt.day,
                'Weekly_Sales': merge_train['Weekly_Sales']
            })

            # Choose the aggregation function
            agg_func = df_datetime.groupby(['Year', 'Month','Week']).mean if operation == 'Average' else df_datetime.groupby(['Year', 'Month','Week']).sum
            datetime_aggregated = agg_func({'Weekly_Sales': 'mean' if operation == 'Average' else 'sum'}).reset_index()

            # Create the plot
            sns.lineplot(data=datetime_aggregated, x='Week', y='Weekly_Sales', ax=ax1, hue='Year', palette=color_palette_3)
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.set_xlabel('Weeks', fontsize=fontsize_axes)
            ax1.set_ylabel(y1, fontsize=fontsize_axes)
            ax1.grid(True, linestyle='-')

            # Set x-axis step size to increments of 5 using xticks
            weeks = datetime_aggregated['Week'].unique()
            ax1.set_xticks(range(min(weeks), max(weeks) + 1, 1))

            plt.tight_layout()
            st.pyplot(fig3)
      

    # Case 2: 2 axes, var1 or var2 are Weekly Sales
    if (y1 == 'Weekly_Sales' or y2 == 'Weekly_Sales') and y2 is not None and x == 'Date':

        # Temporary DataFrame for the selected option in the app
        df_choice = pd.DataFrame({
            'Date': merge_train[x],   # Variable for the x-axis
            'Year': merge_train['Date'].dt.year,
            'Month': merge_train['Date'].dt.month,
            'Week': merge_train['Date'].dt.isocalendar().week,
            'y1': merge_train[y1],    # Variable for the y1-axis
            'y2': merge_train[y2],    # Variable for the y2-axis
            'Type': merge_train['Type']
        })

        # Choose the aggregation function
        if operation == 'Average':
            df_choice_aggregated_c2_1 = df_choice.groupby(['Year', 'Month']).agg({'y1': 'mean', 'y2':'mean'}).reset_index()
            df_choice_aggregated_c2_1_date = df_choice.groupby('Date').agg({'y1': 'mean', 'y2':'mean'}).reset_index()
        elif operation == 'Sum':
            df_choice_aggregated_c2_1 = df_choice.groupby(['Year', 'Month']).agg({'y1': 'sum', 'y2':'sum'}).reset_index()
            df_choice_aggregated_c2_1_date = df_choice.groupby('Date').agg({'y1': 'sum', 'y2':'sum'}).reset_index()

        # Plot 1: Line plot on a yearly basis
        if y1 == 'Weekly_Sales' and y2 not in ['Type', 'Size', 'Dept']:
            fig, ax1 = plt.subplots(figsize=(15,6))  

            # Draw y1 (Weekly Sales)
            sns.lineplot(x='Date', y='y1', data=df_choice_aggregated_c2_1_date, color=color_palette_2[0], ax=ax1, label=y1)
            ax1.set_title("Analysis of the desired parameters", fontsize=fontsize_title)
            ax1.set_ylabel(y1, fontsize=fontsize_axes)
            ax1.set_xlabel('Year', fontsize=fontsize_axes)  # 'Date' as label
            ax1.legend(loc='upper left')
            ax1.grid(True, linestyle='-')

            # Second y-axis for y2
            ax2 = ax1.twinx()
            sns.lineplot(x='Date', y='y2', data=df_choice_aggregated_c2_1_date, color=color_palette_2[1], ax=ax2, label=y2)
            ax2.set_ylabel(y2, fontsize=fontsize_axes)
            ax2.legend(loc='upper right')

            plt.tight_layout()
            st.pyplot(fig)

            # Plot 2: Line plot on a monthly basis
            fig, ax1 = plt.subplots(figsize=(15,6))

            # Draw y1 (monthly basis)
            sns.lineplot(x='Month', y='y1', data=df_choice_aggregated_c2_1, hue='Year', palette=color_palette_3, ax=ax1)
            ax1.set_title("Analysis of the desired parameters", fontsize=fontsize_title)
            ax1.set_ylabel(y1, fontsize=fontsize_axes)
            ax1.set_xlabel('Month', fontsize=fontsize_axes)
            ax1.legend(loc='upper left')
            ax1.grid(True, linestyle='-')

            # Second y-axis for y2
            ax2 = ax1.twinx()
            sns.lineplot(x='Month', y='y2', data=df_choice_aggregated_c2_1, hue='Year', palette='Wistia', ax=ax2)
            ax2.set_ylabel(y2, fontsize=fontsize_axes)
            ax2.legend(loc='upper right')

            plt.tight_layout()
            st.pyplot(fig)

        # Case: If y2 is equal to Weekly_Sales
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

        # If the x-axis is not 'Date' and y1/y2 is equal to 'Weekly_Sales'
        elif (y1 == 'Weekly_Sales' or y2 == 'Weekly_Sales') and x != 'Date' and not (y1 == 'Size' or y2 == 'Size'):
            st.write("No meaningful analysis possible. Please try different parameters!")


    # Case3: 1 axis, var1 is not weekly sales
    elif y1 != 'Weekly_Sales' and y2 is None:
        
        # Case3.2: y1 == Store 
        if y1 == 'Store' and x == 'Size':
            st.write("No meaningful evaluation possible. Please try other parameters!")
        
        # Case 3.3: y1 == Dept 
        if y1 == 'Dept':
            st.write("No meaningful evaluation possible. Please try other parameters!")
            

        # Case 3.4: y1 == Temperature 
        if y1 == 'Temperature':
            if x == 'Date':
                df_c3_4 = pd.DataFrame({'Date':merge_train['Date'],
                                        'Year':merge_train['Date'].dt.year, 
                                        'Month':merge_train['Date'].dt.month,
                                        'Week':merge_train['Date'].dt.isocalendar().week,
                                        'Temperature':merge_train['Temperature']})
                    
                # Choose the aggregation function
                if operation == 'Average':
                    temperatur_aggregated_c3_4 = df_c3_4.groupby(['Year', 'Month']).agg({'Temperature': 'mean'}).reset_index()
                    temperatur_c3_4 = df_c3_4.groupby('Date').agg({'Temperature': 'mean'}).reset_index()
                else:
                    temperatur_aggregated_c3_4 = df_c3_4.groupby(['Year', 'Month']).agg({'Temperature': 'sum'}).reset_index()
                    temperatur_c3_4 = df_c3_4.groupby('Date').agg({'Temperature': 'sum'}).reset_index()

                    
                # Draw line chart by month
    

                # Create a figure and axis
                fig, ax = plt.subplots(figsize=(15,6))

                sns.lineplot(x='Month', y='Temperature', hue='Year', data=temperatur_aggregated_c3_4, palette=color_palette_3,ax=ax)

                # Set title, axis labels, and grid
                ax.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
                ax.set_xlabel('Months', fontsize=fontsize_axes)
                ax.set_ylabel('Temperature', fontsize=fontsize_axes)
                ax.grid(True, linestyle='-', alpha=0.7)
                plt.tight_layout()
                st.pyplot(fig)


                # Create line plot by year

                fig2, ax2 = plt.subplots(figsize=(15,6))
                sns.lineplot(x='Date', y='Temperature', data=temperatur_c3_4, color=color_palette_1[0])
                ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
                ax2.set_xlabel('Years', fontsize=fontsize_axes)
                ax2.set_ylabel('Temperature', fontsize=fontsize_axes)
                ax2.grid(True,linestyle='-', alpha=0.7)

                # Add trendline
                plt.tight_layout()

                st.pyplot(fig2)

            elif x != 'Date':
                st.write("No meaningful evaluation possible. Please try other parameters!")


        # Case 3.5: y1 == CPI 
        if y1 == 'CPI' and x == 'Date':
            df_c3_5 = pd.DataFrame({
                'Date': merge_train['Date'],
                'Year': merge_train['Date'].dt.year, 
                'Month': merge_train['Date'].dt.month,
                'Week': merge_train['Date'].dt.isocalendar().week,
                'CPI': merge_train['CPI']
            })
            
            # Choose the aggregation function
            if operation == 'Average':
                cpi_aggregated_c3_5 = df_c3_5.groupby(['Year', 'Month']).agg({'CPI': 'mean'}).reset_index()
                cpi_aggregated_c3_5_date = df_c3_5.groupby('Date').agg({'CPI': 'mean'}).reset_index()
            else:
                cpi_aggregated_c3_5 = df_c3_5.groupby(['Year', 'Month']).agg({'CPI': 'sum'}).reset_index()
                cpi_aggregated_c3_5_date = df_c3_5.groupby('Date').agg({'CPI': 'sum'}).reset_index()

            # Draw line chart by month

            # Create a figure and axis
            fig1, ax1 = plt.subplots(figsize=(15,6))

            # Draw the line chart
            sns.lineplot(x='Month', y='CPI', hue='Year', data=cpi_aggregated_c3_5, palette=color_palette_3, ax=ax1)

            # Set title and axis labels
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.set_xlabel('Months', fontsize=fontsize_axes)
            ax1.set_ylabel('CPI', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')

            # Adjust layout and show plot
            plt.tight_layout()
            st.pyplot(fig1)

            # Create line plot by year

            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='CPI', data=cpi_aggregated_c3_5_date, color=color_palette_1[0])
            ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax2.set_xlabel('Years', fontsize=fontsize_axes)
            ax2.set_ylabel('CPI', fontsize=fontsize_axes)
            ax2.grid(True,linestyle='-', alpha=0.7)

            plt.tight_layout()

            st.pyplot(fig2)

        elif y1 == 'CPI' and x != 'Date':
            st.write("No meaningful evaluation possible. Please try other parameters!")


        # Case 3.6: y1 == Unemployment  
        if y1 == 'Unemployment' and x == 'Date':
            
            df_c3_6 = pd.DataFrame({'Date':merge_train['Date'],
                                    'Year':merge_train['Date'].dt.year, 
                                    'Month':merge_train['Date'].dt.month,
                                    'Week':merge_train['Date'].dt.isocalendar().week,
                                    'Unemployment':merge_train['Unemployment']})
                
            # Choose the aggregation function
            if operation == 'Average':
                unemployment_aggregated_c3_6 = df_c3_6.groupby(['Year', 'Month']).agg({'Unemployment': 'mean'}).reset_index()
                unemployment_aggregated_c3_6_date = df_c3_6.groupby('Date').agg({'Unemployment': 'mean'}).reset_index()
            else:
                unemployment_aggregated_c3_6 = df_c3_6.groupby(['Year', 'Month']).agg({'Unemployment': 'sum'}).reset_index()
                unemployment_aggregated_c3_6_date = df_c3_6.groupby('Date').agg({'Unemployment': 'sum'}).reset_index()

            # Draw line chart by month

            # Create a figure and axis
            fig, ax = plt.subplots(figsize=(15,6))

            sns.lineplot(x='Month', y='Unemployment', hue='Year', data=unemployment_aggregated_c3_6, palette=color_palette_3,ax=ax)

            # Set title and axis labels
            ax.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax.set_xlabel('Months', fontsize=fontsize_axes)
            ax.set_ylabel('Unemployment', fontsize=fontsize_axes)
            ax.grid(True, linestyle='-')

            # Adjust layout and show plots
            plt.tight_layout()
            st.pyplot(fig)

            # Create line plot by year

            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Unemployment', data=unemployment_aggregated_c3_6_date, palette=color_palette_1[0])
            ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax2.set_xlabel('Years', fontsize=fontsize_axes)
            ax2.set_ylabel('Unemployment', fontsize=fontsize_axes)
            ax2.grid(True,linestyle='-', alpha=0.7)
            plt.tight_layout()
            st.pyplot(fig2)

        elif y1 == 'Unemployment' and x != 'Date':
            st.write("No meaningful evaluation possible. Please try other parameters!")

        # Case 3.7: y1 == Fuel_Price  
        if y1 == 'Fuel_Price' and x == 'Date':
            
            df_c3_6 = pd.DataFrame({'Date':merge_train['Date'],
                                    'Year':merge_train['Date'].dt.year, 
                                    'Month':merge_train['Date'].dt.month,
                                    'Week':merge_train['Date'].dt.isocalendar().week,
                                    'Fuel_Price':merge_train['Fuel_Price']})
                
            # Choose the aggregation function
            if operation == 'Average':
                unemployment_aggregated_c3_6 = df_c3_6.groupby(['Year', 'Month']).agg({'Fuel_Price': 'mean'}).reset_index()
                unemployment_aggregated_c3_6_date = df_c3_6.groupby('Date').agg({'Fuel_Price': 'mean'}).reset_index()
            else:
                unemployment_aggregated_c3_6 = df_c3_6.groupby(['Year', 'Month']).agg({'Fuel_Price': 'sum'}).reset_index()
                unemployment_aggregated_c3_6_date = df_c3_6.groupby('Date').agg({'Fuel_Price': 'sum'}).reset_index()

            # Draw line chart by month

            # Create a figure and axis
            fig, ax = plt.subplots(figsize=(15,6))

            sns.lineplot(x='Month', y='Fuel_Price', hue='Year', data=unemployment_aggregated_c3_6, palette=color_palette_3,ax=ax)

            # Set title and axis labels
            ax.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax.set_xlabel('Months', fontsize=fontsize_axes)
            ax.set_ylabel('Fuel_Price', fontsize=fontsize_axes)
            ax.grid(True, linestyle='-')

            # Adjust layout and show plots
            plt.tight_layout()
            st.pyplot(fig)

            # Create line plot by year

            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Fuel_Price', data=unemployment_aggregated_c3_6_date, palette=color_palette_1[0])
            ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax2.set_xlabel('Years', fontsize=fontsize_axes)
            ax2.set_ylabel('Fuel_Price', fontsize=fontsize_axes)
            ax2.grid(True,linestyle='-', alpha=0.7)
            plt.tight_layout()
            st.pyplot(fig2)

        elif y1 == 'Fuel_Price' and x != 'Date':
            st.write("No meaningful evaluation possible. Please try other parameters!")


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
            

            # Create a figure and axis
            fig, ax = plt.subplots(figsize=(15,6))

            # Draw the line chart
            sns.lineplot(x='Month', y='IsHoliday', hue='Year', data=isholiday_aggregated_c3_7, palette=color_palette_3, ax=ax)

            # Set title and axis labels
            ax.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax.set_xlabel('Months', fontsize=fontsize_axes)
            ax.set_ylabel('Holidays', fontsize=fontsize_axes)
            ax.grid(True,linestyle='-')
            
            # Adjust layout and show plot
            plt.tight_layout()
            st.pyplot(fig)

            # Create line plot by year
            fig2, ax2 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='IsHoliday', data=isholiday_aggregated_date_c3_7, palette=color_palette_1[0])
            ax2.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax2.set_xlabel('Years', fontsize=fontsize_axes)
            ax2.set_ylabel('Holidays', fontsize=fontsize_axes)
            ax2.grid(True,linestyle='-', alpha=0.7)
            plt.tight_layout()
            st.pyplot(fig2)
            
        elif y1 == 'IsHoliday' and x != 'Date':
            st.write("No meaningful evaluation possible. Please try other parameters!")


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
            
            #Choose the aggregation function
            if operation == 'Average':
                MD1_aggregated_c3_10_date = df_c3_10.groupby(['Date']).agg({'MarkDown1': 'mean'}).reset_index() 
                MD1_aggregated_c3_10 = df_c3_10.groupby(['Year', 'Month']).agg({'MarkDown1': 'mean'}).reset_index()  
            else:
                MD1_aggregated_c3_10_date = df_c3_10.groupby(['Date']).agg({'MarkDown1': 'sum'}).reset_index() 
                MD1_aggregated_c3_10 = df_c3_10.groupby(['Year', 'Month']).agg({'MarkDown1': 'sum'}).reset_index()


            # Create Diagram 1 - Only MarkDown1 over the course of the month
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown1', hue='Year', data=MD1_aggregated_c3_10, palette=color_palette_3, ax=ax1)
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.set_xlabel('Months', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown1', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Show diagram 1
            st.pyplot(fig1)

            
            # Create Diagram 2 - MarkDown1 over the course of the year
            
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

            # Prepare data for Diagram 2 - All MarkDowns over the course of the year
            df_c3_10_long = df_c3_10_agg.melt(id_vars=['Date'], 
                                            value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                            var_name='MarkDown', 
                                            value_name='Value')

            # Create Diagram 2 - All MarkDowns over the course of the year
            fig3, ax3 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_10_long, palette='cool', ax=ax3)
            ax3.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax3.set_xlabel('Years', fontsize=fontsize_axes)
            ax3.set_ylabel('MarkDowns 1-5', fontsize=fontsize_axes)
            ax3.grid(True,linestyle='-')
            plt.tight_layout()

            # Show diagram 2
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
            
            # Choose aggregational function 
            if operation == 'Average':
                MD2_aggregated_c3_11_date = df_c3_11.groupby(['Date']).agg({'MarkDown2': 'mean'}).reset_index() 
                MD2_aggregated_c3_11 = df_c3_11.groupby(['Year', 'Month']).agg({'MarkDown2': 'mean'}).reset_index()  
            else:
                MD2_aggregated_c3_11_date = df_c3_11.groupby(['Date']).agg({'MarkDown2': 'sum'}).reset_index() 
                MD2_aggregated_c3_11 = df_c3_11.groupby(['Year', 'Month']).agg({'MarkDown2': 'sum'}).reset_index()


            # Create Diagram 1 - Only MarkDown2 over the course of the month
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown2', hue='Year', data=MD2_aggregated_c3_11, palette=color_palette_3, ax=ax1)
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.set_xlabel('Months', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown2', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Show diagram1
            st.pyplot(fig1)

            
            # Create Diagram 2 - MarkDown2 over the course of the year
        
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

            # Prepare data for Diagram 2 - All MarkDowns over the course of the year
            df_c3_11_long = df_c3_11_agg.melt(id_vars=['Date'], 
                                            value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                            var_name='MarkDown', 
                                            value_name='Value')

            # Create Diagram 2 - All MarkDowns over the course of the year
            fig3, ax3 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_11_long, palette='cool', ax=ax3)
            ax3.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax3.set_xlabel('Years', fontsize=fontsize_axes)
            ax3.set_ylabel('MarkDowns 1-5', fontsize=fontsize_axes)
            ax3.grid(True,linestyle='-')
            plt.tight_layout()

            # Show diagram2
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
            
            # Choose aggregational function 
            if operation == 'Average':
                MD3_aggregated_c3_12_date = df_c3_12.groupby(['Date']).agg({'MarkDown3': 'mean'}).reset_index() 
                MD3_aggregated_c3_12 = df_c3_12.groupby(['Year', 'Month']).agg({'MarkDown3': 'mean'}).reset_index()  
            else:
                MD3_aggregated_c3_12_date = df_c3_12.groupby(['Date']).agg({'MarkDown3': 'sum'}).reset_index() 
                MD3_aggregated_c3_12 = df_c3_12.groupby(['Year', 'Month']).agg({'MarkDown3': 'sum'}).reset_index()


            # Create Diagram 1 - Only MarkDown3 over the course of the month
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown3', hue='Year', data=MD3_aggregated_c3_12, palette=color_palette_3, ax=ax1)
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.set_xlabel('Months', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown3', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Show diagram1
            st.pyplot(fig1)

            
            # Create Diagram 2 - MarkDown3 over the course of the year
            
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

            # Prepare data for Diagram 2 - All MarkDowns over the course of the year
            df_c3_12_long = df_c3_12_agg.melt(id_vars=['Date'], 
                                            value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                            var_name='MarkDown', 
                                            value_name='Value')

            # Create Diagram 2 - All MarkDowns over the course of the year
            fig3, ax3 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_12_long, palette='cool', ax=ax3)
            ax3.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax3.set_xlabel('Years', fontsize=fontsize_axes)
            ax3.set_ylabel('MarkDowns 1-5', fontsize=fontsize_axes)
            ax3.grid(True,linestyle='-')
            plt.tight_layout()

            # Show diagram2
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
            
            # Choose aggregational function
            if operation == 'Average':
                MD4_aggregated_c3_13_date = df_c3_13.groupby(['Date']).agg({'MarkDown4': 'mean'}).reset_index() 
                MD4_aggregated_c3_13 = df_c3_13.groupby(['Year', 'Month']).agg({'MarkDown4': 'mean'}).reset_index()  
            else:
                MD4_aggregated_c3_13_date = df_c3_13.groupby(['Date']).agg({'MarkDown4': 'sum'}).reset_index() 
                MD4_aggregated_c3_13 = df_c3_13.groupby(['Year', 'Month']).agg({'MarkDown4': 'sum'}).reset_index()


            # Create Diagram 1 - Only MarkDown4 over the course of the month
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown4', hue='Year', data=MD4_aggregated_c3_13, palette=color_palette_3, ax=ax1)
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.set_xlabel('Months', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown4', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Show diagram1
            st.pyplot(fig1)

            
            # Create Diagram 2 - MarkDown4 over the course of the year
      
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

            # Prepare data for Diagram 2 - All MarkDowns over the course of the year
            df_c3_13_long = df_c3_13_agg.melt(id_vars=['Date'], 
                                            value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                            var_name='MarkDown', 
                                            value_name='Value')

            # Create Diagram 2 - All MarkDowns over the course of the year
            fig3, ax3 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_13_long, palette='cool', ax=ax3)
            ax3.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax3.set_xlabel('Years', fontsize=fontsize_axes)
            ax3.set_ylabel('MarkDowns 1-5', fontsize=fontsize_axes)
            ax3.grid(True,linestyle='-')
            plt.tight_layout()

            # Show diagram2
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
            
            # Choose aggregational function
            if operation == 'Average':
                MD5_aggregated_c3_14_date = df_c3_14.groupby(['Date']).agg({'MarkDown5': 'mean'}).reset_index() 
                MD5_aggregated_c3_14 = df_c3_14.groupby(['Year', 'Month']).agg({'MarkDown5': 'mean'}).reset_index()  
            else:
                MD5_aggregated_c3_14_date = df_c3_14.groupby(['Date']).agg({'MarkDown5': 'sum'}).reset_index() 
                MD5_aggregated_c3_14 = df_c3_14.groupby(['Year', 'Month']).agg({'MarkDown5': 'sum'}).reset_index()


            # Create Diagram 1 - Only MarkDown5 over the course of the month
            fig1, ax1 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Month', y='MarkDown5', hue='Year', data=MD5_aggregated_c3_14, palette=color_palette_3, ax=ax1)
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.set_xlabel('Months', fontsize=fontsize_axes)
            ax1.set_ylabel('MarkDown5', fontsize=fontsize_axes)
            ax1.grid(True,linestyle='-')
            plt.tight_layout()
           
            # Show diagram1
            st.pyplot(fig1)

            
            # Create Diagram 2 - MarkDown5 over the course of the year
            
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

            # Prepare data for Diagram 2 - All MarkDowns over the course of the year
            df_c3_14_long = df_c3_14_agg.melt(id_vars=['Date'], 
                                            value_vars=['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'], 
                                            var_name='MarkDown', 
                                            value_name='Value')

            # Create Diagram 2 - All MarkDowns over the course of the year
            fig3, ax3 = plt.subplots(figsize=(15,6))
            sns.lineplot(x='Date', y='Value', hue='MarkDown', data=df_c3_14_long, palette='cool', ax=ax3)
            ax3.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax3.set_xlabel('Years', fontsize=fontsize_axes)
            ax3.set_ylabel('MarkDowns 1-5', fontsize=fontsize_axes)
            ax3.grid(True,linestyle='-')
            plt.tight_layout()

            # Show diagram2
            st.pyplot(fig3)

        elif y1 == 'MarkDown5' and x != 'Date':
            st.write('Keine sinnvolle Auswertung möglich. Bitte versuche es mit anderen Parametern!')


    # Case 4: 2 y-axes, var1 and var2 are not weekly sales
    if y1 != 'Weekly_Sales' and y2 != 'Weekly_Sales' and x == 'Date' and y2 is not None:

        # Create DataFrame
        df_c4 = pd.DataFrame({
            'Date': merge_train['Date'],
            'Year': merge_train['Date'].dt.year, 
            'Month': merge_train['Date'].dt.month,
            'Week': merge_train['Date'].dt.isocalendar().week,
            y1: merge_train[y1],
            y2: merge_train[y2]
        })

        # Choose the aggregation function
        if operation == 'Average':
            agg_c4_month = df_c4.groupby(['Year', 'Month']).agg({y1: 'mean', y2: 'mean'}).reset_index()
            agg_c4_year = df_c4.groupby('Date').agg({y1: 'mean', y2: 'mean'}).reset_index()
        else:
            agg_c4_month = df_c4.groupby(['Year', 'Month']).agg({y1: 'sum', y2: 'sum'}).reset_index()
            agg_c4_year = df_c4.groupby(['Date']).agg({y1: 'sum', y2: 'sum'}).reset_index()

        if x == 'Date' and (y1 == 'Size' or y1 == 'Type' or y1 == 'Dept' or y2 == 'Size' or y2 == 'Type' or y2 == 'Dept'):
            st.write("No meaningful evaluation possible. Please try with other parameters!")
        
        else:
            # Draw Diagram 1 - Annual Overview
            
            fig1, ax1 = plt.subplots(figsize=(15, 6))
            sns.lineplot(x='Date', y=y1, data=agg_c4_year, color='blue', ax=ax1, label=y1)
            ax1.set_ylabel(y1, fontsize=fontsize_axes)
            ax1.set_xlabel('Years', fontsize=fontsize_axes)
            ax1.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax1.legend(loc='upper left')
            ax1.grid(True, linestyle='-')

            # Create second y-axis
            ax2 = ax1.twinx()
            sns.lineplot(x='Date', y=y2, data=agg_c4_year, color='red', ax=ax2, label=y2)
            ax2.set_ylabel(y2, fontsize=fontsize_axes)
            ax2.legend(loc='upper right')

            # Adjust layout and display
            plt.tight_layout()
            st.pyplot(fig1)

            # Draw Diagram 2 - Monthly Overview
            
            fig2, ax3 = plt.subplots(figsize=(15, 6))
            sns.lineplot(x='Month', y=y1, data=agg_c4_month, ax=ax3, hue='Year', palette=color_palette_3)
            ax3.set_ylabel(y1, fontsize=fontsize_axes)
            ax3.set_xlabel('Months', fontsize=fontsize_axes)
            ax3.set_title('Analysis of the desired parameters', fontsize=fontsize_title)
            ax3.legend(loc='upper left')
            ax3.grid(True, linestyle='-')

            # Create second y-axis for the second diagram
            ax4 = ax3.twinx()
            sns.lineplot(x='Month', y=y2, data=agg_c4_month, ax=ax4, hue='Year', palette='Wistia')
            ax4.set_ylabel(y2, fontsize=fontsize_axes)
            ax4.legend(loc='upper right')

            plt.tight_layout()
            st.pyplot(fig2)

    elif y1 != 'Weekly_Sales' and y2 != 'Weekly_Sales' and x != 'Date' and y2 is not None:   

        st.write("No meaningful evaluation possible. Please try with other parameters!")


# Correlation Analysis
@st.cache_resource
def show_corr():
    merge_train, merge_test = data_preprocessing()

    # Predefined color palettes
    color_palette_1 = ['#FF6C3E']    # 1 color for the chart
    color_palette_2 = ['#FF6C3E','#3ED1FF']    # 2 colors for the chart
    color_palette_3 = ['#FF6C3E','#3ED1FF','#70FF3E']    # 3 colors for the chart
    color_palette_4 = ['#FF6C3E','#3ED1FF','#70FF3E','#CD3EFF']    # 4 colors for the chart

    fontsize_title = 20
    fontsize_axes = 15
    
    # Create bar plot
    fig1, ax1 = plt.subplots(figsize=(15, 6))
    merge_train.corr()['Weekly_Sales'].abs().sort_values()[:-1].plot(kind='bar', ax=ax1, color=color_palette_1)
    ax1.set_title('Correlation Analysis:', fontsize=fontsize_title)
    ax1.set_ylabel('Correlation Coefficients')
    
    # Display the chart in Streamlit
    st.pyplot(fig1)


# Heatmap Store-Department-Weekly_Sales - Combinations
@st.cache_resource
def get_store_department_sales_heatmap():
    merge_train, merge_test = data_preprocessing()

    # Calculate the sum of Weekly_Sales per Store
    store_sales_summary = merge_train.groupby('Store')['Weekly_Sales'].sum().reset_index()

    # Sort stores by sales
    sorted_stores = store_sales_summary.sort_values('Weekly_Sales', ascending=False)['Store']

    # Store - Department - Weekly_Sales
    pivot_table = merge_train.pivot_table(index='Dept', columns='Store', values='Weekly_Sales', aggfunc='sum')
    pivot_table = pivot_table[sorted_stores]

    fig1, ax1 = plt.subplots(figsize=(120, 60))
    sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt=".1f")
    plt.title('Sales Heatmap by Store and Department', fontsize=100)
    plt.xlabel('Store', fontsize=70)
    plt.ylabel('Department', fontsize=70)
    st.pyplot(fig1)

# Heatmap Type-Department-Weekly_Sales - Combinations
def get_type_department_sales_heatmap():
    merge_train, merge_test = data_preprocessing()

    # Type - Department - Weekly_Sales
    pivot_table = merge_train.pivot_table(index='Dept', columns='Type', values='Weekly_Sales', aggfunc='sum')

    fig2, ax1 = plt.subplots(figsize=(20, 100))
    sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt=".1f")
    plt.title('Sales Heatmap by Type and Department', fontsize=20)
    plt.xlabel('Type', fontsize=15)
    plt.ylabel('Department', fontsize=15)
    st.pyplot(fig2)


# Holiday Analysis
@st.cache_resource
def get_holiday():

    # Font sizes
    fontsize_title = 20
    fontsize_axes = 15

    # Plot1: Overview of Holidays (Bar chart for each holiday with Total Sales)
        
    # Predefined color palettes
    colors = ['#FF6C3E', '#3ED1FF', '#70FF3E', '#CD3EFF', '#FFDB3E']  # 5 colors for 5 holidays
    
    # Import function from preprocessing.py
    merge_train, merge_test = data_preprocessing()
    
    # Create the plot layout
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
    ax = ax.flatten()  # Flatten the 2D axes into a 1D list
    
    # Holiday columns and colors
    holidays = ['Christmas', 'Labor_Day', 'Super_Bowl', 'Thanksgiving', 'Easter']  # Only 5 holidays
    
    # Plot a bar representation of Weekly_Sales for each holiday
    for i, holiday in enumerate(holidays):
        # Filter by the current holiday
        holiday_data = merge_train[merge_train[holiday] == 1]
        
        # Draw a bar chart for Weekly_Sales based on the year
        holiday_data.groupby('Year')['Weekly_Sales'].sum().plot(kind='bar', ax=ax[i], color=colors[i])
        
        # Set the title of the subplot
        ax[i].set_title(f'{holiday}', fontsize=fontsize_title)
        ax[i].set_xlabel('')
        ax[i].set_ylabel('Sum of Sales', fontsize=fontsize_axes)
    
    # Remove the last (empty) subplot if there are only 5 plots
    fig.delaxes(ax[-1])  # Remove the unnecessary axis as we only need 5 plots
    
    # Adjust layout
    plt.tight_layout()

    # Insert title
    st.markdown("<h5 style='text-align: center;'>Overview of Holiday Sales</h5>", unsafe_allow_html=True)
    
    # Display plot in Streamlit
    st.pyplot(fig)
    

    # Plot2: 
       
    # Font sizes
    fontsize_title = 20
    fontsize_axes = 15

    # Line chart by weeks
    fig, ax1 = plt.subplots(figsize=(15, 6))

    # Create a DataFrame with years, weeks, months, and Weekly_Sales
    df_datetime = pd.DataFrame({
        'Date': merge_train['Date'],
        'Year': merge_train['Date'].dt.year,
        'Month': merge_train['Date'].dt.month,
        'Week': merge_train['Date'].dt.isocalendar().week,
        'Day': merge_train['Date'].dt.day,
        'Weekly_Sales': merge_train['Weekly_Sales']
    })

    # Select the aggregation function and reset the index
    agg_func = df_datetime.groupby(['Date'])['Weekly_Sales'].mean().reset_index()

    # Create plot for average sales
    sns.lineplot(data=agg_func, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Analysis of the Desired Parameters', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average of Sales', fontsize=fontsize_axes)
    ax1.grid(True, linestyle='-')

    # Add holiday sales
    holidays = ['Christmas', 'Labor_Day', 'Super_Bowl', 'Thanksgiving', 'Easter']
    colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#FFC300']  # Bolder color palette for holidays

    # Second Y-axis for holiday sales
    ax2 = ax1.twinx()

    for i, holiday in enumerate(holidays):
        # Filter by the current holiday
        holiday_data = merge_train[merge_train[holiday] == 1]
        
        # Calculate average sales for the holiday
        holiday_sales = holiday_data.groupby('Date')['Weekly_Sales'].mean().reset_index()

        # Add bar chart for the holiday with wider bars
        ax2.bar(holiday_sales['Date'], holiday_sales['Weekly_Sales'], color=colors[i], alpha=0.3, width=10, label=holiday, linestyle='--')

    # Labels for the second Y-axis
    ax2.set_ylabel('Average of Holiday Sales', fontsize=fontsize_axes)

    # Add legend
    ax1.legend(title='Average Weekly Sales', fontsize=fontsize_axes)
    ax2.legend(holidays, title='Holidays', fontsize=fontsize_axes, loc='upper left')

    plt.tight_layout()
    st.pyplot(fig)
    


    # Plot3: All Markdowns + Holidays + Weekly_Sales
        
    # Step 1: Create DataFrame with the necessary columns
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

    # Step 2: Filter holidays
    holidays = df_datetime[df_datetime['IsHoliday'] == 1]

    # Step 3: Calculate average Weekly_Sales per date
    agg_df = df_datetime.groupby('Date').agg({
        'Weekly_Sales': 'mean',
        'MarkDown1': 'mean',
        'MarkDown2': 'mean',
        'MarkDown3': 'mean',
        'MarkDown4': 'mean',
        'MarkDown5': 'mean'
    }).reset_index()

    # Step 4: Filter DataFrame for date range from July 2011
    agg_df = agg_df[agg_df['Date'] >= '2011-07-01']

    # Font sizes
    fontsize_title = 20
    fontsize_axes = 15

    # Step 5: Create plot
    fig3, ax1 = plt.subplots(figsize=(15, 6))

    # Step 6: Plot average Weekly Sales on the first Y-axis
    sns.lineplot(data=agg_df, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Average Weekly Sales and Markdowns Over Time', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average Weekly Sales', fontsize=fontsize_axes)
    ax1.grid(True)

    # Step 7: Plot Markdowns on the second Y-axis
    ax2 = ax1.twinx()  # Create second Y-axis
    for i in range(1, 6):
        markdown_col = f'MarkDown{i}'
        sns.lineplot(data=agg_df, x='Date', y=markdown_col, ax=ax2, label=markdown_col, alpha=0.6)

    ax2.set_ylabel('Markdowns', fontsize=fontsize_axes)

    # Step 8: Mark holidays
    for index, row in holidays.iterrows():
        if row['Date'] >= pd.Timestamp('2011-07-01'):  # Only display holidays if they fall after the filter date
            ax1.axvline(x=row['Date'], color='red', linestyle='--', alpha=0.5)

    # Step 9: Adjust legend and layout
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    st.pyplot(fig3)

    

    # Plot4: Only MarkDown1 + Holidays + Weekly_Sales

    # Step 1: Create a DataFrame with the necessary columns
    df_datetime = pd.DataFrame({
        'Date': merge_train['Date'],
        'Weekly_Sales': merge_train['Weekly_Sales'],
        'MarkDown1': merge_train['MarkDown1'],
        'IsHoliday': merge_train['IsHoliday']  
    })

    # Step 2: Filter holidays
    holidays = df_datetime[df_datetime['IsHoliday'] == 1]

    # Step 3: Calculate average Weekly_Sales per date
    agg_df = df_datetime.groupby('Date').agg({
        'Weekly_Sales': 'mean',
        'MarkDown1': 'mean'
    }).reset_index()

    # Step 4: Filter DataFrame to date range from July 2011
    agg_df = agg_df[agg_df['Date'] >= '2011-07-01']

    # Font sizes
    fontsize_title = 20
    fontsize_axes = 15

    # Step 5: Create plot
    fig4, ax1 = plt.subplots(figsize=(15, 6))

    # Step 6: Plot average Weekly Sales on the first Y-axis
    sns.lineplot(data=agg_df, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Average Weekly Sales and MarkDown1 Over Time', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average Weekly Sales', fontsize=fontsize_axes)
    ax1.grid(True)

    # Step 7: Plot only MarkDown1 on the second Y-axis
    ax2 = ax1.twinx()  # Create second Y-axis
    sns.lineplot(data=agg_df, x='Date', y='MarkDown1', ax=ax2, color='orange', label='MarkDown1', alpha=0.6)
    ax2.set_ylabel('MarkDown1', fontsize=fontsize_axes)

    # Step 8: Mark holidays
    for index, row in holidays.iterrows():
        if row['Date'] >= pd.Timestamp('2011-07-01'):  # Only display holidays if they are after the filter date
            ax1.axvline(x=row['Date'], color='red', linestyle='--', alpha=0.5)

    # Step 9: Adjust legend and layout

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    st.pyplot(fig4)
    

    # Plot5: Only MarkDown2 + Holidays + Weekly_Sales

    # Step 1: Create DataFrame with the necessary columns
    df_datetime = pd.DataFrame({
        'Date': merge_train['Date'],
        'Weekly_Sales': merge_train['Weekly_Sales'],
        'MarkDown2': merge_train['MarkDown2'],
        'IsHoliday': merge_train['IsHoliday']  
    })

    # Step 2: Filter holidays
    holidays = df_datetime[df_datetime['IsHoliday'] == 1]

    # Step 3: Calculate average Weekly_Sales per date
    agg_df = df_datetime.groupby('Date').agg({
        'Weekly_Sales': 'mean',
        'MarkDown2': 'mean'
    }).reset_index()

    # Step 4: Filter DataFrame for date range starting from July 2011
    agg_df = agg_df[agg_df['Date'] >= '2011-07-01']

    # Font sizes
    fontsize_title = 20
    fontsize_axes = 15

    # Step 5: Create plot
    fig5, ax1 = plt.subplots(figsize=(15, 6))

    # Step 6: Plot average Weekly Sales on the first Y-axis

    sns.lineplot(data=agg_df, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Average Weekly Sales and MarkDown2 Over Time', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average Weekly Sales', fontsize=fontsize_axes)
    ax1.grid(True)

    # Step 7: Plot only MarkDown2 on the second Y-axis
    ax2 = ax1.twinx()  # Create a second Y-axis
    sns.lineplot(data=agg_df, x='Date', y='MarkDown2', ax=ax2, color='orange', label='MarkDown2', alpha=0.6)
    ax2.set_ylabel('MarkDown2', fontsize=fontsize_axes)

    # Step 8: Mark holidays
    for index, row in holidays.iterrows():
        if row['Date'] >= pd.Timestamp('2011-07-01'):  # Only display holidays that are after the filter date
            ax1.axvline(x=row['Date'], color='red', linestyle='--', alpha=0.5)

    # Step 9: Adjust legend and layout
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    st.pyplot(fig5) 
    

    # Plot6: Only MarkDown3 + Holidays + Weekly_Sales

    # Step 1: Create a DataFrame with the necessary columns
    df_datetime = pd.DataFrame({
        'Date': merge_train['Date'],
        'Weekly_Sales': merge_train['Weekly_Sales'],
        'MarkDown3': merge_train['MarkDown3'],  # Use only MarkDown3
        'IsHoliday': merge_train['IsHoliday']  
    })

    # Step 2: Filter holidays
    holidays = df_datetime[df_datetime['IsHoliday'] == 1]

    # Step 3: Calculate average Weekly_Sales per date

    agg_df = df_datetime.groupby('Date').agg({
        'Weekly_Sales': 'mean',
        'MarkDown3': 'mean'  # Nur MarkDown3 aggregieren
    }).reset_index()

    # Step 4: Filter DataFrame for date range starting from July 2011
    agg_df = agg_df[agg_df['Date'] >= '2011-07-01']

    # Font sizes
    fontsize_title = 20
    fontsize_axes = 15

    # Step 5: Create the plot
    fig6, ax1 = plt.subplots(figsize=(15, 6))

    # Step 6: Plot average Weekly Sales on the first Y-axis
    sns.lineplot(data=agg_df, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Average Weekly Sales and MarkDown3 Over Time', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average Weekly Sales', fontsize=fontsize_axes)
    ax1.grid(True)

    # Step 7: Plot only MarkDown3 on the second Y-axis
    ax2 = ax1.twinx()  # Create a second Y-axis
    sns.lineplot(data=agg_df, x='Date', y='MarkDown3', ax=ax2, color='orange', label='MarkDown3', alpha=0.6)
    ax2.set_ylabel('MarkDown3', fontsize=fontsize_axes)

    # Step 8: Mark holidays
    for index, row in holidays.iterrows():
        if row['Date'] >= pd.Timestamp('2011-07-01'):  # Only show holidays if they fall after the filter date
            ax1.axvline(x=row['Date'], color='red', linestyle='--', alpha=0.5)

    # Step 9: Adjust legend and layout

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    st.pyplot(fig6)
    

    # Plot7: Only MarkDown4 + Holidays + Weekly_Sales

    # Step 1: Create a DataFrame with the necessary columns
    df_datetime = pd.DataFrame({
        'Date': merge_train['Date'],
        'Weekly_Sales': merge_train['Weekly_Sales'],
        'MarkDown4': merge_train['MarkDown4'],  # Use MarkDown4
        'IsHoliday': merge_train['IsHoliday']  
    })

    # Step 2: Filter holidays
    holidays = df_datetime[df_datetime['IsHoliday'] == 1]

    # Step 3: Calculate average Weekly_Sales per date
    agg_df = df_datetime.groupby('Date').agg({
        'Weekly_Sales': 'mean',
        'MarkDown4': 'mean'  # MarkDown4 aggregieren
    }).reset_index()

    # Step 4: Filter the DataFrame for the date range starting from July 2011
    agg_df = agg_df[agg_df['Date'] >= '2011-07-01']

    # Font sizes
    fontsize_title = 20
    fontsize_axes = 15

    # Step 5: Create the plot
    fig7, ax1 = plt.subplots(figsize=(15, 6))

    # Step 6: Plot the average Weekly Sales on the first Y-axis
    sns.lineplot(data=agg_df, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Average Weekly Sales and MarkDown4 Over Time', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average Weekly Sales', fontsize=fontsize_axes)
    ax1.grid(True)

    # Step 7: Plot only MarkDown4 on the second Y-axis
    ax2 = ax1.twinx()  # Create the second Y-axis
    sns.lineplot(data=agg_df, x='Date', y='MarkDown4', ax=ax2, color='orange', label='MarkDown4', alpha=0.6)
    ax2.set_ylabel('MarkDown4', fontsize=fontsize_axes)

    # Step 8: Mark holidays
    for index, row in holidays.iterrows():
        if row['Date'] >= pd.Timestamp('2011-07-01'):  # Only show holidays if they are after the filter date
            ax1.axvline(x=row['Date'], color='red', linestyle='--', alpha=0.5)

    # Step 9: Adjust legend and layout
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    st.pyplot(fig7)
    

    # Plot8: Only MarkDown5 + Holidays + Weekly_Sales

    # Step 1: Create DataFrame with the necessary columns
    df_datetime = pd.DataFrame({
        'Date': merge_train['Date'],
        'Weekly_Sales': merge_train['Weekly_Sales'],
        'MarkDown5': merge_train['MarkDown5'],  # Use MarkDown5
        'IsHoliday': merge_train['IsHoliday']  
    })

    # Step 2: Filter holidays
    holidays = df_datetime[df_datetime['IsHoliday'] == 1]

    # Step 3: Calculate average Weekly_Sales per date

    agg_df = df_datetime.groupby('Date').agg({
        'Weekly_Sales': 'mean',
        'MarkDown5': 'mean'  # MarkDown5 aggregieren
    }).reset_index()

    # Step 4: Filter DataFrame for the date range starting from July 2011
    agg_df = agg_df[agg_df['Date'] >= '2011-07-01']

    # Font sizes
    fontsize_title = 20
    fontsize_axes = 15

    # Step 5: Create the plot
    fig8, ax1 = plt.subplots(figsize=(15, 6))

    # Step 6: Plot average Weekly Sales on the first Y-axis

    sns.lineplot(data=agg_df, x='Date', y='Weekly_Sales', ax=ax1, color='blue', label='Average Weekly Sales')
    ax1.set_title('Average Weekly Sales and MarkDown5 Over Time', fontsize=fontsize_title)
    ax1.set_xlabel('Date', fontsize=fontsize_axes)
    ax1.set_ylabel('Average Weekly Sales', fontsize=fontsize_axes)
    ax1.grid(True)

    # Step 7: Plot only MarkDown5 on the second Y-axis
    ax2 = ax1.twinx()  # Create a second Y-axis
    sns.lineplot(data=agg_df, x='Date', y='MarkDown5', ax=ax2, color='orange', label='MarkDown5', alpha=0.6)
    ax2.set_ylabel('MarkDown5', fontsize=fontsize_axes)

    # Step 8: Mark holidays
    for index, row in holidays.iterrows():
        if row['Date'] >= pd.Timestamp('2011-07-01'):  # Only show holidays that are after the filter date
            ax1.axvline(x=row['Date'], color='red', linestyle='--', alpha=0.5)

    # Step 9: Adjust legend and layout
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    st.pyplot(fig8)
    
  
# Dashboard
def get_dashboard():
   
    st.write("Click [here](https://public.tableau.com/app/profile/over.fit/viz/Dash-GO-NOW-040_this/1a-Data?publish=yes) to open the dashboard.")



    
    


