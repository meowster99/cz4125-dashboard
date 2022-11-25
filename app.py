from dash import Dash, html, dcc, Input, Output, dash_table
import dash
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.colors import n_colors
import re
import random
import styles, utils
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
      className='scroller',
      children=[
        html.Div(
          className='content-box-sidebar',
          children=[
            html.Div(
            className='',
            children=[
              html.H2(
                'Top Economic Events',
                className='content-box-header row',
              ),
              html.Div(
                className='filter-options',
                children=[
                  dcc.Dropdown(
                    style={
                      "width": '420px',
                      'margin-top': '5px',
                    },
                    id="selection_type",
                    value='Known Significant Events',
                    options=['Known Significant Events', 'By Sentiment Techniques', 'By Measures of Economic Dependency',],
                    multi=False,
                  ),
                  html.Div(
                    id='gl_choices',
                    style={
                      'display': 'none'
                    },
                    children=[
                      html.P('News Type: '),
                      dcc.RadioItems(
                        ['Global', 'Local'],
                        'Global',
                        id='navbar_gl',
                      ),
                    ]),
                ]),
              ]),
              html.P(
              'These events are shown in purple on the chart.',
              id='descriptor-text',
              className='subtext'),
              html.Div(id='navbar-content'),
            ]),
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
@app.callback(Output('descriptor-text', 'style'),
              Input('url', 'pathname'))
def render_desription_text(pathname):
  if pathname == '/overview-of-project':
    return {'display': 'none'}
@app.callback(Output('navbar-content', 'children'), 
              Input('selection_type', 'value'), 
              Input('navbar_gl', 'value')
              )
def generate_top_headlines(selection_type, global_local):
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
      if global_local == 'Global':
        return [html.Div(
          className='content-box-list',
          children=[
            html.H3(html.A(global_events['hl'][i] + ' (global)', href=global_events['url'][i], target='_blank')),
            html.P(global_events['date'][i]),
            # html.P(global_events['url'][i]),
          ]
        ) for i in range(len(global_events['hl']))] 
      else:
        return [html.Div(
        className='content-box-list',
        children=[
          html.H3(html.A(local_events['hl'][i] + ' (local)', href=local_events['url'][i], target='_blank')),
          html.P(local_events['date'][i]),
          # html.P(local_events['url'][i]),
        ]
      ) for i in range(len(local_events['hl']))]

@app.callback(Output('gl_choices', 'style'),
          Input('selection_type', 'value'))
def render_navbar_options(selection_type):
  if selection_type == 'Known Significant Events':
    return {'display': 'none'}
  else:
    return {
      'margin-left': '50px',
      'margin-top': '0px',
      'display': 'initial'
      }

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
