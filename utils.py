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
import numpy as np
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import pickle
from src.trade import TradeStat, UnifiedStats


TRADE_DATA = './data/trade_data/trade_data.pkl'

with open(TRADE_DATA, 'rb') as inp:
  s = pickle.load(inp)
b = UnifiedStats()
b.extend(s)
b.filter()

techniques = ['Anomaly Detection', 'Event Tagging', 'Change Point Detection']
energy_list = ["Fuels", "Minerals", "Ores and Metals"]
grocery_list = ["Food", "Agricultural Raw Materials", "Animals", "Food Products"]
cpi_list = ['Food']
trade_list = list(set(energy_list + grocery_list + cpi_list))
full_list = b.product_codes()
pc_list = [pc for pc in full_list if pc not in trade_list]

all_countries = b.countries
country_list = [country.name for country in all_countries]

# --- exports/imports table ---
df_col = [{
  "name": "Import country",
  'id': 'country_im'
}, {
  "name": "Imports (US$ Thousands)",
  'id': 'import-data'
}, {
  "name": "Export country",
  'id': 'country_ex'
}, {
  "name": "Exports (US$ Thousands)",
  'id': 'export-data'
}]

# regression models function
def ses(y, n):
  fit1 = SimpleExpSmoothing(y, initialization_method="estimated").fit()
  fcast1 = fit1.forecast(n).rename("SES")
  fit2 = Holt(y, initialization_method="estimated").fit()
  fcast2 = fit2.forecast(n).rename("Holt's")
  fit3 = Holt(y, exponential=True, initialization_method="estimated").fit()
  fcast3 = fit3.forecast(n).rename("Exponential")
  fit4 = Holt(y, damped_trend=True,
              initialization_method="estimated").fit(damping_trend=0.98)
  fcast4 = fit4.forecast(n).rename("Additive Damped")
  fit5 = Holt(y,
              exponential=True,
              damped_trend=True,
              initialization_method="estimated").fit()
  fcast5 = fit5.forecast(n).rename("Multiplicative Damped")

  fcast = pd.DataFrame()
  fcast['SES'] = fcast1
  fcast["Holt's"] = fcast2
  fcast['Exponential'] = fcast3
  fcast['Additive Damped'] = fcast4
  fcast['Multiplicative Damped'] = fcast5
  fcast = fcast.reset_index()

  return fcast


def prepare_for_plotting(df, date_col, format=None, to_datetime=True):
  if to_datetime:
    df[date_col] = pd.to_datetime(df[date_col],
                                  format=format).dt.to_period('M')
  df = df.rename({date_col: 'date'}, axis=1)
  return df


def get_tagged_df(global_local_choice):
  return pd.read_csv('data/news_data/tagged_df_global.csv'
                     ) if global_local_choice == "Global" else pd.read_csv(
                       'data/news_data/tagged_df_local.csv')


def display_tagged_events(global_local_choice, df: pd.DataFrame = None):
  if global_local_choice == "Global":
    tagged_global_events = pd.read_csv('data/news_data/tagged_df_global.csv')
    event_df = tagged_global_events.copy()
    event_df = event_df.rename({'url': 'links'}, axis=1)
  else:
    tagged_local_events = pd.read_csv('data/news_data/tagged_df_local.csv')
    event_df = tagged_local_events.copy()
  try:
    event_df = prepare_for_plotting(event_df, 'published_on', to_datetime=True)
  except:
    event_df = prepare_for_plotting(event_df,
                                    'published_on',
                                    to_datetime=False)
  event_df.date = event_df.date.astype(str)
  df.date = df.date.astype(str)
  if df is not None:
    merged_df = pd.merge(
      df,
      event_df[['query_term', 'true_headline', 'date', 'links', 'event_tag']],
      on='date',
      how='right')
    return merged_df
  return event_df


def load_news_sentiments_datasets(global_local_choice):
  if global_local_choice == "Global":
    return pd.read_csv('data/anomaly_data/anomaly_global.csv')
  else:
    return pd.read_csv('data/anomaly_data/anomaly_local.csv')

def load_changepoint_datasets(global_local_choice):
    return pd.read_csv('data/changepoints_data/changepoints_local.csv') if global_local_choice == "Local" else pd.read_csv('data/changepoints_data/changepoints_local.csv')

