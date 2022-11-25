import re

import dash
import dash_daq as daq
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dash_table, dcc, html
from plotly.colors import n_colors
from plotly.subplots import make_subplots

import styles
import utils

dash.register_page(__name__, name='Wages', path='/wage-tracker')
filter = [
  'covid',
  'pandemic',
  'recession',
  'inflation',
  'war',
]

wages = pd.read_csv('data/median_annual_salary_by_industry.csv')
industry = [
  'Real Wage vs Average Wage',
  'Managers & Administrators (Including Working Proprietors)', 'Professionals',
  'Associate Professionals & Technicians', 'Clerical Support Workers',
  'Service & Sales Workers', 'Craftsmen & Related Trades Workers',
  'Plant & Machine Operators & Assemblers',
  'Cleaners, Labourers & Related Workers'
]


def layout():
  return html.Div(
    className='content-box',
    children=[
      html.H3('Wage Tracker'),
      html.Div(
        className='filter-options',
        children=[
          dcc.Dropdown(
            style={
              "width": '400px',
              'margin-top': '5px'
            },
            id="slct_industry",
            className='dropdown-industry',
            value='Managers & Administrators (Including Working Proprietors)',
            options=industry,
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
        id='news-analysis-c4',
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
                     html.Div(id='info-c4'),
                   ]),
        ]),
      dcc.Graph(id='wages', responsive=False),
    ])


@callback(Output('news-analysis-c4', 'style'),
          Input('toggle-prediction', 'value'))
def render_callbacks(predict):
  if predict:
    return {'display': 'none'}
  else:
    return {'display': 'initial'}


@callback(Output('info-c4', 'children'), Input('detection_method', 'value'))
def render_information(detection_method):
  return utils.get_technique_information(detection_method)


@callback(Output('wages', 'figure'), Input('slct_industry', 'value'),
          Input('global_local', 'value'), Input('toggle-prediction', 'value'),
          Input('detection_method', 'value'), Input('selection_type', 'value'), 
              Input('navbar_gl', 'value'))
