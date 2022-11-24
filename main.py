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
      className='scroller content-box-sidebar',
      children=[
        html.Div(
          # className='content-box-sidebar',
          children=html.Div(
            className='',
            children=[
              html.H2(
                'Top Economic Events',
                className='content-box-header row',
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
navbar_layout = html.Div(children=[
  html.P(
    'Top Economic Events',
    className='subtext row content-box-list',
  ),
  html.Div(className='container-column', children=[]),
])


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
  app.run_server(host='0.0.0.0', port=random.randint(2000, 9000), debug=True)
