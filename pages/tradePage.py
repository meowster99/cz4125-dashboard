import pickle
from typing import List

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from pages.config.config import *
from dash import Input, Output, dcc, html, callback, dash_table
import dash
from plotly.subplots import make_subplots

from src.trade import TradeStat, UnifiedStats
from utils import trade_list

TRADE_DATA = './data/trade_data/trade_data.pkl'
labels = ['Export', 'Import']
colors = ['#1c9099', '#a6bddb']

with open(TRADE_DATA, 'rb') as inp:
  s = pickle.load(inp)
b = UnifiedStats()
b.extend(s)
world_imports = b.get_indicator(partner="World", indicator="Import")
world_exports = b.get_indicator(partner="World", indicator="Export")
b.filter()

all_countries = b.countries
country_list = [country.name for country in all_countries]
full_list = b.product_codes()
pc_list = [pc for pc in full_list if pc not in trade_list]

regions: UnifiedStats = UnifiedStats()
regions.extend(b.region_list)

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

# --- init dash ---
dash.register_page(__name__, name='Trade statistics', path='/trade-stats')


def layout():
  return html.Div([
    dbc.Row([
      html.H1(children="Geospatial graph of Exports and Imports"),
      dbc.Col([dcc.Dropdown(YEAR_RANGE, 2019, id='year-network-dropdown')],
              style={"width": "25%"}),
      dbc.Col([dcc.Dropdown(pc_list, pc_list[0], id='prodcode-network-dropdown')],
              style={"width": "25%"}),
      dbc.Col([
        dcc.RadioItems(
          labels, labels[0], id='ind-network-dropdown')
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
        dbc.Col([dcc.Dropdown(YEAR_RANGE, 2019, id='year-network-dropdown1')],
                style={"width": "25%"}),
      ]),
    ], ),
    dbc.Row([
      dbc.Col(dcc.Graph(id="pie-graph-tradereliance")),
    ], ),
    dbc.Row([
      html.H1(children="Exports and Imports over time"),
      dbc.Col(
        [dcc.Dropdown(country_list, 'Malaysia', id='country-lineg-dropdown')],
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
      dbc.Col([dcc.Dropdown(pc_list, pc_list[0], id='pc-lineg-dropdown')],
              style={"width": "25%"}),
    ], ),
    dbc.Row([
      dbc.Col([
        dcc.RadioItems(
          ['Top 5', 'Top 10', "All"], 'Top 5', id="checklist-pc", inline=True)
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

def createScatter(graph, row, col, **kwargs):
  return graph.append_trace(go.Scatter(name=kwargs['name'],
                                       x=kwargs['x'],
                                       y=kwargs['y'],
                                       legendgroup=kwargs['legendgroup'],
                                       marker=dict(colorscale="Viridis", ),
                                       mode="lines"),
                            row=row,
                            col=col)


# --- callbacks ---
@callback(
  Output(component_id='geospatial-network', component_property='figure'), [
    Input(component_id='year-network-dropdown', component_property='value'),
    Input(component_id='prodcode-network-dropdown',
          component_property='value'),
    Input(component_id='ind-network-dropdown', component_property='value')
  ])
def graph_update(year_value, pc_value, ind_value):
  o = b.get_indicator(productcode=pc_value, indicator=ind_value)
  e = UnifiedStats()
  e.extend(o)
  all_ind: List[TradeStat] = e.indicators

  longitude = e.get_long()
  latitude = e.get_lat()

  fig_network = go.Figure()

  fig_network.add_trace(
    go.Scattergeo(
      locationmode='country names',
      lon=longitude,
      lat=latitude,
      hoverinfo='text',
      text=e.get_country_names(),
      mode='markers',
      marker=dict(size=2,
                  color='rgb(255, 0, 0)',
                  line=dict(width=3, color='rgba(68, 68, 68, 0)'))))

  # Singapore
  fig_network.add_trace(
    go.Scattergeo(locationmode='country names',
                  lon=[103.851959],
                  lat=[1.290270],
                  hoverinfo='text',
                  text=["Singapore"],
                  mode='markers',
                  marker=dict(size=2,
                              color='rgb(255, 0, 0)',
                              line=dict(width=3,
                                        color='rgba(68, 68, 68, 0)'))))

  for i in range(len(all_ind)):
    max_ = float(e.get_max(year_value))
    data = all_ind[i].stats.get(int(year_value))
    if max_ > 0:
      if data:
        fig_network.add_trace(
          go.Scattergeo(
            locationmode='country names',
            lon=[103.851959, all_ind[i].country_info.long],
            lat=[1.290270, all_ind[i].country_info.lat],
            mode='lines',
            line=dict(width=1, color='red'),
            opacity=(float(data) / max_),
          ))
  fig_network.update_layout(
    title_text=f'{pc_value}'
    f'({ind_value}) for {year_value}',
    showlegend=False,
    height=600,
  )

  return fig_network


@callback(Output(component_id='sunburst', component_property='figure'), [
  Input(component_id='year-network-dropdown', component_property='value'),
  Input(component_id='prodcode-network-dropdown', component_property='value')
])
def trade_prop(year_value, pc_value):
  # world statistics
  for x, y in zip(world_imports, world_exports):
    if x.productcode == pc_value:
      import_total = x.stats.get(year_value)
    if y.productcode == pc_value:
      export_total = y.stats.get(year_value)
  # region statistics
  region_stats = regions.get_indicator(productcode=pc_value)
  temp_ids = ["Import", "Export"]
  temp_label = ["Import", "Export"]
  temp_parent = ["", ""]
  temp_values = [import_total, export_total]
  temp_colours = [colors[0], colors[1]]
  for i in region_stats:
    temp_ids.append(f"{i.indicator} - {i.partner}")
    temp_label.append(i.partner)
    temp_parent.append(i.indicator)
    temp_values.append(i.stats.get(year_value))
    temp_colours.append(colors[0] if i.indicator == "Import" else colors[1])
  # country statistics
  country_stats = b.get_indicator(productcode=pc_value)
  for a in country_stats:
    # e.g.
    # temp id:
    # North America - United States
    if COUNTRY_REG.get(a.partner):
      temp_ids.append(f"{a.indicator} - {a.partner}")
      temp_label.append(a.partner)
      temp_parent.append(f"{a.indicator} - {COUNTRY_REG.get(a.partner)}")
      temp_values.append(a.stats.get(year_value))
      temp_colours.append(colors[0] if a.indicator == "Import" else colors[1])
  labels = [*temp_label]
  parents = [*temp_parent]
  values = [*temp_values]
  colours = [*temp_colours]
  fig = go.Figure(
    go.Sunburst(ids=temp_ids,
                labels=labels,
                parents=parents,
                values=values,
                insidetextorientation='radial',
                marker=dict(colors=colours),
                branchvalues="total"))
  fig.update_layout(
    title_text=f'{pc_value} '
    f'for {year_value}',
    showlegend=False,
    height=600,
  )
  return fig


@callback(
  Output(component_id='pie-graph-tradereliance', component_property='figure'),
  [Input(component_id='year-network-dropdown1', component_property='value')])
def pie_update(year_value):
  import_vals = []
  export_vals = []
  import_pc = []
  export_pc = []

  for x, y in zip(world_imports, world_exports):
    import_vals.append(x.stats.get(year_value))
    import_pc.append(x.productcode)
    export_vals.append(y.stats.get(year_value))
    export_pc.append(y.productcode)

  fig_piechart = make_subplots(1,
                               2,
                               specs=[[{
                                 'type': 'domain'
                               }, {
                                 'type': 'domain'
                               }]],
                               subplot_titles=['Imports', 'Exports'])
  fig_piechart.add_trace(
    go.Pie(labels=import_pc,
           values=import_vals,
           scalegroup='one',
           name=f"Imports in {year_value}",
           textinfo='label+percent',
           textposition='inside'), 1, 1)
  fig_piechart.add_trace(
    go.Pie(labels=export_pc,
           values=export_vals,
           scalegroup='one',
           name=f"Exports in {year_value}",
           textinfo='label+percent',
           textposition='inside'), 1, 2)
  fig_piechart.update_layout(title_text=f'Trade for {year_value}',
                             uniformtext_minsize=12,
                             uniformtext_mode='hide')
  return fig_piechart


@callback(
  Output(component_id='line-graph-trade', component_property='figure'),
  [Input(component_id='country-lineg-dropdown', component_property="value")])
def lineg_update(country_value):

  # --- export/import line graph ---
  country_stats = b.get_indicator(partner=country_value)
  fig_line = make_subplots(rows=1,
                           cols=2,
                           subplot_titles=[
                             f'Imports from {country_value}',
                             f'Exports to {country_value}'
                           ])
  for i in country_stats:
    if i.indicator == "Import":
      row, col = (1, 1)
      lg = '1'
    elif i.indicator == "Export":
      row, col = (1, 2)
      lg = '2'
    createScatter(fig_line, row, col, name=i.productcode,
                  x=list(i.stats.keys()), y=list(i.stats.values()),
                  legendgroup=lg)
  return fig_line


@callback(
  Output(component_id="pc-line-graph-trade", component_property='figure'), [
    Input(component_id='pc-lineg-dropdown', component_property="value"),
    Input(component_id='checklist-pc', component_property="value")
  ])
def pc_lineg_update(pc_value, top_n):
  country_stats = b.get_indicator(productcode=pc_value)
  fig_line = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=[f'Imports to Singapore', f'Exports from Singapore'])
  if top_n != "All":
    top_exporters = {}
    top_importers = {}
    for i in country_stats:
      if i.indicator == "Import":
        top_importers[i.partner] = sum(list(i.stats.values()))
      if i.indicator == "Export":
        top_exporters[i.partner] = sum(list(i.stats.values()))

    top_importers_ = sorted(top_importers.items(),
                            key=lambda x: x[1],
                            reverse=True)
    top_exporters_ = sorted(top_exporters.items(),
                            key=lambda x: x[1],
                            reverse=True)

    if top_n == "Top 5":
      top_importers_ = top_importers_[:5]
      top_exporters_ = top_exporters_[:5]
    else:
      top_importers_ = top_importers_[:10]
      top_exporters_ = top_exporters_[:10]
    for z, e in zip(top_importers_, top_exporters_):
      imp = b.get_indicator(partner=z[0],
                            productcode=pc_value,
                            indicator="Import")[0]
      exp = b.get_indicator(partner=e[0],
                            productcode=pc_value,
                            indicator="Export")[0]
      createScatter(fig_line, 1, 1, name=z[0],
                    x=list(imp.stats.keys()), y=list(imp.stats.values()),
                    legendgroup='1')
      createScatter(fig_line, 1, 2, name=e[0],
                    x=list(exp.stats.keys()), y=list(exp.stats.values()),
                    legendgroup='2')
  else:
    for i in country_stats:
      if i.indicator == "Import":
        row, col = (1, 1)
        lg = '1'
      elif i.indicator == "Export":
        row, col = (1, 2)
        lg = '2'
      createScatter(fig_line, row, col, name=i.partner,
                  x=list(i.stats.keys()), y=list(i.stats.values()),
                  legendgroup=lg)
  return fig_line


@callback(Output("line-graph-timeseries", "figure"),
          Input("checklist", "value"))
def update_line_chart(pc):
  fig_line = make_subplots(
    rows=1, cols=2, subplot_titles=['Imported products', 'Exported products'])
  fig_line.update_layout(
    title_text="Total traded over time",
    legend_tracegroupgap=500,
  )
  for i, e in zip(world_imports, world_exports):
    if i.productcode in pc:
      createScatter(fig_line, 1, 1, name=i.productcode,
                    x=list(i.stats.keys()), y=list(i.stats.values()),
                    legendgroup='1')
    if e.productcode in pc:
      createScatter(fig_line, 1, 2, name=e.productcode,
                    x=list(e.stats.keys()), y=list(e.stats.values()),
                    legendgroup='2')
  return fig_line


@callback(Output("c-line-graph-timeseries", "figure"), Output('tbl', 'data'),
          Input("c-checklist-pc", "value"))
def update_line_chart(top_n):
  fig_cline = make_subplots(
    rows=1, cols=2, subplot_titles=['Import partners', 'Export partners'])
  fig_cline.update_layout(
    title_text="Total traded over time",
    legend_tracegroupgap=500,
  )
  df_data = [{
    'country_im': "Select"
  }, {
    'import-data': "Top n"
  }, {
    'country_ex': "to get"
  }, {
    'export-data': "data"
  }]
  if top_n != "All":
    df_data = []
    sum_imports = {}
    sum_exports = {}
    for c in all_countries:
      country = c.name
      country_im = b.get_indicator(partner=country, indicator="Import")
      country_ex = b.get_indicator(partner=country, indicator="Export")
      sum_i = 0
      sum_e = 0
      for i in country_im:
        sum_i += sum(list(i.stats.values()))
      for e in country_ex:
        sum_e += sum(list(e.stats.values()))
      sum_imports[country] = sum_i
      sum_exports[country] = sum_e

    top_importers_ = sorted(sum_imports.items(),
                            key=lambda x: x[1],
                            reverse=True)
    top_exporters_ = sorted(sum_exports.items(),
                            key=lambda x: x[1],
                            reverse=True)

    if top_n == "Top 5":
      top_importers_ = top_importers_[:5]
      top_exporters_ = top_exporters_[:5]
    else:
      top_importers_ = top_importers_[:10]
      top_exporters_ = top_exporters_[:10]
    for z, e in zip(top_importers_, top_exporters_):
      total_imports = {}
      total_exports = {}
      country_im = b.get_indicator(partner=z[0], indicator="Import")
      country_ex = b.get_indicator(partner=e[0], indicator="Export")
      # imports
      for i in country_im:
        for year in list(i.stats.keys()):
          if year not in total_imports:
            total_imports[year] = i.stats[year]
          else:
            total_imports[year] += i.stats[year]
      # exports
      for x in country_ex:
        for year in list(x.stats.keys()):
          if year not in total_exports:
            total_exports[year] = x.stats[year]
          else:
            total_exports[year] += x.stats[year]
      # draw line
      createScatter(fig_cline, 1, 1, name=z[0],
                    x=list(total_imports.keys()),
                    y=list(total_imports.values()),
                    legendgroup='1')
      createScatter(fig_cline, 1, 2, name=e[0],
                    x=list(total_exports.keys()),
                    y=list(total_exports.values()),
                    legendgroup='2')
      df_data.append({
        'country_im': z[0],
        'import-data': z[1],
        'country_ex': e[0],
        'export-data': e[1]
      })
  else:
    for c in all_countries:
      country = c.name
      total_imports = {}
      total_exports = {}
      country_im = b.get_indicator(partner=country, indicator="Import")
      country_ex = b.get_indicator(partner=country, indicator="Export")
      # imports
      for i in country_im:
        for year in list(i.stats.keys()):
          if year not in total_imports:
            total_imports[year] = i.stats[year]
          else:
            total_imports[year] += i.stats[year]
      # exports
      for e in country_ex:
        for year in list(e.stats.keys()):
          if year not in total_exports:
            total_exports[year] = e.stats[year]
          else:
            total_exports[year] += e.stats[year]
      # draw line
      createScatter(fig_cline, 1, 1, name=country,
                    x=list(total_imports.keys()),
                    y=list(total_imports.values()),
                    legendgroup='1')
      createScatter(fig_cline, 1, 2, name=country,
                    x=list(total_exports.keys()),
                    y=list(total_exports.values()),
                    legendgroup='2')
  return fig_cline, df_data