def wageupdate(ind, global_local_choice, predict, detection_method, selection_type, navbar_gl):
  df = wages.sort_values(by='Data Series').copy()
  if ind != 'Real Wage vs Average Wage':
    male_name = str(ind) + ' - Male '
    female_name = str(ind) + ' - Female '

  if predict:
    height = styles.HEIGHT1
    years = df['Data Series']
    colors = [
      styles.colors['purple'], styles.colors['darkblue'],
      styles.colors['green'], styles.colors['lightblue'],
      styles.colors['yellow']
    ]
    index = pd.date_range(start="2001", end="2021", freq="A")

    fig = go.Figure()

    if ind == 'Real Wage vs Average Wage':
      real_wage = df['Real Wage'].tolist()
      avgWage = df['Average'].tolist()
      yreal_wage = pd.Series(real_wage, index).interpolate(method='linear')
      yavgWage = pd.Series(avgWage, index).interpolate(method='linear')
      fcast_real_wage = utils.ses(yreal_wage, 10)
      fcast_avgWage = utils.ses(yavgWage, 10)

      fig.add_trace(
        go.Scatter(
          x=index,
          y=df['Real Wage'].to_list(),
          line=dict(color=styles.colors['black']),
          name="Real Wage"  # this sets its legend entry
        ))

      fig.add_trace(
        go.Scatter(
          x=index,
          y=df['Average'].to_list(),
          line=dict(color=styles.colors['red']),
          name="Average Wage"  # this sets its legend entry
        ))

      j = 0
      for i in range(1, 6):
        fig.add_traces(
          go.Scatter(x=fcast_real_wage['index'],
                     y=fcast_real_wage.iloc[:, i],
                     mode='lines',
                     name=fcast_real_wage.columns[i] + '- Real Wage',
                     line=dict(color=colors[i - 1])))

        fig.add_traces(
          go.Scatter(x=fcast_avgWage['index'],
                     y=fcast_avgWage.iloc[:, i],
                     mode='lines',
                     name=fcast_avgWage.columns[i] + '- Average Wage',
                     line=dict(color=colors[i - 1])))
    else:
      male = df[male_name].tolist()
      female = df[female_name].tolist()
      ymale = pd.Series(male, index).interpolate(method='linear')
      yfemale = pd.Series(female, index).interpolate(method='linear')
      fcast_male = utils.ses(ymale, 10)
      fcast_female = utils.ses(yfemale, 10)

      fig.add_trace(
        go.Scatter(
          x=index,
          y=ymale,
          line=dict(color=styles.colors['blue']),
          mode='lines',
          name="Male"  # this sets its legend entry
        ))

      fig.add_trace(
        go.Scatter(
          x=index,
          y=yfemale,
          line=dict(color=styles.colors['pink']),
          mode='lines',
          name="Female"  # this sets its legend entry
        ))


      for i in range(1, 6):
        fig.add_traces(
          go.Scatter(x=fcast_male['index'],
                     y=fcast_male.iloc[:, i],
                     mode='lines',
                     legendgroup=fcast_male.columns[i],
                     legendgrouptitle_text=str(fcast_male.columns[i]),
                     name='Male',
                     line=dict(color=px.colors.qualitative.Bold[i])))

        fig.add_traces(
          go.Scatter(x=fcast_female['index'],
                     y=fcast_female.iloc[:, i],
                     mode='lines',
                     legendgroup=fcast_female.columns[i],
                     name='Female',
                     line=dict(color=px.colors.qualitative.Pastel[i])))

      fig.update_layout(height=height, legend_title='Legend', showlegend=True)

  else:
    height = styles.HEIGHT2
    fig = make_subplots(rows=2,
                        cols=1,
                        vertical_spacing=styles.VERT_SPACING,
                        shared_xaxes=True)

    sentiment_df = utils.load_news_sentiments_datasets(global_local_choice)
    try:
      df = utils.prepare_for_plotting(df,
                                      'Data Series',
                                      format='%Y',
                                      to_datetime=True)
    except:
      df = utils.prepare_for_plotting(df,
                                      'Data Series',
                                      format='%Y',
                                      to_datetime=False)
    df = df[df.date > '2010-01']

    merged_df = utils.display_tagged_events(global_local_choice, df)
    # merged_df['value'] = merged_df['value'].max()

    sentiment_df = utils.filter_by_query_term(global_local_choice,
                                              sentiment_df, filter)
    sentiment_df = utils.prepare_for_plotting(sentiment_df, 'date')
    temp_sentiment_df = pd.DataFrame(
      sentiment_df.groupby(['date', 'vader_result_body_x'
                            ])['true_headline'].count()).reset_index().rename(
                              {'true_headline': 'count'}, axis=1)
    temp_sentiment_df['anomaly'] = sentiment_df.groupby(
      ['date', 'vader_result_body_x'])['anomaly'].max().values

    if ind == 'Real Wage vs Average Wage':
      target_col = 'Average'
      fig.add_trace(go.Scatter(x=df.date.astype(str),
                               y=df['Real Wage'],
                               name='Real Wage',
                               mode='lines',
                               marker_color=styles.colors['red']),
                    row=1,
                    col=1)
      fig.add_trace(go.Scatter(x=df.date.astype(str),
                               y=df['Average'],
                               name='Average Wage',
                               mode='lines',
                               marker_color=styles.colors['black']),
                    row=1,
                    col=1)
    else:
      target_col = female_name
      fig.add_trace(go.Scatter(x=df.date.astype(str),
                               y=df[male_name],
                               name='Male',
                               mode='lines',
                               marker_color=styles.colors['blue']),
                    row=1,
                    col=1)
      fig.add_trace(go.Scatter(x=df.date.astype(str),
                               y=df[female_name],
                               name='Female',
                               mode='lines',
                               marker_color=styles.colors['pink']),
                    row=1,
                    col=1)

    fig = utils.add_sentiment_traces(target_col, temp_sentiment_df, merged_df,
                                     global_local_choice, detection_method,
                                     fig)
    headlines, main_dates = utils.view_events_on_chart(fig, selection_type, navbar_gl)
    fig = utils.render_significant_dates(fig, main_dates, '', styles.colors['purple'])
    # fig.update_xaxes(rangeslider_visible=True, )
    fig.update_xaxes(range=['2010-01', '2021-10'])
    fig['layout']['yaxis1'].update(title='Salary (SGD)')
    fig['layout']['xaxis2'].update(rangeslider_visible=True)
    fig.update_layout(height=height, )

  fig.update_layout(
    font=dict(size=10, ),
    legend=dict(groupclick="toggleitem"),
    title=ind,
    width=styles.WIDTH,
    template='plotly_white',
    font_family="Lexend",
  )

  return fig
