"""
Renders the grocery pricing information/ related charts on the page.
"""

from dash import Dash, html, dcc, Input, Output, dash_table, callback
import dash
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.colors import n_colors
import numpy as np
import dash_daq as daq
import utils, styles
from pages.config.config import YEAR_RANGE

# TODO: @chin voon, move your geospatial trade charts related to groceries here

dash.register_page(__name__,
                   name='Grocery Prices',
                   path='/grocery-prices-tracker')

####### DATA #######
groceries = pd.read_csv('data/grocery_prices_2010_2021.csv')
maincatoptions = groceries.maincat.unique()

filter = [
  'covid',
  'export prices',
  'import prices',
  'grocery prices',
  'pandemic',
  'recession',
  'inflation',
  'embargo',
]


####### LAYOUT #######
def layout(prodcode=["Food"]):
  return html.Div(
    className='content-box',
    children=[
      html.H3('Grocery Price Tracker'),
      html.Div(
        className='filter-options',
        children=[
          dcc.Dropdown(
            style={
              "width": '400px',
              'margin-top': '5px'
            },
            id="slct_maincat",
            className='dropdown-maincat',
            value='Bread',
            options=maincatoptions,
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
        id='news-analysis-c3',
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
                     html.Div(id='info-c3'),
                   ]),
        ]),
      dcc.Graph(id='grocprices', ),
      html.Div(style={"width": "25%"},
               children=[
                 html.H1(children="Geospatial graph of Exports and Imports"),
                 html.Div(
                   style={"width": "25%"},
                   children=[
                     dcc.Dropdown(YEAR_RANGE, 2019, id='year-network-dropdown')
                   ],
                 ),
                 html.Div(
                   style={"width": "25%"},
                   children=[
                     dcc.Dropdown(prodcode,
                                  'Food',
                                  id='prodcode-network-dropdown')
                   ],
                 ),
                 html.Div(children=[
                   dcc.RadioItems(['Export', 'Import'],
                                  'Export',
                                  id='ind-network-dropdown')
                 ], ),
               ]),
      html.Div([
        html.Div(
          style={
            'display': 'inline-block',
            "margin": 0,
            'width': '50%'
          },
          children=[dcc.Graph(id='geospatial-network')],
        ),
        html.Div(
          style={
            'display': 'inline-block',
            "margin": 0,
            'width': '50%'
          },
          children=[dcc.Graph(id='sunburst')],
        )
      ])
    ])


@callback(Output('news-analysis-c3', 'style'),
          Input('toggle-prediction', 'value'))
def render_callbacks(predict):
  if predict:
    return {'display': 'none'}
  else:
    return {'display': 'initial'}


@callback(Output('info-c3', 'children'), Input('detection_method', 'value'))
def render_information(detection_method):
  return utils.get_technique_information(detection_method)


@callback(Output('grocprices', 'figure'), Input('slct_maincat', 'value'),
          Input('global_local', 'value'), Input('toggle-prediction', 'value'),
          Input('detection_method', 'value'))
def grocgraph(maincat, global_local_choice, predict, detection_method):
  df = groceries.copy()
  df = df[df['maincat'] == maincat]

  if predict:
    fig = go.Figure()
    legend_title = 'Subcategories'
    height = styles.HEIGHT1
    years = pd.date_range(start="2010", end="2022", freq="A")
    j = 0
    for i in df['subcat'].unique():
      newdf = df[df['subcat'] == i]
      fig.add_trace(
        go.Scatter(x=years,
                   y=newdf["value"],
                   mode='lines+markers',
                   name=str(i),
                   line=dict(color=px.colors.qualitative.Light24[j])), )

      data = newdf["value"].replace(np.nan, 1).tolist()
      index = pd.date_range(start="2010", end="2022", freq="A")
      y = pd.Series(data, index)
      y = y.interpolate(method='linear')

      reg = utils.ses(y, 10)
      fig.add_traces(
        go.Scatter(x=reg['index'],
                   y=reg['Exponential'],
                   mode='lines',
                   name=i + ' SES-10 years',
                   line=dict(color=px.colors.qualitative.Light24[j])))
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
      df = utils.prepare_for_plotting(df,
                                      'year',
                                      format='%Y',
                                      to_datetime=True)
    except:
      df = utils.prepare_for_plotting(df,
                                      'year',
                                      format='%Y',
                                      to_datetime=False)
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

    j = 0
    for i in df['subcat'].unique():
      newdf = df[df['subcat'] == i]
      fig.add_trace(go.Scatter(
        x=newdf.date,
        y=newdf['value'],
        mode='lines+markers',
        name=str(i),
        line=dict(color=px.colors.qualitative.Light24[j]),
        legendgroup='Item Category',
        legendgrouptitle_text="Item Category"),
                    row=1,
                    col=1)
      j += 1

    fig = utils.add_sentiment_traces('value', temp_sentiment_df, merged_df,
                                     global_local_choice, detection_method,
                                     fig)

    # fig.update_xaxes(rangeslider_visible=True, )
    fig.update_xaxes(range=['2010-01', '2021-01'])
    fig['layout']['yaxis1'].update(title='Grocery Prices')
    fig.update_layout(height=height, )

  fig.update_layout(
    font=dict(size=10, ),
    title="Grocery Prices",
    width=styles.WIDTH,
    height=height,
    template='plotly_white',
    font_family="Lexend",
  )
  return fig
