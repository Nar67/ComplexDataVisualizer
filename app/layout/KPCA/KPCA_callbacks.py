import pandas as pd
import numpy as np
import dash

from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate
from app import app
from utils.dimensionality_reduction_visualization import create_figure
from utils.data_type_check import check_all_categorical
from sklearn.decomposition import KernelPCA

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


KPCA_view = html.Div(id='KPCA-layout')

hidden = {
    'gamma-div': ['rbf', 'poly', 'sigmoid'],
    'degree-div': ['poly'],
    'coef0-div': ['poly', 'sigmoid'],
}

@app.callback(Output({'kpca-div': MATCH}, 'hidden'),
              Input('kernel', 'value'))
def show_input(kernel):
    return kernel not in hidden[dash.callback_context.outputs_list['id']['kpca-div']]

@app.callback(Output('KPCA-layout', 'children'),
              Input('data', 'data'),
              State('dataset-info', 'data'))
def create_visualization_KPCA(dff, ds_info):
    if dff is None:
        raise PreventUpdate
        return []
    df = pd.read_json(dff, orient='split')
    return html.Div([
        dcc.Store(id={'type': 'points', 'method': 'kpca'}, storage_type='session'),
        dcc.Markdown('''
            ##### Choose Kernel for the PCA:
            '''),
            html.Div([
            dcc.Dropdown(
                id='kernel',
                options=[{'label': i, 'value': i} for i in ['linear', 'poly', 'rbf', 'sigmoid', 'cosine', 'precomputed']],
                value='linear'
            ),
            html.Div(id={'kpca-div': 'gamma-div'}, hidden=True, children=[
                dcc.Markdown('''
                    ##### Choose gamma for rbf, poly and sigmoid kernels:
                    '''),                
                dcc.Input(
                id='gamma',
                placeholder='0.0',
                type='number'
                )
            ]),
            html.Div(id={'div': 'degree-div'}, hidden=True, children=[
                dcc.Markdown('''
                    ##### Choose degree for poly kernels:
                    '''),                
                dcc.Input(
                id='degree',
                placeholder='0',
                type='number'
                )
            ]),
            html.Div(id={'div': 'coef0-div'}, hidden=True, children=[
                dcc.Markdown('''
                    ##### Choose independent term for poly and sigmoid kernels:
                    '''),                
                dcc.Input(
                id='coef0',
                placeholder='0',
                type='number'
                )
            ]),
        ]),
        dcc.Markdown('''
            ##### Number of components:
            '''),
        dcc.RadioItems(
            id='KPCA-components',
            options=[{'label': i, 'value': i} for i in [2, 3]],
            value=2,
            labelStyle={'margin-right': '12px'}
        ),

        dbc.Button("Generate", color='primary', outline=True, id={'generate': 'kpca'}),


        html.Div([dcc.Graph(id='KPCA-graphic', style={'height': '90vh', 'width': '90vh'})],
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
        ),

        html.Div([dbc.Button("Export KPCA", color='primary', outline=True, id={'type': 'export_points', 'method': 'kpca'}, style={'margin-right':'12px'}),
                     dcc.Download(id={'type': 'download_points_btn', 'method' : 'kpca'}), 
                  dbc.Button("Export Coefs", color='primary', outline=True, id={'type': 'export_coefs', 'method': 'kpca'}, style={'margin-right':'12px'}), 
                    dcc.Download(id={'type': 'download_coefs_btn', 'method' : 'kpca'})])
    ])



#Callback for the KPCA 
@app.callback(Output('KPCA-graphic', 'figure'),
              Output({'type': 'points', 'method': 'kpca'}, 'data'),
              Input({'generate': 'kpca'}, 'n_clicks'),
              State("KPCA-components", "value"),
              State('data', 'data'),
              State('dataset-info', 'data'),
              State('kernel', 'value'),
              State('gamma', 'value'),
              prevent_initial_call=True)
def KPCA(n_clicks, n_components, dff, ds_info, kernel, gamma):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')

    KPCA = KernelPCA(n_components=n_components, kernel=kernel, gamma=gamma)
    components = KPCA.fit_transform(df.loc[:, df.columns != ds_info['label_column']])
    return create_figure(
                    n_components, 
                    df,
                    components,
                    ds_info['labeled'],
                    ds_info['label_column'],
                    get_explained_variance_ratio(components),
                    method='kpca'
            ), pd.DataFrame(components, columns=[i for i in range(n_components)]).to_json(date_format='iso', orient='split')


def get_explained_variance_ratio(transform):
    explained_variance = np.var(transform, axis=0)
    return explained_variance / np.sum(explained_variance)
