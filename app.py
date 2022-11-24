from dash import Dash, html, dcc, Input, Output, dash_table
import dash
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.colors import n_colors
import re
import random
import styles
from utils import pc_list, cpi_list, energy_list, grocery_list
import utils

app = Dash(__name__, )
server = app.server
app.config.suppress_callback_exceptions = True

from pages import consumerPricesPage, backgroundInformationPage, energyPricesPage, wageTrackerPage, groceryPricesPage, tradePage

consumer_prices_page_layout = consumerPricesPage.layout(prodcode=cpi_list)
energy_prices_layout = energyPricesPage.layout(prodcode=energy_list)
wage_tracker_layout = wageTrackerPage.layout()
background_information_layout = backgroundInformationPage.layout(prodcode=pc_list)
grocery_prices_layout = groceryPricesPage.layout(prodcode=grocery_list)

# ------------ APP LAYOUT -----------------
app.layout = html.Div(
  className='complete-background',
  children=[
    dcc.Location(id='url', refresh=False),
    html.Div(
      className='scroller',
      children=[
        html.Div(
          className='content-box-sidebar',
          children=html.Div(
            className='',
            children=[
              html.H2(
                'Top Economic Events',
                className='content-box-header row',
              ),
              dcc.Dropdown(
               id="selection_type",
               value='Known Significant Events',
               options=['Known Significant Events', 'By Sentiment Techniques', 'By Measures of Economic Dependency',],
               multi=False,
              ),
              html.Div(id='navbar-content')
            ],
          )),
      ]),
    html.Div(
      className='dashboard-header',
      children=[
        html.H1('Singapore Economic Tracker'),
        html.Div(
          style={'display': 'inline flex'},
          children=[
            html.Div(children=dcc.Link(f"{page['name']}",
                                       className='default-button navbar-link',
                                       href=page["relative_path"]))
            for page in dash.page_registry.values()
          ]),
      ]),
    html.Div(className='main-content-wrapper',
             children=[
               html.Div(
                 id='page-content',
                 className='body-content-wrapper',
               )
             ])
  ])

# ------------ NAVBAR LAYOUT --------------
@app.callback(Output('navbar-content', 'children'), Input('selection_type', 'value'))
def generate_top_headlines(selection_type):
    if selection_type == 'Known Significant Events':
      events = utils.get_top_headlines(selection_type)
      return [html.Div(
        className='content-box-list',
        children=[
          html.Div(
            # style={'display': 'inline-flex'},
            children=[
              html.H3(html.A(events['hl'][i], href=events['url'][i], target='_blank')),
              html.P(events['date'][i], style={'justify-self': 'end'}),
            ]),
          # html.A(events['url'][i]),
        ]
      ) for i in range(len(events['hl']))]
    else:
      global_events, local_events = utils.get_top_headlines(selection_type)
      return [html.Div(
        className='content-box-list',
        children=[
          html.H3(html.A(global_events['hl'][i] + ' (global)', href=global_events['url'][i], target='_blank')),
          html.P(global_events['date'][i]),
          # html.P(global_events['url'][i]),
        ]
      ) for i in range(len(global_events['hl']))] 
      + [html.Div(
        className='content-box-list',
        children=[
          html.H3(html.A(local_events['hl'][i] + ' (local)', href=local_events['url'][i], target='_blank')),
          html.P(local_events['date'][i]),
          # html.P(local_events['url'][i]),
        ]
      ) for i in range(len(local_events['hl']))]


# # ----------- PAGE NAVIGATION -------------
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
  if pathname == '/consumer-prices-tracker':
    return consumer_prices_page_layout
  elif pathname == '/energy-prices-tracker':
    return energy_prices_layout
  elif pathname == '/wage-tracker':
    return wage_tracker_layout
  elif pathname == '/grocery-prices-tracker':
    return grocery_prices_layout
  elif pathname == '/overview-of-project':
    return background_information_layout


# ------------- RUN APP -------------------
if __name__ == '__main__':
  app.run_server(debug=True)
