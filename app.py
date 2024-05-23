from dash import Dash, html, dcc, callback, Output, Input, dash_table
from repository import Repository
import plotly.express as px
import certifi
import os

os.environ['SSL_CERT_FILE'] = certifi.where()

repo = Repository()

query = """
SELECT * FROM meli-sbox.ITLOGINMETRICS.TEST_PLOTLY_APP
"""

df = repo.get_data(query)

# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(external_stylesheets=external_stylesheets)


app.layout = [
    html.Div(
        className='row',
        children=[
            'My First App with Data, Graph, and Controls',
            html.Hr(),
            html.H2(children='Dataset', style={'textAlign': 'center', 'fontSize': 24}),
            dash_table.DataTable(data=df.to_dict('records'), page_size=10, style_table={'textAlign': 'center', 'fontSize': 12}),
        ],
        style={
            'textAlign': 'center',
            'color': 'black',
            'fontSize': 24
        }
    ),
    html.Hr(),
    html.Div(
        className='row',
        children=[
            'Select a country:',
            html.Hr(),
            dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
            dcc.Graph(id='graph-content'),
            dcc.Graph(id='graph-content2'),
            dcc.Graph(id='graph-content3')
            ],
        style={
            'textAlign': 'center',
            'fontSize': 24
        }
    ),
    html.Hr(),
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
