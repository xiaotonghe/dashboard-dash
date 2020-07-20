# -*- coding: utf-8 -*-

# import libraries
import os
import pandas as pd
import numpy as np
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import plotly.express as px

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as table
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ]
)

def df_to_table(df):
    return html.Table(
        [html.Tr([html.Th(col) for col in df.columns])]
        + [
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(len(df))
        ]
    )

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
df_line
    


# extracting data for inventory
df_inven = df_Inventory.copy()
df_inven = df_inven.groupby('ITEMID')['QTY'].sum()
df_inven = df_inven.reset_index()

# returns top indicator div
def indicator(color, text, id_value,child):
    return html.Div(
        [
            html.P(text, className="twelve columns indicator_text"),
            html.P(id=id_value, className="indicator_value",children=child),
        ],
        className="four columns indicator pretty_container",
    )

fig_linegraph = px.line(df_line, x='month', y='QTYORDERED', color='year', title='Sales History')
fig_linegraph.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = [1,2, 3,4, 5,6, 7,8, 9,10, 11,12],
        # ticktext = ['One', 'Three', 'Five', 'Seven', 'Nine', 'Eleven']
    )
)



layout = html.Div([
    html.Div(
            className="row indicators",
            style={"width":"100%"},
            children=[
                indicator("#00cc96", "Open Sales Orders", "left_leads_indicator",len(df_OpenSalesOrders)),
                indicator("#119DFF", "Planned Production Orders", "middle_leads_indicator",len(df_PlannedOrders)),
            ],
        ),
    html.Div([
        html.P("Inventory List", className='eight coloumns'),
        html.Div(id="inventory_list", className='table eight columns',
                    children=[df_to_table(df_inven)]
                ),
    ], className="row pretty_container"),
    html.Div([
        dcc.Graph(id='sales_line', figure=fig_linegraph, className='eight columns')
    ], className="row pretty_container"),

])
