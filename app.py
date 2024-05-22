from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import certifi
import os

os.environ['SSL_CERT_FILE'] = certifi.where()

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

app.layout = [
    html.H1(children='My first dash in Plotly Dash', style={'textAlign': 'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content'),
    dcc.Graph(id='graph-content2'),
    dcc.Graph(id='graph-content3')
]


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff, x='year', y='pop')


@callback(
    Output('graph-content2', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph2(value):
    dff = df[df.country == value]
    return px.line(dff, x='year', y='lifeExp')


@callback(
    Output('graph-content3', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph2(value):
    dff = df[df.country == value]
    return px.bar(dff, x='year', y='gdpPercap')


if __name__ == '__main__':
    app.run(debug=True)
