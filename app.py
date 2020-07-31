# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# import libraries
import os
import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import plotly.express as px

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as table
from dash.dependencies import Input, Output

from panels import homepage, opensales, inventory, plannedorders, saleshistory

# ------------------------------------------------------------------------------
# Import and clean data
# (importing)
df_OpenSalesOrders=pd.read_excel("SampleData.xlsx",sheet_name='OpenSalesOrders')
df_Inventory=pd.read_excel("SampleData.xlsx",sheet_name='Inventory')
df_PlannedOrders=pd.read_excel("SampleData.xlsx",sheet_name='PlannedProductionOrders')
df_SalesHistory = pd.read_excel("SampleData.xlsx", sheet_name='SalesHistory')
# extracting data for sales history
df_line=df_SalesHistory.copy()
df_line['month']=df_line['CREATEDDATE'].dt.month
df_line['year']=df_line['CREATEDDATE'].dt.year
df_line = df_line.groupby(['year','month'])['QTYORDERED'].sum()
df_line = df_line.reset_index()

# extracting data for inventory
df_inven = df_Inventory.copy()
df_inven = df_inven.groupby('ITEMID')['QTY'].sum()
df_inven = df_inven.reset_index()

# return html Table with dataframe values
def df_to_table(df):
    return html.Table(
        [html.Tr([html.Th(col) for col in df.columns])]
        + [
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(len(df))
        ], className='table table-striped table-bordered table-hover',
        
    )

# Sales history line graph using plotly express
fig_linegraph = px.line(df_line, x='month', y='QTYORDERED', color='year',
                        hover_data={'year': True, 'month': True, 'QTYORDERED': True},
                        )
fig_linegraph.update_traces(hovertemplate="Year: %{year}: <br>Month: %{month} </br> Qty: %{QTYORDERED}")
fig_linegraph.update_layout(
    
    xaxis=dict(
        visible=True,
        gridcolor='#bdc3c7',
        gridwidth=1,
        tickmode = 'array',
        tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        showgrid=True,
        showline=True,
        # zerolinecolor="#444",
        # zerolinewidth = 1, 
        # size="bottom",
        tickfont=dict(family='Arial',
                        size=12,
                        color='rgb(82,82,82)'),
                    
    ),
    yaxis=dict(
        gridcolor='#bdc3c7',
        gridwidth=1,
        
    ),
    margin=dict(
        l=10,
        r=10,
        t=50, 
    ),
    plot_bgcolor='white',

    hoverlabel=dict(
        bgcolor="white", 
        font_size=16, 
        font_family="Rockwell")
)

# Sales history line graph using go
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_line[df_line['year'] == 2019]['month'],
                    y=df_line[df_line['year'] == 2019]['QTYORDERED'],
                    mode='lines+markers', line_color='rgb(128, 128, 128)',name='2019'))
fig.add_trace(go.Scatter(x=df_line[df_line['year'] == 2020]['month'],
                    y=df_line[df_line['year'] == 2020]['QTYORDERED'],
                    mode='lines+markers', line_color='rgb(36, 194, 206)', name='2020'))
fig.update_layout(xaxis=dict(tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                            zerolinecolor='rgb(170, 170, 170)',
                            showgrid=False),
                    yaxis=dict(gridcolor='rgb(170, 170, 170)',
                                zerolinecolor='rgb(170, 170, 170)'),
                    plot_bgcolor='white'        
                    )


