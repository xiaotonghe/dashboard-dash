# -*- coding: utf-8 -*-

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

app = dash.Dash(__name__, external_stylesheets=[
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ]
)

# return html Table with dataframe values
def df_to_table(df):
    return html.Table(
        [html.Tr([html.Th(col) for col in df.columns])]
        + [
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(len(df))
        ]
    )

df_Inventory = pd.read_excel("SampleData.xlsx", sheet_name='Inventory')

layout = [

    html.Div([
        html.P("Inventory Details", className="twelve columns indicator_text"),
        html.Div(id="leads_table1", className="table",
                children=[df_to_table(df_Inventory)],
                style={'width': "100%"}),
    ],className="row ten columns pretty_container")
]