# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
spacex_df["class"]=spacex_df["class"].astype("category")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df[['Launch Site']].groupby(['Launch Site'], as_index=False).first()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': launch_sites['Launch Site'][0], 'value': launch_sites['Launch Site'][0]},
                                        {'label': launch_sites['Launch Site'][1], 'value': launch_sites['Launch Site'][1]},
                                        {'label': launch_sites['Launch Site'][2], 'value': launch_sites['Launch Site'][2]},
                                        {'label': launch_sites['Launch Site'][3], 'value': launch_sites['Launch Site'][3]},
                                    ],
                                    value='ALL',
                                    placeholder="Select Launch Site here",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(id='success-pie-chart'),
                                html.Br(),

                                html.P("Payload Range (kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=500,
                                    marks={0: '0',2500: '2500',5000: '5000',7500: '7500',10000: '10000'},
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(id='success-payload-scatter-chart'),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback([
               Output(component_id='success-pie-chart', component_property='children'),
               Output(component_id='success-payload-scatter-chart', component_property='children')
              ],
              [
               Input(component_id='site-dropdown',  component_property='value'),
               Input(component_id='payload-slider', component_property='value')
              ]
             )
def get_scatter_chart(entered_site,selected_range):
    if entered_site == 'ALL':
        filter_logic = spacex_df['Payload Mass (kg)'].between( selected_range[0],selected_range[1] )
        fig_pie = px.pie(spacex_df[filter_logic],values='class', names='Launch Site',title='Total Success Launches By Site')
        fig_scat = px.strip(spacex_df[filter_logic],
                            x='Payload Mass (kg)',
                            y='class',
                            color='Booster Version Category',
                            title = 'Correlation for Payload and Success for All Sites')
    else:
        site_df = spacex_df[spacex_df['Launch Site']==entered_site]
        filter_logic = site_df['Payload Mass (kg)'].between( selected_range[0],selected_range[1] )
        fig_pie = px.pie(site_df[filter_logic],names='class', title='Total Success Launches for Site '+entered_site)
        print(site_df[filter_logic])
        fig_scat = px.strip(site_df[filter_logic],
                            x='Payload Mass (kg)',
                            y='class',
                            color='Booster Version Category',
                            title = 'Correlation for Payload and Success for Site '+entered_site)
    return [dcc.Graph(figure=fig_pie),
            dcc.Graph(figure=fig_scat)]

# Run the app
if __name__ == '__main__':
    app.run_server()