# ------------------------------------------------------------------------------
# App layout
app = dash.Dash(__name__, external_stylesheets=[
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ]
)
# app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
                html.Div([
                    html.Div([
                        html.Nav([html.Button([html.Img(src='assets/Sokol-Logo-DBIConvention.png', className="col-md-3 logo logo-btn",
                                style={"height":"60px","width":"300px"},id='logo_btn',n_clicks=0)]
                                , style={"margin-bottom": "0px"}),
                                ], style={"height": "50px", "margin-bottom": "20px"}),
                    ],className='navbar navbar-default top-navbar', ),
                    html.Div([
                        
                        html.Div([
                            html.H1([])
                        ], className="row col-md-12 page-header"),
                    
                        html.Div([
                            html.Div([
                                html.Button([
                                    html.Div([
                                        html.Div([
                                            html.Img(src='assets/money1.png',className="tile-icon"),
                                        ],className="panel-left pull-left"),
                                        html.Div([
                                            html.H3([len(df_OpenSalesOrders)],className="tile-content"),
                                            html.Div(['Open Sales'],),
                                        ],className="panel-right")
                                    ],className="panel text-center no-boder tile"),
                                ],id='open_btn',n_clicks=0,className="tile-btn col-xs-6 col-md-3 col-lg-3 "),
                            ]),

                            html.Div([
                                html.Button([
                                    html.Div([
                                        html.Div([
                                            html.Img(src='assets/pen.png',className="tile-icon"),
                                        ], className="panel-left pull-left"),
                                        html.Div([
                                            html.H3([len(df_PlannedOrders)],className="tile-content"),
                                            html.Div(['Planned Orders'],),
                                        ],className="panel-right")
                                    ],className="panel text-center no-boder tile"),
                                ],id='plan_btn',n_clicks=0,className="tile-btn col-xs-6 col-md-3 col-lg-3"),
                            ]),

                            html.Div([
                                html.Button([
                                    html.Div([
                                        html.Div([
                                            html.Img(src='assets/sales history.png',className="tile-icon"),
                                        ],className="panel-left pull-left"),
                                        html.Div([
                                            html.H3([len(df_SalesHistory)],className="tile-content"),
                                            html.Div(['Sales History'],),
                                        ],className="panel-right")
                                    ],className="panel text-center no-boder tile"),
                                ],id='history_btn',n_clicks=0,className="tile-btn col-xs-6 col-md-3 col-lg-3"),
                            ]),

                            html.Div([
                                html.Button([
                                    html.Div([
                                        html.Div([
                                            html.Img(src='assets/inventory1.png',className="tile-icon"),
                                        ],className="panel-left pull-left"),
                                        html.Div([
                                            html.Div([df_to_table(df_inven),],className='sm-tb'),
                                            html.Div(['Inventory List'],),
                                        ],className="panel-right")
                                    ],className="panel text-center no-boder tile"),
                                ],id="inventory_btn",n_clicks=0,className="tile-btn col-xs-6 col-md-3 col-lg-3"),
                            ]),                           
                            
                        ], className="row col-xs-12 col-md-12 upper-main"),
                        
                        html.Div([
                            html.Div([
                                html.Div(className='panel-heading',id='main-header'),
                                html.Div([
                                    dcc.Graph(figure=fig)
                                ],id='main-content',className='lg-tb panel-body morris-hover morris-default-style'),
                            ],className='panel panel-default morris-line-chart')
                        ], className="row col-xs-12 col-md-12 col-lg-12 lower-main"),
                    
                    ], id="page-inner")

                ], id='wrapper')
])

# ------------------------------------------------------------------------------
# callback
@app.callback([Output('main-content','children'),
               Output('main-header','children')],
              [Input('logo_btn','n_clicks'),
               Input('open_btn','n_clicks'),
               Input('plan_btn','n_clicks'),
               Input('history_btn','n_clicks'),
               Input('inventory_btn','n_clicks')])
def displayClick(btn1, btn2, btn3,btn4,btn5):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'logo_btn' in changed_id:
        text ='Sales History line chart'
        msg = dcc.Graph(figure=fig)
        ele = html.Div(msg)
    elif 'open_btn' in changed_id:
        text='Open Sales Order Detail'
        msg = df_to_table(df_OpenSalesOrders)
        ele = html.Div(msg)
    elif 'plan_btn' in changed_id:
        text='Planned Orders Detail'
        msg = df_to_table(df_PlannedOrders)
        ele = html.Div(msg,className='special')
    elif 'history_btn' in changed_id:
        text='Sales History Detail'
        msg = df_to_table(df_SalesHistory)
        ele = html.Div(msg)
    elif 'inventory_btn' in changed_id:
        text='Inventory Detail'
        msg = df_to_table(df_Inventory)
        ele = html.Div(msg,className='special')
    else:
        text ='Sales History line chart'
        msg = dcc.Graph(figure=fig)
        ele = html.Div(msg)
    return ele,[text]

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    #app.run_server(debug=True)
    # Get port and debug mode from environment variables    
    app.run_server(debug=True, host="0.0.0.0", port=5000)