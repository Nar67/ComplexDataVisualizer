import pandas as pd
import base64
import datetime
import io
import numpy as np

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from layout.upload.upload import upload_info

from dash.dependencies import Input, Output, State

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.impute import KNNImputer
from sklearn.impute import SimpleImputer

from detect_delimiter import detect

from app import app



@app.callback(Output("url", "pathname"),
              Input('upload_btn', 'n_clicks'), prevent_initial_call=True)
def upload_view(n_clicks):
    return "/upload"

@app.callback(Output('categorical_input', 'hidden'),
              Input('dataset-kind', 'value'))
def show_input(kind):
    return kind != 'mixed'

@app.callback(Output('label-column-dropdown', 'hidden'),
              Input('dataset-labeled', 'value'))
def show_input(labeled):
    return labeled != 'labeled'


#Callback for the upload 
@app.callback(Output('predata', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'), 
              prevent_initial_call=True)
def upload_dataset(content, name, dates):
    if content is not None:
        df = parse_contents(content, name, dates)
        df.replace([np.inf, -np.inf, '?'], np.nan, inplace=True)

        return df.to_json(date_format='iso', orient='split')
    else:
        return None


@app.callback(Output('upload-info', 'children'),
              Input('predata', 'data'),
              prevent_initial_call=True)
def upload_options(dff):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')
    return upload_info(df)


@app.callback(Output('dataset-info', 'data'),
              Output('data', 'data'),
              Input('confirm_upload_btn', 'n_clicks'),
              State('dataset-kind', 'value'), 
              State('categorical_column_input', 'value'),
              State('dataset-labeled', 'value'),
              State('feature-column', 'value'),
              State('convert-vars', 'value'),
              State('missing-values', 'value'),
              State('predata', 'data'),
              prevent_initial_call=True)
def save_upload_options(n_clicks, dataset_kind, column_text, labeled, label_column, convert, missing_values, dff):
    if dff is None:
        raise PreventUpdate        
    df = pd.read_json(dff, orient='split')
    
    if column_text != None:
        df = convert_vars(df, parse_categorical_column_text(column_text), convert) 


    if missing_values == 'impute':
        df = impute_missing(df, convert)
    
    return {'dataset_type': dataset_kind, 
            'column_info': parse_categorical_column_text(column_text) if column_text != None else None,
            'labeled': labeled == 'labeled',
            'label_column': label_column if labeled == 'labeled' else None},\
            df.to_json(date_format='iso', orient='split')


def convert_vars(df, categorical_cols, convert):
    if 'numerical' in convert: #majority of numerical, converting categorical to numerical
        return pd.get_dummies(df, columns=[df.columns[i] for i in categorical_cols])
    else: #converting numerical to categorical
        return discretize(df, [df.columns[i] for i in categorical_cols])


def discretize(df, categorical_cols):
    for col in list(set(df.columns).difference(categorical_cols)):
        disc_col = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='kmeans').fit_transform(df[[col]])
        disc_col = pd.DataFrame(disc_col).rename(columns={0: col})
        df[[col]] = disc_col
        del(disc_col)
    return df


def impute_missing(df, convert):
    if 'numerical' in convert:
        imputer = KNNImputer()
    else:
        imputer = SimpleImputer(strategy='most_frequent')

    imputer.fit_transform(df)
    return df

def parse_categorical_column_text(text):
    res = []
    for i in text.split(','):
        if '-' in i:
            res += range(int(i.split('-')[0])-1, int(i.split('-')[1]))
        else:
            res.append(int(i)-1)
    return res

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    
    decoded = base64.b64decode(content_string)
    try:
        if '.csv' in filename:
            # Assume that the user uploaded a CSV file
            delimiter = detect(io.StringIO(decoded.decode('utf-8')).getvalue().split('\n')[0])
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep = delimiter)
        elif '.xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        return html.Div([
            'There was an error processing this file.'
        ])
    return df