def filter_by_query_term(global_local_choice, sentiment_df, filters):
  tagged_df = get_tagged_df(global_local_choice)
  tagged_df = tagged_df.rename({'published_on': 'date'}, axis=1)
  tagged_df['date'] = pd.to_datetime(tagged_df['date']).astype(str)
  tagged_df['query_term'] = tagged_df['query_term'].str.strip()
  merged_df = pd.merge(tagged_df, sentiment_df, on='date',
                       how='right').query('query_term in @filters')
  return merged_df

def get_technique_information(detection_method):
  if detection_method == 'Anomaly Detection':
    return html.P('Employs the LevelShiftAD detector to track the difference between median values at two sliding windows of size 30 thus identifying the anomalies across datapoints.', className='subtext')
  elif detection_method == 'Event Tagging':
    return html.P('Various macroeconomic events mentioned in the relevant news articles have been labelled on the chart.', className='subtext')
  elif detection_method == 'Change Point Detection':
    return html.P('Uses the Pruned Exact Linear Time algorithm to detect change points', className='subtext')
  

def add_sentiment_traces(target_col, temp_sentiment_df, merged_df, global_local_choice,
                         detection_method, fig):
  if detection_method == 'Anomaly Detection':
    temp_sentiment_df['anomaly'] = temp_sentiment_df['anomaly'].map({
      0:
      'rgba(135, 206, 250, 0.0)',
      2:
      styles.colors['red']
    })
  else:
    temp_sentiment_df['anomaly'] = temp_sentiment_df['anomaly'].map({
      0:
      'rgba(135, 206, 250, 0.0)',
      2:
      'rgba(135, 206, 250, 0.0)'
    })

  colors = [
    styles.colors['yellow'], styles.colors['lightblue'], styles.colors['green']
  ]
  temp_sentiment_df['vader_result_body_x'] = temp_sentiment_df[
    'vader_result_body_x'].map({
      0: 'negative',
      1: 'neutral',
      2: 'positive'
    })
  for i, group in enumerate(temp_sentiment_df.groupby('vader_result_body_x')):
    fig.add_trace(go.Scatter(
      x=group[1].date.astype(str),
      y=group[1]['count'],
      mode='lines+markers',
      line_color=colors[i],
      name=group[0],
      text=group[1]['vader_result_body_x'],
      hovertemplate="%{y} counts of %{text} sentiment<extra></extra>",
      marker_color=temp_sentiment_df['anomaly'],
      legendgroup='Sentiment',
      legendgrouptitle_text="Sentiment"),
                  row=2,
                  col=1)

  if detection_method == 'Event Tagging':
    colorScale = px.colors.qualitative.G10
    for i, group in enumerate(merged_df.groupby('event_tag')):
      # for x in group[1].date.astype(str):
      #   fig.add_vline(x=x, line_width=5, line_color=colorScale[i], opacity=0.3)
      fig.add_trace(go.Scatter(
        x=group[1].date.astype(str),
        y=group[1][target_col],
        name=group[0],
        text=group[1].event_tag,
        mode='markers',
        marker_color=colorScale[i],
        hovertemplate="<b>%{x}:</b> %{text}<extra></extra>",
        legendgroup='Macro Events',
        legendgrouptitle_text="Macro Events"),
                    row=1,
                    col=1)

    fig.update_layout(showlegend=True)

  if detection_method == 'Change Point Detection':
    changepoints = load_changepoint_datasets(global_local_choice)
    changepoints = changepoints.drop(changepoints.columns[[0]],axis = 1)
    changepoints.columns =['Change']
    changepoints["Change"] = changepoints["Change"].astype('str')
    changepoints = list(changepoints['Change'])
    for x in changepoints:
      fig.add_vline(x= x, line_width=5, line_color="red", opacity=0.3)

                                    
  fig['layout']['yaxis2'].update(title='Volume of Sentiment')

  fig['layout']['xaxis2'].update(rangeslider_visible=True,
                                 rangeslider_thickness=0.1)
                           
  fig.update_layout(legend=dict(groupclick="toggleitem"),)
                           
  return fig