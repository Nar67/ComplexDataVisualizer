import pandas as pd
import base64
import datetime
import io

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State

from app import app



@app.callback(Output("url", "pathname"),
              Input('upload_btn', 'n_clicks'), prevent_initial_call=True)
def upload_view(n_clicks):
    return "/upload"

@app.callback(Output('categorical_input', 'hidden'),
              Input('dataset-kind', 'value'))
def show_input(kind):
    return kind != 'mixed'


#Callback for the upload 
@app.callback(Output('data', 'data'),
              Output('dataset-type', 'data'),
              Output('dataset-column-text', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'), 
              State('dataset-kind', 'value'), 
              State('categorical_column_input', 'value'), 
              prevent_initial_call=True)
def upload_dataset(content, name, dates, dataset_kind, column_text):
    if content is not None:
        df = parse_contents(content, name, dates)
        return df.to_json(date_format='iso', orient='split'), dataset_kind, column_text
    else:
        return None, None, None



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    
    decoded = base64.b64decode(content_string)
    try:
        if '.csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif '.xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df