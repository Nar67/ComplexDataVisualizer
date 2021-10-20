import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from utils.dimensionality_reduction_visualization import create_figure_tSNE
from utils.data_type_check import check_all_categorical
from sklearn.manifold import TSNE

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


tSNE_view = html.Div(id='tSNE-layout')


@app.callback(Output('tSNE-layout', 'children'),
              Input('data', 'data'))
def create_visualization_tSNE(dff):
    if dff is None:
        raise PreventUpdate
        return []
    df = pd.read_json(dff, orient='split')
    return html.Div([
        dcc.Store(id={'type': 'points', 'method': 'tSNE'}, storage_type='session'),
        html.Div([
            dcc.Markdown('''
            ##### Choose perplexity:
            '''),
            dcc.Input(
                id='perplexity',
                placeholder='30.0',
                type='number'
                ),
            dcc.Markdown('''
            ##### Choose early exaggeration:
            '''),
            dcc.Input(
                id='early-exaggeration',
                placeholder='12.0',
                type='number'
                ),
            dcc.Markdown('''
            ##### Choose learning rate:
            '''),
            dcc.Input(
                id='learning-rate',
                placeholder='200.0',
                type='number'
                ),
            ]),
            dcc.Markdown('''
            ##### Number of components:
            '''),        
            dcc.RadioItems(
                id='tSNE-components',
                options=[{'label': i, 'value': i} for i in [2, 3]],
                value=2,
                labelStyle={'margin-right': '12px'}
            ),

            dbc.Button("Generate", color='primary', outline=True, id={'generate': 'tSNE'}),


        html.Div([dcc.Graph(id='tSNE-graphic', style={'height': '90vh', 'width': '90vh'})],
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
        ),

        html.Div([dbc.Button("Export tSNE", color='primary', outline=True, id={'type': 'export_points', 'method': 'tSNE'}, style={'margin-right':'12px'}),
                     dcc.Download(id={'type': 'download_points_btn', 'method' : 'tSNE'}), 
                  dbc.Button("Export Coefs", color='primary', outline=True, id={'type': 'export_coefs', 'method': 'tSNE'}, style={'margin-right':'12px'}), 
                    dcc.Download(id={'type': 'download_coefs_btn', 'method' : 'tSNE'})])
    ])



#Callback for the tSNE 
@app.callback(Output('tSNE-graphic', 'figure'),
              Output({'type': 'points', 'method': 'tSNE'}, 'data'),
              Input({'generate': 'tSNE'}, 'n_clicks'),
              State("tSNE-components", "value"),
              State('data', 'data'),
              State('perplexity', 'value'),
              State('early-exaggeration', 'value'),
              State('learning-rate', 'value'),
              State('dataset-info', 'data'),
              prevent_initial_call=True)
def tSNE(n_clicks, n_components, dff, perplexity, exaggeration, learning_rate, ds_info):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')

    tSNE = TSNE(n_components=n_components, 
                perplexity=perplexity if perplexity is not None else 12.0, 
                early_exaggeration=exaggeration if exaggeration is not None else 30.0, 
                learning_rate=learning_rate if learning_rate is not None else 200.0)
    components = tSNE.fit_transform(df.loc[:, df.columns != ds_info['label_column']])

    return create_figure_tSNE(
                    n_components, 
                    df, 
                    components, 
                    ds_info['labeled'],
                    ds_info['label_column'],
                    tSNE.kl_divergence_
            ), pd.DataFrame(components, columns=[i for i in range(n_components)]).to_json(date_format='iso', orient='split')
