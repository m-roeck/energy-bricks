from dash import Dash, dcc, html, Input, Output
import os
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = Dash(__name__)

# server = app.server

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

load_wind_solar = pd.read_csv('notebooks/load_solar_wind.csv')
load_wind_solar = load_wind_solar.drop(['Unnamed: 0'], axis=1)
load = pd.read_csv('notebooks/load.csv')
load = load.drop(['Unnamed: 0'], axis=1)

df = pd.read_csv('notebooks/prediction.csv')
df = df.rename(columns={"Unnamed: 0": "Hour"})
df = df.set_index('Hour')
df = df.T
df = df.round(0)


fig = make_subplots(2,1, vertical_spacing = 0.02, row_heights=[0.4,0.6])
fig.add_trace(go.Bar(name="Wind PPA", x=load_wind_solar["hour_ending"], y=load_wind_solar["tot_solar"], marker=dict(color='#EBC471')), row=2, col=1)
fig.add_trace(go.Bar(name="Solar PPA", x=load_wind_solar["hour_ending"], y=load_wind_solar["tot_wind"], marker=dict(color='#8AB280')), row=2, col=1)
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
fig.update_xaxes(showticklabels=True, row=2, col=1)
fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 1, row = 2, col = 1, mirror = True)
fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 1, row = 2, col = 1, mirror = True)
fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1, mirror = True)
fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1, mirror = True)
fig.update_xaxes(title='Hour', row=2, col=1)
fig.update_yaxes(title='Demand & Supply (kW)', row=2, col=1)
fig.update_xaxes(showgrid=True, gridwidth=0, gridcolor='#f3f3f3', row=2, col=1, dtick=1, tickson="boundaries")
fig.update_yaxes(showgrid=True, gridwidth=0, gridcolor='#f3f3f3', row=2, col=1)

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

df_forecast = pd.read_csv('prediction_main.csv')
df_forecast = df_forecast.drop(['Unnamed: 0'], axis=1)

logo = "assets/visuals/logoo.png"


# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Github", href="https://github.com/m-roeck/microsoft-risk")),
#         dbc.NavItem(dbc.NavLink("Linkedin", href="https://www.linkedin.com/in/martin-roeck/")),
#     ],
#     brand=html.Img(src=logo, height="30px"),
#     brand_href="/Users/martin/myprojects/microsoft_risk/microsoft-risk/visuals/logo.png",
#     color="white",
#     style={
#         'color':'black',
#     },
#     dark=False,
# )

navbar = dbc.Navbar(
    dbc.Container(
        [
            # dbc.Col(
            #     html.A(
            #         # Use row and col to control vertical alignment of logo / brand
            #         dbc.Row(
            #             [
            #                 dbc.Col(html.Img(src=logo, height="30px")),
            #             ],
            #             align="center",
            #             className="g-0",
            #         ),
            #         style={"textDecoration": "none"},
            #     ),
            #     width={'offset': 0.8},
            # ),
            dbc.Col(html.Img(src=logo, height="30px")),
            dbc.NavItem(dbc.NavLink("Github", href="https://github.com/m-roeck/microsoft-risk")),
            dbc.NavItem(dbc.NavLink("Linkedin", href="https://www.linkedin.com/in/martin-roeck/")),
        ],
        style={
        'border': '3px solid black'
        },
    ),
    color="white",
    dark=False,
    style={
        'border': '3px solid black'
    },
)


app.layout = html.Div([

    # dbc.Row([
    #     dbc.Col(
    #             html.A(
    #                 # Use row and col to control vertical alignment of logo / brand
    #                 dbc.Row(
    #                     [
    #                         dbc.Col(html.Img(src=logo, height="50px")),
    #                     ],
    #                     align="center",
    #                     className="g-0",
    #                 ),
    #                 style={"textDecoration": "none"},
    #             ),
    #             width=9,
    #         ),
    #     dbc.Col([
    #             dbc.Col(dbc.NavItem(dbc.NavLink("Github", href="https://github.com/m-roeck/microsoft-risk"))),
    #             dbc.Col(dbc.NavItem(dbc.NavLink("Linkedin", href="https://www.linkedin.com/in/martin-roeck/")))
    #         ], 
    #         width=1
    #     ),
    # ]),
    navbar,
    
    dcc.Tabs(
        id="tabs-with-classes-2",
        value='tab-2',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Visualization',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                    html.Div(
                        dbc.Row([
                            dbc.Col(html.Div(
                                    "A single column",
                                ),
                                width=3,
                                style={
                                    'border': '3px solid black'
                                },
                            ),
                            dbc.Col([
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
                                            value=15,
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
                        style={
                            'border': '3px solid black'
                        },
                    )
                ]
            ),
            dcc.Tab(
                label='Risk Analytics',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected', 
                children=[
                    html.Div(
                        dbc.Row([
                            dbc.Col(html.Div(
                                    "A single column",
                                ),
                                width=3,
                                style={
                                    'border': '3px solid black'
                                },
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id = 'example_graph',
                                    figure = fig,
                                ),
                            ) 
                        ]),
                        style={
                            'border': '3px solid black'
                        },
                    )
                ],
            ),
        ],
        style={
        'border': '3px solid black'
        },
    )
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('hour-slider', 'value'))
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
