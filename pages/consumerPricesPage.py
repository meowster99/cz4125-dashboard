"""
Renders the CPI information/ related charts on the page.
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

# TODO: @chin voon, move your geospatial trade charts related to CPI here

dash.register_page(__name__,
                   name='Consumer Price Index',
                   path='/consumer-prices-tracker')

####### DATA #######
cpidf = pd.read_csv('data/CPI_categories_from_1961.csv')
cpicatoptions = cpidf.level_2.unique()

query_mapper = {
  'Food': [
    'inflation', 'energy crisis', 'recession', 'embargo', 'covid', 'war',
    'export prices', 'import prices', 'grocery prices', 'electricity prices',
    'pandemic', 'recession'
  ],
  'Food Excl Food Serving Services': [
    'inflation', 'energy crisis', 'recession', 'embargo', 'covid', 'war',
    'export prices', 'import prices', 'grocery prices', 'electricity prices',
    'pandemic', 'recession'
  ],
  'Food Serving Services': [
    'inflation', 'energy crisis', 'recession', 'embargo', 'covid', 'war',
    'export prices', 'import prices', 'grocery prices', 'electricity prices',
    'pandemic', 'recession'
  ],
  'Housing & Utilities': [
    'inflation', 'housing crisis', 'energy crisis', 'tsunami', 'recession',
    'embargo', 'covid', 'war', 'housing', 'energy', 'electricity prices',
    'pandemic', 'recession'
  ],
  'Transport': [
    'inflation', 'energy crisis', 'recession', 'covid', 'war', 'energy',
    'electricity prices', 'pandemic', 'recession'
  ],
}


####### LAYOUT #######
def layout(prodcode=['Food']):
  return html.Div(
    children=[
      html.Div(
        className='content-box',
        children=[
              html.H3('Consumer Price Index Tracker'),
      html.Div(
        className='filter-options',
        children=[
          dcc.Dropdown(
            style={
              "width": '400px',
              'margin-top': '5px'
            },
            id="slct_cpicat",
            className='dropdown-maincat',
            value='Food',
            options=cpicatoptions,
            multi=False,
          ),
          html.Div(children=[
            html.Div(
              style={
                'margin-left': '550px',
                'margin-top': '10px'
              },
              children=[
                daq.ToggleSwitch(
                  label='View Predictions?',
                  id='toggle-prediction',
                  size=40,
                  # labelPosition='right',
                  value=False),
              ]),
          ]),
        ]),
      html.Div(
        # className='filter-options',
        style={'display': 'inline-flex'},
        id='news-analysis-c1',
        children=[
          html.Div(children=[
            html.P('News Type: '),
            dcc.RadioItems(
              ['Global', 'Local'],
              'Global',
              id='global_local',
            ),
          ]),
          html.Div(
            style={'padding-top': '10px'},
            children=[
              html.P('Analysis Method: '),
              dcc.Dropdown(
                # style={
                # "width": '400px',
                # 'margin-top': '5px'
                # },
                id="detection_method",
                value=utils.techniques[0],
                options=utils.techniques,
                multi=False,
              ),
              html.Div(id='info-c1'),
            ]),
        ]),
      dcc.Graph(
        id='cpival',
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


@callback(Output('news-analysis-c1', 'style'),
          Input('toggle-prediction', 'value'))
def render_callbacks(predict):
  if predict:
    return {'display': 'none'}
  else:
    return {'display': 'initial'}


@callback(Output('info-c1', 'children'), Input('detection_method', 'value'))
def render_information(detection_method):
  return utils.get_technique_information(detection_method)


@callback(Output('cpival', 'figure'), Input('global_local', 'value'),
          Input('slct_cpicat', 'value'), Input('toggle-prediction', 'value'),
          Input('detection_method', 'value'), Input('selection_type', 'value'), 
              Input('navbar_gl', 'value'))
def cpi(global_local_choice, maincat, predict, detection_method, selection_type, navbar_gl):
  df = cpidf.copy()
  df['value'] = df['value'].apply(lambda x: np.nan if x == ' ' else x)
  df = df.dropna()
  df = df[df['level_2'] == maincat]
  df['value'] = df['value'].astype(float)

  if predict:
    legend_title = 'Model'
    height = styles.HEIGHT1
    df = df.replace(
      r'^\s*$', 1, regex=True
    )  # replace with 1 bc Holt's method needs positive non zero value

    data = df['value'].tolist()
    index = pd.date_range(start="1961", end="2021-11", freq="M")
    y = pd.Series(data, index).interpolate(method='linear')

    fig = go.Figure()
    fig.add_trace(
      go.Scatter(
        x=index,
        y=data,
        mode='lines',
        name=str(maincat),
      ), )

    reg = utils.ses(y, 200)
    for i in range(1, 6):
      fig.add_traces(
        go.Scatter(x=reg['index'],
                   y=reg.iloc[:, i],
                   mode='lines',
                   name=reg.columns[i],
                   line=dict(color=px.colors.qualitative.Light24[i - 1])))
    fig.update_layout(height=height,
                      legend_title=legend_title,
                      showlegend=True)

  else:
    legend_title = 'Macro Event'
    height = styles.HEIGHT2
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0, shared_xaxes=True)

    sentiment_df = utils.load_news_sentiments_datasets(global_local_choice)
    try:
      df = utils.prepare_for_plotting(df, 'month', to_datetime=True)
    except:
      df = utils.prepare_for_plotting(df, 'month', to_datetime=False)
    # df = df[df.date > '2010-01']

    merged_df = utils.display_tagged_events(global_local_choice, df)
    # merged_df['value'] = merged_df['value'].max()

    sentiment_df = utils.filter_by_query_term(global_local_choice,
                                              sentiment_df,
                                              query_mapper[maincat])
    sentiment_df = utils.prepare_for_plotting(sentiment_df, 'date')
    temp_sentiment_df = pd.DataFrame(
      sentiment_df.groupby(['date', 'vader_result_body_x'
                            ])['true_headline'].count()).reset_index().rename(
                              {'true_headline': 'count'}, axis=1)
    temp_sentiment_df['anomaly'] = sentiment_df.groupby(
      ['date', 'vader_result_body_x'])['anomaly'].max().values

    fig.add_trace(go.Scatter(x=df.date.astype(str),
                             y=df['value'],
                             name='CPI value',
                             marker_color=styles.colors['blue']),
                  row=1,
                  col=1)
    if detection_method != 'Change Point Detection':
      dates_yearly, dates_monthly = utils.read_price_change_data(
        'cpi', maincat, [], detection_method)
      fig = utils.render_significant_dates(fig,
                                      dates_monthly,
                                      detection_method,
                                      color=styles.colors['orange'])
      
    elif detection_method == 'Change Point Detection':
      dates_yearly = utils.read_price_change_data(
        'cpi', maincat, [], detection_method)
    fig = utils.render_significant_dates(fig,
                                          dates_yearly,
                                          detection_method,
                                          color=styles.colors['otherred'])
      
    fig = utils.add_sentiment_traces('value', temp_sentiment_df, merged_df,
                                     global_local_choice, detection_method,
                                       fig)
    headlines, main_dates = utils.view_events_on_chart(fig, selection_type, navbar_gl)
    fig = utils.render_significant_dates(fig, main_dates, '', styles.colors['purple'])

    # fig.update_xaxes(rangeslider_visible=True, )
    fig.update_xaxes(range=['2012-01', '2021-10'])
    fig['layout']['yaxis1'].update(title='CPI')
    fig.update_layout(height=height, )

  fig.update_layout(
    font=dict(size=10, ),
    legend=dict(groupclick="toggleitem"),
    title="CPI of " + maincat,
    width=styles.WIDTH,
    template='plotly_white',
    font_family="Lexend",
  )

  return fig
