from dash import Dash, html, dcc, callback, Output, Input, dash_table
from repository import Repository
import plotly.express as px
import certifi
import os

os.environ['SSL_CERT_FILE'] = certifi.where()

repo = Repository()

query = """
SELECT
  TX_DATE,
  CUST_ENTITY_TYPE,
  CUST_MOBILE_OS,
  LOGIN_TYPE,
  SIT_SITE_ID,
  PLATFORM_ID,
  CUST_DEVICE,
  CUST_TIER,
  CUST_ACCOUNT_MODEL,
  TAG_BUGGED_TRANSACTION,
  LOGIN_SECURITY_POLICY,
  COUNT(DISTINCT tracking_id) AS TXS,
  COUNT(
    DISTINCT CASE
      WHEN FLAG_GRANTED_TX = 1 THEN TRACKING_ID
      ELSE NULL
    END
  ) AS TXS_GRANTED_AGNOSTICO,
  COUNT(
    DISTINCT CASE
      WHEN (
        FLAG_GRANTED_TX = 1
        OR FLAG_RECOVERED_TX = 1
      ) THEN TRACKING_ID
      ELSE NULL
    END
  ) AS TXS_OVERALL_GRANTED,
  COUNT(
    DISTINCT CASE
      WHEN FLAG_GRANTED_TX = 1 THEN TRACKING_ID
      ELSE NULL
    END
  ) AS TXS_GRANTED_RECOVERY,
  COUNT(DISTINCT CUS_CUST_ID) AS USERS, -- Esta es la que va a cambiar el total de usuarios de acuerdo a la agrupación temporal
  COUNT(DISTINCT CONCAT(TX_DATE, CUS_CUST_ID)) AS USERS_DATE,
  COUNT(
    DISTINCT CASE
      WHEN FLAG_GRANTED_TX = 1 THEN CONCAT(TX_DATE, CUS_CUST_ID)
      ELSE NULL
    END
  ) AS USERS_DATE_GRANTED_AGNOSTICO,
  COUNT(
    DISTINCT CASE
      WHEN (
        FLAG_GRANTED_TX = 1
        OR FLAG_RECOVERED_TX = 1
      ) THEN CONCAT(TX_DATE, CUS_CUST_ID)
      ELSE NULL
    END
  ) AS USERS_DATE_GRANTED_OVERALL,
  COUNT(
    DISTINCT CASE
      WHEN FLAG_GRANTED_TX = 1 THEN CONCAT(TX_DATE, CUS_CUST_ID)
      ELSE NULL
    END
  ) AS USERS_DATE_GRANTED_RECOVERY,
FROM
  meli-bi-data.WHOWNER.BT_CRS_LOGIN_TRANSACTIONS
WHERE
  1 = 1
  AND TX_DATE >= CURRENT_DATE - 90
  -- AND PLATFORM_ID = 'mp'
  -- AND SIT_SITE_ID = 'mlb'
GROUP BY
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10,
  11
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
            'Select a site:',
            html.Hr(),
            dcc.Dropdown(df.SIT_SITE_ID.unique(), 'mlb', id='dropdown-selection'),
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
    dff = df[df.SIT_SITE_ID == value]
    # Agrupo por TX_DATE y sumo USERS_DATE
    dff = dff.groupby('TX_DATE').agg({'USERS_DATE': 'sum'}).reset_index()
    return px.line(dff, x='TX_DATE', y='USERS_DATE')


@callback(
    Output('graph-content2', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph2(value):
    dff = df[df.SIT_SITE_ID == value]
    # Agrupo por TX_DATE y sumo TXS
    dff = dff.groupby('TX_DATE').agg({'TXS': 'sum'}).reset_index()
    return px.line(dff, x='TX_DATE', y='TXS')


@callback(
    Output('graph-content3', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph2(value):
    dff = df[df.SIT_SITE_ID == value]
    # Agrupo por TX_DATE y sumo USERS_DATE_GRANTED_OVERALL y USERS_DATE
    dff = dff.groupby('TX_DATE').agg({'USERS_DATE_GRANTED_OVERALL': 'sum', 'USERS_DATE': 'sum'}).reset_index()
    dff["CONVERSION_RATE"] = dff["USERS_DATE_GRANTED_OVERALL"] / dff["USERS_DATE"]
    return px.bar(dff, x='TX_DATE', y='CONVERSION_RATE')


if __name__ == '__main__':
    app.run(debug=True)
