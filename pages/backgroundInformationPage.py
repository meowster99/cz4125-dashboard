"""
Renders the background information about the metric/ prices that we are tracking.
"""

from dash import Dash, html, dcc, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.colors import n_colors
import re
from pages.config.config import YEAR_RANGE
from utils import *

# TODO: @chin voon, move your OTHER trade charts to this page in an organised fashion
dash.register_page(__name__,
                   name='Overview of Project',
                   path='/overview-of-project')
####
objectives = [
  'Visualise and predict future prices',
  'Visualise top news events and analyse the relationship between news sentiments and prices',
  'Visualise and understand Singapores Foreign Economic Dependencies',
  'Visualise Singapores Consumer Price Index over time'
]
methods = ['.']


def layout(prodcode=['Wood']):
  return html.Div(
    className='content-box',
    children=[
      html.H3("Information on our Dashboard"),
      dcc.Markdown(
        'In this project, we developed a data product to help consumers visualise and understand price changes of certain goods and services (G&S) in Singapore. By integrating the data we obtained from conducting the news sentiment analysis, we can further analyse how events around the world affect prices in Singapore, thereby helping us to predict future price changes when a significant event occurs.'
      ),
      html.Div(children=[
        html.P("Objectives:"),
        html.Ul(id='obj-list', children=[html.Li(i) for i in objectives])
      ]),
      html.Div(children=[
        html.P("Methods Employed in our Dashboard"),
        html.Ul(id='methods-list', children=[html.Li(i) for i in methods])
      ]),
      dbc.Row([
        html.H1(children="Geospatial graph of Exports and Imports"),
        dbc.Col([dcc.Dropdown(YEAR_RANGE, 2019, id='year-network-dropdown')],
                style={"width": "25%"}),
        dbc.Col([
          dcc.Dropdown(prodcode, prodcode[0], id='prodcode-network-dropdown')
        ],
                style={"width": "25%"}),
        dbc.Col([
          dcc.RadioItems(
            ['Export', 'Import'], 'Export', id='ind-network-dropdown')
        ],
                style={"width": "25%"}),
      ], ),
      dbc.Row([
        dbc.Row([dcc.Graph(id='geospatial-network')],
                style={
                  'display': 'inline-block',
                  "margin": 0,
                  'width': '50%'
                }),
        dbc.Row([dcc.Graph(id='sunburst')],
                style={
                  'display': 'inline-block',
                  "margin": 0,
                  'width': '50%'
                }),
      ], ),
      dbc.Row([
        html.H1(children="Percentage of Exports and Imports"),
        dbc.Row([
          dbc.Col(
            [dcc.Dropdown(YEAR_RANGE, 2019, id='year-network-dropdown1')],
            style={"width": "25%"}),
        ]),
      ], ),
      dbc.Row([
        dbc.Col(dcc.Graph(id="pie-graph-tradereliance")),
      ], ),
      dbc.Row([
        html.H1(children="Exports and Imports over time"),
        dbc.Col([
          dcc.Dropdown(country_list, 'Malaysia', id='country-lineg-dropdown')
        ],
                style={"width": "25%"}),
      ], ),
      dbc.Row([
        dbc.Row([dcc.Graph(id="line-graph-trade")],
                style={
                  'display': 'inline-block',
                  "margin": 0,
                  'width': '100%'
                }),
      ], ),
      dbc.Row([
        dbc.Col([dcc.Dropdown(prodcode, prodcode[0], id='pc-lineg-dropdown')],
                style={"width": "25%"}),
      ], ),
      dbc.Row([
        dbc.Col([
          dcc.RadioItems(['Top 5', 'Top 10', "All"],
                         'Top 5',
                         id="checklist-pc",
                         inline=True)
        ],
                style={"width": "25%"}),
        dbc.Row([dcc.Graph(id="pc-line-graph-trade")],
                style={
                  'display': 'inline-block',
                  "margin": 0,
                  'width': '100%'
                }),
      ], ),
      dbc.Row([
        html.H1(children="Products traded in Singapore"),
        dbc.Row([dcc.Graph(id="line-graph-timeseries")],
                style={
                  'display': 'inline-block',
                  "margin": 0,
                  'width': '100%'
                }),
        dbc.Col([
          dcc.Checklist(id="checklist",
                        options=b.product_codes(),
                        value=["Fuels", "Manufactures"],
                        inline=True)
        ],
                style={
                  "width": "25%",
                  'display': 'inline-block'
                }),
      ], ),
      dbc.Row([
        html.H1(children="Trading partners of Singapore"),
        dbc.Col([
          dcc.RadioItems(['Top 5', 'Top 10', "All"],
                         'Top 5',
                         id="c-checklist-pc",
                         inline=True)
        ],
                style={"width": "25%"}),
        dbc.Row([dcc.Graph(id="c-line-graph-timeseries")],
                style={
                  'display': 'inline-block',
                  "margin": 0,
                  'width': '100%'
                }),
        dbc.Row([dash_table.DataTable(id="tbl", columns=df_col)])
      ], ),
    ])
