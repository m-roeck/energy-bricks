from dash import Dash, dcc, html, Input, Output
import os
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import base64
# from functions import retrieve_forecast

# app = Dash(__name__)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

df_forecast = pd.read_csv('prediction_main.csv')
df_forecast = df_forecast.drop(['Unnamed: 0'], axis=1)

logo = "assets/visuals/logoo.png"

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Col(html.Img(src=logo, height="30px")),
            dbc.NavItem(dbc.NavLink("Github", href="https://github.com/m-roeck/microsoft-risk")),
            dbc.NavItem(dbc.NavLink("Linkedin", href="https://www.linkedin.com/in/martin-roeck/")),
        ],
    ),
    color="white",
    dark=False,
)

first_description = dcc.Markdown('''
    &nbsp;  
    **Brief Explanation**

    The graph to the right shows the hourly 
    Locational Marginal Price (LMP) against forecast 
    results for a single day. 

    The legend gives the six forecast models that
    are used to predict the LMP at the given node.
    The actual price is given by the 'LMP' line.
    
    The hour of the day is given on the x-axis
    slider. Use the slider show the real LMP
    against forecasts.

    We see the forecast models capture 
    variations in the price. However,
    it is far from perfect.
''')

second_description = dcc.Markdown('''
    &nbsp;  
    **Brief Explanation**

    This visualization can be used to identify
    periods of wholesale price exposure for C&I 
    sites (e.g. data centers). 

    The top heatmap shows hourly day-ahead LMP forecasts
    at the closest node to the site (i.e. the wholesale
    price of electricity for the site).

    The chart below shows the facilities load,
    in combination with PPA supply from
    hypothetical wind and solar PPAs.

    In combination, the user can identify periods
    when site demand is greater than contracted
    supply, and when extreme pricing periods
    occur. 

    Hypothetically, a user would then choose
    to apply hedging strategies to mitigate
    this market exposure.

    
''')

fourth_description = dcc.Markdown('''
    &nbsp;  
    **Data Pipeline**
    
    The following visual describes the data pipeline utilized for the forecast and consequent risk management visualization. 
    
    While the deployed app uses static data, due to Heroku's cost, the code for the automated dashboard can be found on Github.
    
''')

quick_start_description = dcc.Markdown('''
    &nbsp;  
    **Brief Explanation**
    
    Energy Bricks has two components: (1) data pipeline and trained models, and (2) a dashboard to uncover market exposure.

    **The dashboard** is used to identify periods of extreme pricing events, in combination with periods when PPA energy supply is less than facility demand. This is visualized in the image to the right. In combination, these conditions lead to wholesale market exposure. This events can be mitigated day-ahead using systematic hedging strategies.

    **The forecasting model** is built in Jupyter Notebooks, and can be found in the 'notebooks' folder of the Github repository. For more information on the data pipeline, see the Data Pipeline tab or Github repository.

''')

image_filename = 'assets/visuals/data_pipeline.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

dashboard_explanation_filename = 'assets/visuals/dashboard_explanation.png' # replace with your own image
encoded_dashboard_explanation = base64.b64encode(open(dashboard_explanation_filename, 'rb').read())


load_wind_solar = pd.read_csv('notebooks/load_solar_wind.csv')
load_wind_solar = load_wind_solar.drop(['Unnamed: 0'], axis=1)
load = pd.read_csv('notebooks/load.csv')
load = load.drop(['Unnamed: 0'], axis=1)

df = pd.read_csv('notebooks/prediction.csv')
df = df.rename(columns={"Unnamed: 0": "Hour"})
df = df.set_index('Hour')

# df = retrieve_forecast()
df = df.T
df = df.round(0)

