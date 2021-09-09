import pandas as pd
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate
from app import app
import dash


import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

@app.callback(
    Output({'type': 'download_points_btn', 'method' : MATCH}, "data"),
    Input({'type': 'export_points', 'method': MATCH}, 'n_clicks'),
    State({'type': 'points', 'method': MATCH}, "data"), #wip
    prevent_initial_call=True,
)
def download_points(n_clicks, points):
    if points is None:
        raise PreventUpdate
            
    method = dash.callback_context.inputs_list[0]['id']['method']
    df = pd.read_json(points, orient='split')
    return dcc.send_data_frame(df.to_csv, method + '.csv')
