import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from utils.dimensionality_reduction_visualization import create_mds_figure
from utils.data_type_check import check_all_categorical
from sklearn.manifold import MDS

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


mds_view = html.Div(id='mds-layout')


@app.callback(Output('mds-layout', 'children'),
              Input('data', 'data'))
def create_visualization_mds(dff):
    if dff is None:
        raise PreventUpdate
        return []
    df = pd.read_json(dff, orient='split')
    return html.Div([
        dcc.Store(id={'type': 'points', 'method': 'mds'}, storage_type='session'),
        html.Div([
            dcc.Markdown('''
                    ##### Choose dissimilarity measure:
                    '''),                
            dcc.Dropdown(
                id='dissimilarity',
                options=[{'label': i, 'value': i} for i in ['euclidean', 'precomputed']],
                value='euclidean'
            ),
            dcc.Checklist(
                id='metric-checklist',
                options=[{'label': 'Use metric MDS', 'value': 'True'}],
                style={'margin-top': '20px'}
                ),
            ]),
        dcc.Markdown('''
        ##### Number of components:
        '''),
        dcc.RadioItems(
                id='mds-components',
                options=[{'label': i, 'value': i} for i in [2, 3]],
                value=2,
                labelStyle={'margin-right': '12px'}
            ),

        dbc.Button("Generate", color='primary', outline=True, id={'generate': 'mds'}),

        html.Div([dcc.Graph(id='mds-graphic', style={'height': '90vh', 'width': '90vh'})],
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
        ),

        html.Div([dbc.Button("Export MDS", color='primary', outline=True, id={'type': 'export_points', 'method': 'mds'}, style={'margin-right':'12px'}),
                     dcc.Download(id={'type': 'download_points_btn', 'method' : 'mds'}), 
                  dbc.Button("Export Coefs", color='primary', outline=True, id={'type': 'export_coefs', 'method': 'mds'}, style={'margin-right':'12px'}), 
                    dcc.Download(id={'type': 'download_coefs_btn', 'method' : 'mds'})])
    ])


#Callback for the mds 
@app.callback(Output('mds-graphic', 'figure'),
              Output({'type': 'points', 'method': 'mds'}, 'data'),
              Input({'generate': 'mds'}, 'n_clicks'),
              State("mds-components", "value"),
              State('data', 'data'),
              State('metric-checklist', 'value'),
              State('dissimilarity', 'value'),
              State('dataset-info', 'data'),
              prevent_initial_call=True)
def mds(n_clicks, n_components, dff, metric, dissimilarity, ds_info):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')

    mds = MDS(n_components=n_components, metric=metric, dissimilarity=dissimilarity)
    components = mds.fit_transform(df.loc[:, df.columns != ds_info['label_column']])

    return create_mds_figure(
                    n_components, 
                    df, 
                    components,
                    ds_info['labeled'],
                    ds_info['label_column'],
                    mds.stress_,
            ), pd.DataFrame(components, columns=[i for i in range(n_components)]).to_json(date_format='iso', orient='split')
