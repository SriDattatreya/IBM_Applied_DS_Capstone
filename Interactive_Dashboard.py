# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the data into pandas dataframe
spacex_df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

opt_list = [{'label': 'All Sites', 'value': 'ALL'}] + \
           [{'label': ls, 'value': ls} for ls in pd.unique(spacex_df['Launch Site']).tolist()]

min_slider = 0
max_slider = 10000
step_slider = 1000

# Create a dash application
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=opt_list,
                                             value='ALL',
                                             placeholder='Select a Launch Site',
                                             searchable=True,
                                             style={'width': '100%',
                                                    'padding': '3px',
                                                    'font-size': '20px',
                                                    'text-align-last': 'center'}
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=min_slider, max=max_slider, step=step_slider,
                                                marks={i: '{}'.format(i) for i
                                                       in range(min_slider, max_slider + 1, step_slider)},
                                                value=[min_payload, max_payload]
                                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        df1 = spacex_df.loc[spacex_df['class'] == 1]
        fig1 = px.pie(df1, values='class',
                      names='Launch Site',
                      title='Total Successful launches by Site')
    else:
        df1 = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        fig1 = px.pie(df1,
                      names='class',
                      title='Total Successful launches for site %s' % entered_site)
    # return the pie chart
    return fig1


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, slider_range):
    low, high = slider_range
    df2 = spacex_df.loc[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    if entered_site == 'ALL':
        fig2 = px.scatter(df2, x='Payload Mass (kg)', y='class',
                          color='Booster Version Category',
                          title='Correlation between Payload and Success for all Sites')
    else:
        df2 = df2.loc[df2['Launch Site'] == entered_site]
        fig2 = px.scatter(df2, x='Payload Mass (kg)', y='class',
                          color='Booster Version Category',
                          title='Correlation between Payload and Success for site %s' % entered_site)
    # return the outcomes scatter chart
    return fig2


# Run the app
if __name__ == '__main__':
    app.run_server(host="localhost", debug=False, dev_tools_ui=False, dev_tools_props_check=False)