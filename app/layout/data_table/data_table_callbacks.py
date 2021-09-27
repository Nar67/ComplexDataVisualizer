import pandas as pd
import plotly.express as px
from app import app
import dash_table


from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import dash_html_components as html
import dash_core_components as dcc
from layout.data_table.data_table import data_table

#Callback for the upload 
@app.callback(Output('table-output-data', 'children'),
              Input('data', 'data'))
def create_table(dff):
    if dff is None:
        raise PreventUpdate
        return []
    df = pd.read_json(dff, orient='split')
    return html.Div([
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i, 'type': table_type(df[i])} for i in df.columns],
            page_size=150,
            sort_action='native',
            filter_action='native',
            
            style_table={'overflowX': 'auto',
                        'overflowY': 'auto',
                        'minWidth': '100%'},

            style_as_list_view=True,

            fixed_rows={'headers': True},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },

            style_cell={
                'minWidth': '180px',
                'width': '180px', 
                'maxWidth': '180px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            tooltip_header={i: i for i in df.columns},
            tooltip_duration=2000
        ),
    ])

def table_type(df_column):
    if isinstance(df_column.dtype, pd.DatetimeTZDtype):
        return 'datetime',
    elif (isinstance(df_column.dtype, pd.StringDtype) or
            isinstance(df_column.dtype, pd.BooleanDtype) or
            isinstance(df_column.dtype, pd.CategoricalDtype) or
            isinstance(df_column.dtype, pd.PeriodDtype)):
        return 'text'
    elif (isinstance(df_column.dtype, pd.SparseDtype) or
            isinstance(df_column.dtype, pd.IntervalDtype) or
            isinstance(df_column.dtype, pd.Int8Dtype) or
            isinstance(df_column.dtype, pd.Int16Dtype) or
            isinstance(df_column.dtype, pd.Int32Dtype) or
            isinstance(df_column.dtype, pd.Int64Dtype)):
        return 'numeric'
    else:
        return 'any'