fig = make_subplots(2,1, vertical_spacing = 0.02, row_heights=[0.4,0.6])
fig.add_trace(go.Bar(name="Solar PPA", x=load_wind_solar["hour_ending"], y=load_wind_solar["tot_solar"], marker=dict(color='#EBC471')), row=2, col=1)
fig.add_trace(go.Bar(name="Wind PPA", x=load_wind_solar["hour_ending"], y=load_wind_solar["tot_wind"], marker=dict(color='#8AB280')), row=2, col=1)
fig.add_trace(go.Bar(name="Exposed Load", x=load_wind_solar["hour_ending"], y=load_wind_solar["ext_pricing"], marker=dict(color='#EBE8FC')), row=2, col=1)
fig.add_trace(go.Scatter(name="Datacenter Demand", x=load["hour_ending"], y=load["value"], marker=dict(color='#071334')), row=2,col=1)
fig.add_trace(
    go.Heatmap(
        z=df, text=df, texttemplate="%{text}", textfont={"size":12},
        colorscale= 'Sunset',
        zmin=0,
        zmax=150,
        y=['et', 'rf', 'xgboost', 'catboost', 'lightgbm', 'dt']
    ), 
    row=1, 
    col=1
)
fig.update_layout(
    barmode='stack',
    width=1000,
    height=585,
    paper_bgcolor="#ffffff",
    plot_bgcolor ="#FAFAFA"
)
fig.update_xaxes(showticklabels=False) # hide all the xticks
# fig.update_xaxes(showticklabels=True, row=2, col=1)
fig.update_xaxes(
    showgrid=True, 
    gridwidth=0, 
    gridcolor='#f3f3f3',
    dtick=1, 
    tickson="boundaries",
    title='Hour',
    showticklabels=True,
    showline = True, 
    linecolor = 'black', 
    linewidth = 1, 
    row = 2, 
    col = 1, 
    mirror = True
)
fig.update_yaxes(
    range=[0, 2750],
    showgrid=True, 
    gridwidth=0, 
    gridcolor='#f3f3f3',
    title='Demand & Supply (kW)',
    showline = True, 
    linecolor = 'black', 
    linewidth = 1, 
    row = 2, 
    col = 1, 
    mirror = True
)
fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1, mirror = True)
fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1, mirror = True)

fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="top",
        y=0.57,
        xanchor="left",
        x=0.01
    ),
    margin={
        't': 40,
        'r': 0
    },
)

# load_wind_solar = pd.read_csv('notebooks/load_solar_wind.csv')
# load_wind_solar = load_wind_solar.drop(['Unnamed: 0'], axis=1)
# load = pd.read_csv('notebooks/load.csv')
# load = load.drop(['Unnamed: 0'], axis=1)

# df = pd.read_csv('notebooks/prediction.csv')
# df = df.rename(columns={"Unnamed: 0": "Hour"})
# df = df.set_index('Hour')

# # df = retrieve_forecast()
# df = df.T
# df = df.round(0)

# fig = make_subplots(2,1, vertical_spacing = 0.02, row_heights=[0.4,0.6])
# fig.add_trace(go.Bar(name="Solar PPA", x=load_wind_solar["hour_ending"], y=load_wind_solar["tot_solar"], marker=dict(color='#EBC471')), row=2, col=1)
# fig.add_trace(go.Bar(name="Wind PPA", x=load_wind_solar["hour_ending"], y=load_wind_solar["tot_wind"], marker=dict(color='#8AB280')), row=2, col=1)
# fig.add_trace(go.Scatter(name="Datacenter Demand", x=load["hour_ending"], y=load["value"], marker=dict(color='#071334')), row=2,col=1)
# fig.add_trace(
#     go.Heatmap(
#         z=df, text=df, texttemplate="%{text}", textfont={"size":12},
#         colorscale= 'Sunset',
#         zmin=0,
#         zmax=150,
#         y=['et', 'rf', 'xgboost', 'catboost', 'lightgbm', 'dt']
#     ), 
#     row=1, 
#     col=1
# )
# fig.update_layout(
#     barmode='stack',
#     width=1000,
#     height=585,
#     paper_bgcolor="#ffffff",
#     plot_bgcolor ="#FAFAFA"
# )
# fig.update_xaxes(showticklabels=False) # hide all the xticks
# fig.update_xaxes(showticklabels=True, row=2, col=1)
# fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 1, row = 2, col = 1, mirror = True)
# fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 1, row = 2, col = 1, mirror = True)
# fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1, mirror = True)
# fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1, mirror = True)
# fig.update_xaxes(title='Hour', row=2, col=1)
# fig.update_yaxes(title='Demand & Supply (kW)', row=2, col=1)
# fig.update_xaxes(showgrid=True, gridwidth=0, gridcolor='#f3f3f3', row=2, col=1, dtick=1, tickson="boundaries")
# fig.update_yaxes(showgrid=True, gridwidth=0, gridcolor='#f3f3f3', row=2, col=1)

