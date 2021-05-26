import pandas as pd
import base64
import datetime
import io

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State

from app import app




#Callback for the upload 
@app.callback(Output('data', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'), prevent_initial_call=True)
def upload_dataset(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
        return df.to_json(date_format='iso', orient='split')






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