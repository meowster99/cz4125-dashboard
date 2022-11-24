"""
Renders the energy pricing information/ related charts on the page.
"""

import re

import dash
import dash_daq as daq
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dash_table, dcc, html
from plotly.colors import n_colors
from plotly.subplots import make_subplots
from statsmodels.tsa.api import ExponentialSmoothing, Holt, SimpleExpSmoothing

import styles
import utils
from pages.config.config import YEAR_RANGE

 # TODO: @chin voon, move your geospatial trade charts related to energy here


dash.register_page(__name__,
                   name='Energy Prices',
                   path='/energy-prices-tracker')

####### DATA #######
energy = pd.read_csv('data/monthly_avg_energy_price.csv')
slider_years = utils.prepare_for_plotting(
  energy, 'Data Series')['date'].astype(str).to_list()

filter = [
  'energy', 'energy crisis', 'electricity prices', 'war', 'tsunami',
  'hurricane', 'natural disaster', 'nuclear disaster', 'pandemic', 'recession',
  'covid', 'inflation'
]


def ses(y):
  # fitting SES
  fit1 = SimpleExpSmoothing(y, initialization_method="estimated").fit()
  fcast1 = fit1.forecast(100).rename("SES")
  fit2 = Holt(y, initialization_method="estimated").fit()
  fcast2 = fit2.forecast(100).rename("Holt's")
  fit3 = Holt(y, exponential=True, initialization_method="estimated").fit()
  fcast3 = fit3.forecast(100).rename("Exponential")
  fit4 = Holt(y, damped_trend=True,
              initialization_method="estimated").fit(damping_trend=0.98)
  fcast4 = fit4.forecast(100).rename("Additive Damped")
  fit5 = Holt(y,
              exponential=True,
              damped_trend=True,
              initialization_method="estimated").fit()
  fcast5 = fit5.forecast(100).rename("Multiplicative Damped")
  fcast = pd.DataFrame()
  fcast['SES'] = fcast1
  fcast["Holt's"] = fcast2
  fcast['Exponential'] = fcast3
  fcast['Additive Damped'] = fcast4
  fcast['Multiplicative Damped'] = fcast5
  fcast = fcast.reset_index()
  return fcast


def layout(prodcode=["Fuels"]):
  return html.Div(
    children=[
      html.Div(
        className='content-box',
        children=[
                html.H3('Energy Prices'),
      html.Div(style={'display': 'inline flex'},
               children=[
                 html.Div(style={
                   'margin-left': '900px',
                   'margin-top': '10px'
                 },
                          children=[
                            daq.ToggleSwitch(label='View Predictions?',
                                             id='toggle-prediction',
                                             value=False),
                          ]),
               ]),
      html.Div(
        id='news-analysis-c2',
        children=[
          html.Div(
            #  style={'display': 'inline flex'},
            children=[
              html.P('News Type: '),
              dcc.RadioItems(
                ['Global', 'Local'],
                'Global',
                id='global_local',
              ),
            ]),
          html.Div(style={'padding-top': '10px'},
                   children=[
                     html.P('Analysis Method: '),
                     dcc.Dropdown(
                       id="detection_method",
                       value=utils.techniques[0],
                       options=utils.techniques,
                       multi=False,
                     ),
                     html.Div(id='info-c2'),
                   ]),
        ]),
      dcc.Graph(
        id='energyprices',
        responsive=False,
      ),
      ]),
      html.Div(
        className='content-box',
        children=[
        html.H3(children="Geospatial graph of Exports and Imports"),
        html.Div(children=[
          html.P('Choose Year:'),
          dcc.Dropdown(YEAR_RANGE, 2019, id='year-network-dropdown'),
          html.P('Choose Product:'),
          dcc.Dropdown(prodcode, prodcode[0], id='prodcode-network-dropdown'),
          html.Div(
          style={"width": "25%"},
          children=[
            html.P('Choose Trade Type:'),
            dcc.RadioItems(['Export', 'Import'], 'Export', id='ind-network-dropdown')
          ]),
          ]),
          html.Div(children=[
            dcc.Graph(id='geospatial-network')],),
          ]),
      html.Div(
        className='content-box',
        children=[
        html.H3("Singapore's Bilateral Trade Relations"),
        html.Div(children=[
          dcc.Graph(id='sunburst')],),
      ]),
    ])


