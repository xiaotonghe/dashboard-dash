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
df=df_SalesHistory.copy()
df_new=df.groupby('CREATEDDATE')['QTYORDERED'].sum()
df_new=df_new.reset_index()
df_new['year']=df_new['CREATEDDATE'].dt.year
df_new['month']=df_new['CREATEDDATE'].dt.month
df_new['day'] = df_new['CREATEDDATE'].dt.day

# return html Table with dataframe values
def df_to_table(df):
    return html.Table(
        [html.Tr([html.Th(col) for col in df.columns])]
        + [
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(len(df))
        ]
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
    
    dcc.Tabs(id='tabs-layout', value='homepage', children=[
        dcc.Tab(label='Home page', value='homepage', children=homepage.layout),
        dcc.Tab(label='Sales Orders', value='salesorders', children=opensales.layout),
        dcc.Tab(label='Inventory', value='inventory', children=inventory.layout),
        dcc.Tab(label='Planned Production Orders', value='plannedorders',children=plannedorders.layout),
        dcc.Tab(label='Sale History', value='salehistory',children=saleshistory.layout)
    ]),
])

# ------------------------------------------------------------------------------
# Tabs switching
# @app.callback(Output('tabs-content', 'children'),
#             [Input('tabs-layout', 'values')])

# def render_content(tab):
#     if tab == 'homepage':
#         return homepage.layout



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    #app.run_server(debug=True)
    # Get port and debug mode from environment variables    
    app.run_server(debug=True, host="0.0.0.0", port=5000)
