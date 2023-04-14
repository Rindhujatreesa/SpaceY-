# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                #options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'site1', 'value': 'site1'}, ...]
                                dcc.Dropdown(id='site_dropdown',
                                                  options=[
                                                        {'label': 'All Sites', 'value': 'ALL'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                                        {'label':'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                  ],
                                                  value='ALL',
                                                  placeholder="Select a Launch Site here",
                                                  searchable=True
                                                  ),
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site_dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # Function decorator to specify function input and output

                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
				                    id='range_slider', min=0, max=10000, step=500,
                                    marks={0: '0',2500:'2500',5000:'5000',7500:'7500',10000: '10000'},
                                    value=[min_payload, max_payload]
				                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site_dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
             Input(component_id='site_dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site']==str(entered_site)]
    grouped_fdf = filtered_df.groupby(['class'])['Launch Site'].count().reset_index()
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Percent of successful launches for all sites')
        return fig
    else:
        fig = px.pie(grouped_fdf, 
        values='Launch Site',
        names='class',
        title='Percent of successful launches', 
        color='class')
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site_dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id ="success-payload-scatter-chart",component_property = "figure"), 
    [Input(component_id = "site_dropdown",component_property = "value"),
    Input(component_id = "range_slider", component_property = "value")])
def update_bar_chart(entered_site,range_slider):
    low, high = range_slider
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    filtered_df = spacex_df[spacex_df['Launch Site']==str(entered_site)]
    mask1 = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)    
    if entered_site == 'ALL': 
        fig = px.scatter(
        spacex_df[mask], x="Payload Mass (kg)", y="class", 
        color="Booster Version Category")
        return fig
    else:
        fig = px.scatter(
        filtered_df[mask1], x="Payload Mass (kg)", y="class", 
        color= "Booster Version Category")
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