# fig.update_layout(
#     legend=dict(
#         orientation="h",
#         yanchor="top",
#         y=0.57,
#         xanchor="left",
#         x=0.01
#     ),
#     margin={
#         't': 40,
#         'r': 0
#     },
# )


app.layout = html.Div([

    navbar,
    
    dcc.Tabs(
        id="tabs-with-classes-2",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Quick Start',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected', 
                children=[
                    html.Div(
                        dbc.Row([
                            dbc.Col(html.Div(
                                    quick_start_description,
                                ),
                                width=3,
                                style={
                                    'border-right': '1px solid #d6d6d6'
                                },
                            ),
                            dbc.Col(html.Div([
                                    dbc.Row("s ", style={'color':'white'}),
                                    dbc.Row("s ", style={'color':'white'}),
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_dashboard_explanation.decode()), width="900",),
                                    html.P(" ")
                                ]),
                                width=9,
                            ) 
                        ]),
                    )
                ],
            ),
            dcc.Tab(
                label='Dashboard',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected', 
                children=[
                    html.Div(
                        dbc.Row([
                            dbc.Col(html.Div(
                                    second_description,
                                ),
                                width=3,
                                style={
                                    'border-right': '1px solid #d6d6d6'
                                },
                            ),
                            dbc.Col([
                                dcc.Graph(
                                    id = 'daily_risk_forecast',
                                    figure=fig
                                ),
                                # dcc.Interval(
                                #     id='interval-component',
                                #     interval=1*1000,
                                #     n_intervals=0
                                # )
                            ]) 
                        ]),
                    )
                ],
            ),
            dcc.Tab(
                label='Price Forecast',
                value='tab-3',
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                    html.Div(
                        dbc.Row([
                            dbc.Col(html.Div([
                                    first_description,
                                ]),
                                width=3,
                                style={
                                    'border-right': '1px solid #d6d6d6'
                                },
                            ),
                            dbc.Col([
                                dbc.Row("s ", style={'color':'white'}),
                                dbc.Row(dcc.Graph(id='graph-with-slider')),
                                dbc.Row([
                                    dbc.Col(
                                        width=0
                                    ),
                                    dbc.Col(
                                        dcc.Slider(
                                            0,
                                            23,
                                            step=1,
                                            value=3,
                                            marks={str(i): str(i) for i in range(0,24)},
                                            id='hour-slider'
                                        ),
                                        width = 11
                                    ),
                                    dbc.Col(
                                        width = 0
                                    )
                                ]),
                            ]),
                        ]),
                        # style={
                        #     'border': '3px solid black'
                        # },
                    )
                ]
            ),
            dcc.Tab(
                label='Data Pipeline',
                value='tab-4',
                className='custom-tab',
                selected_className='custom-tab--selected', 
                children=[
                    html.Div(
                        dbc.Row([
                            dbc.Col(html.Div([
                                    fourth_description,
                                ]),
                                width=2,
                                style={
                                    'border-right': '1px solid #d6d6d6'
                                },
                            ),
                            dbc.Col(html.Div([
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), width="1000",),
                                    html.P(" ")
                                ]),
                                width=10,
                                style={
                                    'border-right': '1px solid #d6d6d6'
                                },
                            ),
                        ]),
                    )
                ],
            ),
            
        ],
    )
])

# @app.callback(
#     Output('daily_risk_forecast', 'figure'),
#     Input('interval-component', 'n_intervals'))
# def update_risk(n):
#     load_wind_solar = pd.read_csv('notebooks/load_solar_wind.csv')
#     load_wind_solar = load_wind_solar.drop(['Unnamed: 0'], axis=1)
#     load = pd.read_csv('notebooks/load.csv')
#     load = load.drop(['Unnamed: 0'], axis=1)

#     df = pd.read_csv('notebooks/prediction.csv')
#     df = df.rename(columns={"Unnamed: 0": "Hour"})
#     df = df.set_index('Hour')

