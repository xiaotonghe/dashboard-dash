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


# ------------------------------------------------------------------------------
# Import and clean data
# (importing)
df_OpenSalesOrders=pd.read_excel("SampleData.xlsx",sheet_name='OpenSalesOrders')
df_Inventory=pd.read_excel("SampleData.xlsx",sheet_name='Inventory')
df_PlannedOrders=pd.read_excel("SampleData.xlsx",sheet_name='PlannedProductionOrders')
df_SalesHistory = pd.read_excel("SampleData.xlsx", sheet_name='SalesHistory')
# extracting data for sales history
df=df_SalesHistory.copy()
df_new=df.groupby('CREATEDDATE')['QTYORDERED'].sum()
df_new=df_new.reset_index()
df_new['year']=df_new['CREATEDDATE'].dt.year
df_new['month']=df_new['CREATEDDATE'].dt.month
df_new['day'] = df_new['CREATEDDATE'].dt.day
# extracting data for total sales orders number

# extracting data for planned production orders number

# return html Table with dataframe values
def df_to_table(df):
    return html.Table(
        [html.Tr([html.Th(col) for col in df.columns])]
        + [
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(len(df))
        ]
    )
# returns top indicator div
def indicator(color, text, id_value,child):
    return html.Div(
        [
            html.P(text, className="twelve columns indicator_text"),
            html.P(id=id_value, className="indicator_value",children=child),
        ],
        className="four columns indicator pretty_container",
    )
# ------------------------------------------------------------------------------
# App layout
app = dash.Dash(__name__, external_stylesheets=[
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ]
)
server = app.server

app.layout = html.Div([
    html.H1("Dashboard Demo", style={'text-align': 'center'}, className="header"),

    html.Div(
                className="row indicators",
                style={"width":"100%"},
                children=[
                    indicator("#00cc96", "Open Sales Orders", "left_leads_indicator",len(df_OpenSalesOrders)),
                    indicator("#119DFF", "Planned Production Orders", "middle_leads_indicator",len(df_PlannedOrders)),
                ],
            ),
    
    html.Div([
        dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2019", "value": 2019},
                     {"label": "2020", "value": 2020}],
                 multi=False,
                 value=2019,
                 style={'width': "40%"}
                 ),
        dcc.Graph(id='sales_line', figure={}, className='eight columns')
    ], className="row pretty_container"),
    

    html.Div([
        html.P("Open Sales Details", className="twelve columns indicator_text"),
        html.Div(id="leads_table", className="table",
                children=[df_to_table(df_OpenSalesOrders)],
                style={'width': "100%"}),
    ], className="row six columns pretty_container"),

    html.Div([
        html.P("Inventory Details", className="twelve columns indicator_text"),
        html.Div(id="leads_table1", className="table",
                children=[df_to_table(df_Inventory)],
                style={'width': "100%"}),
    ],className="row six columns pretty_container")
    
])

# ------------------------------------------------------------------------------

# Droptown --> linegraph and table
@app.callback(
    Output(component_id='sales_line', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(year):
    # filter data
    df=df_new.copy()
    df=df[df['year'] == year]
    fig_linegraph = px.line(df, x='CREATEDDATE', y='QTYORDERED', title='Sales History')
    
    # sales open table
    fig_table = px.line(df, x='CREATEDDATE', y='QTYORDERED', title='Sales History')
    
    return fig_linegraph

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    #app.run_server(debug=True)
    # Get port and debug mode from environment variables    
    app.run_server(debug=True, host="0.0.0.0", port=5000)
