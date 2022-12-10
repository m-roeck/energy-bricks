from dash import Dash, dcc, html, Input, Output
import os
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = Dash(__name__)

server = app.server

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


fig = make_subplots(2,1, vertical_spacing = 0.01)
fig.add_trace(go.Bar(x=load_wind_solar["hour_ending"], y=load_wind_solar["tot_solar"]), row=2, col=1)
fig.add_trace(go.Bar(x=load_wind_solar["hour_ending"], y=load_wind_solar["tot_wind"]), row=2, col=1)
fig.add_trace(go.Line(x=load["hour_ending"], y=load["value"]), row=2,col=1)
fig.add_trace(go.Heatmap(z=df, text=df, texttemplate="%{text}", textfont={"size":10}), row=1, col=1)
fig.update_layout(
    barmode='stack',
    width=1000,
    height=800,
)
fig.update_xaxes(showticklabels=False) # hide all the xticks
fig.update_xaxes(showticklabels=True, row=2, col=1)

fig.update_layout(legend=dict(
    orientation="h",
    yanchor="top",
    y=0.49,
    xanchor="left",
    x=0.01
))

df_forecast = pd.read_csv('prediction_main.csv')
df_forecast = df_forecast.drop(['Unnamed: 0'], axis=1)


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Energy Bricks",
    brand_href="/Users/martin/myprojects/microsoft_risk/microsoft-risk/visuals/logo.png",
    color="primary",
    dark=True,
)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

app.layout = html.Div([
    
    navbar,
    
    dcc.Tabs([
        dcc.Tab(label='Visualization', children=[
            dcc.Graph(id='graph-with-slider'),
            dcc.Slider(
                0,
                23,
                step=None,
                value=15,
                marks={str(i): str(i) for i in range(0, 24)},
                id='hour-slider'
            )   
        ]),
        dcc.Tab(label='Tab two', children=[
            dcc.Graph(
                id = 'example_graph',
                figure = fig,
            )
        ]),
    ])

])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('hour-slider', 'value'))
def update_figure(selected_hour):
    
    input = selected_hour

    temp_df = df_forecast.copy()

    temp_df.loc[input,['catboost', 'et', 'rf', 'xgboost', 'lightgbm', 'dt']] = df_forecast.loc[input,'LMP']

    fig_forecast = px.line(temp_df.iloc[input:23].drop(['dt', 'LMP'], axis=1))
    fig_forecast.add_trace(go.Scatter(x=temp_df.index, y=temp_df['LMP'].iloc[0:input+1]))

    fig_forecast.update_layout(transition_duration=500)

    return fig_forecast


if __name__ == '__main__':
    app.run_server(debug=True)
