#!/usr/bin/env python
# coding: utf-8


"""Date: The date of the observation.
Recession: A binary variable indicating recession perion; 1 means it was recession, 0 means it was normal.
Automobile_Sales: The number of vehicles sold during the period.
GDP: The per capita GDP value in USD.
Unemployment_Rate: The monthly unemployment rate.
Consumer_Confidence: A synthetic index representing consumer confidence, which can impact consumer spending and automobile purchases.
Seasonality_Weight: The weight representing the seasonality effect on automobile sales during the period.
Price: The average vehicle price during the period.
Advertising_Expenditure: The advertising expenditure of the company.
Vehicle_Type: The type of vehicles sold; Supperminicar, Smallfamiliycar, Mediumfamilycar, Executivecar, Sports.
Competition: The measure of competition in the market, such as the number of competitors or market share of major manufacturers.
Month: Month of the observation extracted from Date.
Year: Year of the observation extracted from Date.

Components of the report items
Yearly Automobile Sales Statistics

Yearly Average Automobile sales using line chart for the whole period.
For the chosen year provide,
Total Monthly Automobile sales using line chart.
Average Monthly Automobile sales of each vehicle type using bar chart.
Total Advertisement Expenditure for each vehicle using pie chart
Recession Period Statistics

Average Automobile sales using line chart for the Recession Period using line chart.
Average number of vehicles sold by vehicle type using bar chart
Total expenditure share by vehicle type during recession usssing pie chart
Effect of unemployment rate on vehicle type and sales using bar chart
NOTE: You have worked creating a dashboard components in Flight Delay Time Statistics Dashboard section. You will be working on the similar lines for this Dashboard


Install python packages required to run the application. Copy and paste the below command to the terminal


pip3.8 install setuptools

python3.8 -m pip install packaging

python3.8 -m pip install pandas dash

pip3 install httpx==0.20 dash plotly


python3.8 NR.py
"""


# In[ ]:

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')
# Initialize the Dash app
app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
#---------------------------------------------------------------------------------

# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the dropdown menu options
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", 
                style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    #TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:",style={'width':.8,'margin-left':'3px','font-size':20,'text-align-last':'center'}), 
        dcc.Dropdown(
            id='dropdown-statistics',
            options= dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type'
        )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder=str(year_list[0])
        )),
    #Second Inner division for adding 1 inner division for 4 output graphs
    
 html.Div([#TASK 2.3: Add a division for output display
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex','flex-flow':'row wrap'}),
    html.Div(id='output-container2', className='chart-grid', style={'display': 'flex','flex-flow':'row wrap'}),
    ])
])
# Layout ends 

#1st callback To enable or disable the input container based on the selected statistics.
#The selected statistics here can be either Recession Statistics or Yearly Statistics.
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics':
        return False
    else:
        return True

#2nd Callback layout has 1 output container
#will be required to return the plots developed dcc.Graph() into this container as divisions.
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')])

def update_output_container(selected_statistics,input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        output_data = data[data['Recession'] == 1]
    #else:
    #Filter by year 
    #output_data = data[data['Year'] == input_year]


        #Plot 1 Automobile sales fluctuate over Recession Period (year wise) using line chart
        # grouping data for plotting

        yearly_rec= output_data.groupby('Year')['Automobile_Sales'].mean().reset_index()

        # Plotting the line graph
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,

            x='Year',
            y='Automobile_Sales',
            title="Average Number of Automobile Sold in Recession Years"
            )
        )

        #Plot 2 Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        # grouping data for plotting
        cartype_rec = output_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index() 
        R_chart2 = dcc.Graph(
            figure=px.bar(cartype_rec,
                x='Vehicle_Type', 
                y='Automobile_Sales', 
                title="Average Number of Vehicles (by Type) Sold in Recession"
                )
            )
        # Plot 3 : Pie chart for total expenditure share by vehicle type during recessions
            # grouping data for plotting
        exp_rec= output_data.groupby(['Vehicle_Type'])['Advertising_Expenditure'].mean().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, 
                values='Advertising_Expenditure', 
                names='Vehicle_Type', 
                title="Advertising per Vehicle Type in Recession"
                )
            )

        # Plot 4 Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        unemply_type = output_data.groupby('Vehicle_Type')[['Automobile_Sales','unemployment_rate']].mean().reset_index()
        R_chart4  = dcc.Graph(
                    figure= px.bar(unemply_type, 
                    x='Vehicle_Type',
                    y='Automobile_Sales',
                    color = 'unemployment_rate',
                    title="The Effect of Unemployment Rate on Vehicle Type Sales in Recession"
                                )
                            )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)],style={'display': 'flex'})
        ]
    # TASK 2.6: Create and display graphs for Yearly Report Statistics
    # Yearly Statistic Report Plots
    elif (input_year and selected_statistics=='Yearly Statistics') :
        output_data = data[data['Year'] == input_year] # name it output_data  - then copy-paste code above instead of having a # name yearly statistics
        #plot 1 Yearly Automobile sales using line chart for the whole period.
        year_sales = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(year_sales,
            x='Year',
            y='Automobile_Sales',
            title="Average Number of Automobile Sold between 1980 and 2024"
            )
        )

        # Plot 2 Total Monthly Automobile sales using line chart. I THINK BAR IS BETTER
        month_sales = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        ordered_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        Y_chart2 = dcc.Graph( figure=px.bar(month_sales,
            x='Month',
            y='Automobile_Sales',
            category_orders={'Month':ordered_months },
            title="Aggregated Number of Automobile Sold per Month between 1980-2024"))

        # Plot bar chart for average number of vehicles sold during the given year
        cartype_rec = output_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index() 
        Y_chart3 = dcc.Graph(figure=px.bar(cartype_rec,
                x='Vehicle_Type', 
                y='Automobile_Sales', 
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

        # Total Advertisement Expenditure for each vehicle using pie chart
        exp_rec= output_data.groupby(['Vehicle_Type'])['Advertising_Expenditure'].mean().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_rec, 
                values='Advertising_Expenditure', 
                names='Vehicle_Type', 
                title='Advertising per Vehicle Type in in the year {}'.format(input_year)))        

        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display': 'flex'})
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