@callback(Output('news-analysis-c2', 'style'),
          Input('toggle-prediction', 'value'))
def render_callbacks(predict):
  if predict:
    return {'display': 'none'}
  else:
    return {'display': 'initial'}


@callback(Output('info-c2', 'children'), Input('detection_method', 'value'))
def render_information(detection_method):
  return utils.get_technique_information(detection_method)


@callback(Output('energyprices', 'figure'), Input('global_local', 'value'),
          Input('toggle-prediction', 'value'),
          Input('detection_method', 'value'))
def energyprices(global_local_choice, predict, detection_method):
  df = energy.copy()

  if predict:
    fig = go.Figure()
    legend_title = 'Model'
    height = styles.HEIGHT1
    years = df['Data Series']
    data = df['Energy (Cents Per Kilowatt Hour)'].tolist()
    index = pd.date_range(start="2012", end="2023", freq="M")
    y = pd.Series(data, index)
    reg = ses(y)

    fig.add_trace(
      go.Scatter(
        x=index,
        y=y,
        name="Energy Prices"  # this sets its legend entry
      ))
    j = 0
    for i in range(1, 6):
      fig.add_traces(
        go.Scatter(x=reg['index'],
                   y=reg.iloc[:, i],
                   mode='lines',
                   name=reg.columns[i],
                   line=dict(color=px.colors.qualitative.Plotly[j])))
      j = j + 1
    fig.update_layout(height=height,
                      legend_title=legend_title,
                      showlegend=True)

  else:
    height = styles.HEIGHT2
    fig = make_subplots(rows=2, cols=1, vertical_spacing=styles.VERT_SPACING, shared_xaxes=True)

    # loading and getting the data for the plot
    sentiment_df = utils.load_news_sentiments_datasets(global_local_choice)
    try:
      df = utils.prepare_for_plotting(df, 'Data Series', to_datetime=True)
    except:
      df = utils.prepare_for_plotting(df, 'Data Series', to_datetime=False)
    # df = df[df.date>'2010-01']
    merged_df = utils.display_tagged_events(global_local_choice, df)
    sentiment_df = utils.filter_by_query_term(global_local_choice,
                                              sentiment_df, filter)
    sentiment_df = utils.prepare_for_plotting(sentiment_df, 'date')
    temp_sentiment_df = pd.DataFrame(
      sentiment_df.groupby(['date', 'vader_result_body_x'
                            ])['true_headline'].count()).reset_index().rename(
                              {'true_headline': 'count'}, axis=1)
    temp_sentiment_df['anomaly'] = sentiment_df.groupby(
      ['date', 'vader_result_body_x'])['anomaly'].max().values

    fig.add_trace(go.Scatter(x=df.date.astype(str),
                             y=df['Energy (Cents Per Kilowatt Hour)'],
                             name='Energy (cents per kwh)',
                             marker_color=styles.colors['blue']),
                  row=1,
                  col=1)

    fig = utils.add_sentiment_traces('Energy (Cents Per Kilowatt Hour)',
                                     temp_sentiment_df, merged_df,
                                     global_local_choice, detection_method,
                                     fig)

    # fig.update_xaxes(rangeslider_visible=True, )
    fig.update_xaxes(range=['2012-01', '2021-10'])
    fig['layout']['yaxis1'].update(title='Energy Prices (cents per kwh)')
    fig.update_layout(height=height, )

  fig.update_layout(
    font=dict(
        size=10,
    ),
    title="Energy Prices",
    width=styles.WIDTH,
    height=height,
    template='plotly_white',
    font_family="Lexend",
  )

  return fig