#     # df = retrieve_forecast()
#     df = df.T
#     df = df.round(0)

#     fig = make_subplots(2,1, vertical_spacing = 0.02, row_heights=[0.4,0.6])
#     fig.add_trace(go.Bar(name="Wind PPA", x=load_wind_solar["hour_ending"], y=load_wind_solar["tot_solar"], marker=dict(color='#EBC471')), row=2, col=1)
#     fig.add_trace(go.Bar(name="Solar PPA", x=load_wind_solar["hour_ending"], y=load_wind_solar["tot_wind"], marker=dict(color='#8AB280')), row=2, col=1)
#     fig.add_trace(go.Scatter(name="Datacenter Demand", x=load["hour_ending"], y=load["value"], marker=dict(color='#071334')), row=2,col=1)
#     fig.add_trace(
#         go.Heatmap(
#             z=df, text=df, texttemplate="%{text}", textfont={"size":12},
#             colorscale= 'Sunset',
#             zmin=0,
#             zmax=150,
#             y=['et', 'rf', 'xgboost', 'catboost', 'lightgbm', 'dt']
#         ), 
#         row=1, 
#         col=1
#     )
#     fig.update_layout(
#         barmode='stack',
#         width=1000,
#         height=585,
#         paper_bgcolor="#ffffff",
#         plot_bgcolor ="#FAFAFA"
#     )
#     fig.update_xaxes(showticklabels=False) # hide all the xticks
#     fig.update_xaxes(showticklabels=True, row=2, col=1)
#     fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 1, row = 2, col = 1, mirror = True)
#     fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 1, row = 2, col = 1, mirror = True)
#     fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1, mirror = True)
#     fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1, mirror = True)
#     fig.update_xaxes(title='Hour', row=2, col=1)
#     fig.update_yaxes(title='Demand & Supply (kW)', row=2, col=1)
#     fig.update_xaxes(showgrid=True, gridwidth=0, gridcolor='#f3f3f3', row=2, col=1, dtick=1, tickson="boundaries")
#     fig.update_yaxes(showgrid=True, gridwidth=0, gridcolor='#f3f3f3', row=2, col=1)

#     fig.update_layout(
#         legend=dict(
#             orientation="h",
#             yanchor="top",
#             y=0.57,
#             xanchor="left",
#             x=0.01
#         ),
#         margin={
#             't': 40,
#             'r': 0
#         },
#     )

#     return fig


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('hour-slider', 'value')
)
def update_figure(selected_hour):
    
    input = selected_hour

    temp_df = df_forecast.copy()

    temp_df.loc[input,['catboost', 'et', 'rf', 'xgboost', 'lightgbm', 'dt']] = df_forecast.loc[input,'LMP']

    fig_forecast = px.line(temp_df.iloc[input:23].drop(['dt', 'LMP'], axis=1))
    fig_forecast.add_trace(go.Scatter(name="LMP", x=temp_df.index, y=temp_df['LMP'].iloc[0:input+1]))

    fig_forecast.update_layout(
        # barmode='stack',
        width=1000,
        height=450,
        paper_bgcolor="#ffffff",
        plot_bgcolor ="#FAFAFA"
    )   

    fig_forecast.update_xaxes(showline = True, linecolor = 'black', linewidth = 1, mirror = True)
    fig_forecast.update_yaxes(showline = True, linecolor = 'black', linewidth = 1, mirror = True)
    fig_forecast.update_xaxes(showgrid=True, gridwidth=0, gridcolor='#f3f3f3', dtick=1)
    fig_forecast.update_yaxes(showgrid=True, gridwidth=0, gridcolor='#f3f3f3', title ="Price ($/MWh)")
    fig_forecast.update_xaxes(range=[0, 23])
    fig_forecast.update_yaxes(range=[25, 125])
    fig_forecast.update_xaxes(showticklabels=False, title ="")

    fig_forecast.update_layout(
        transition_duration=500,
        margin={
            't': 40,
            'r': 0,
            'b': 0
        },
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        legend_title_text='Forecast Model'
    )

    return fig_forecast


if __name__ == '__main__':
    app.run_server(debug=True)