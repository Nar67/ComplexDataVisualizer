import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from utils.dimensionality_reduction_visualization import create_figure
from utils.data_type_check import check_all_categorical
from sklearn.decomposition import KernelPCA

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


KPCA_view = html.Div(id='KPCA-layout')


@app.callback(Output('KPCA-layout', 'children'),
              Input('data', 'data'))
def create_visualization_KPCA(dff):
    if dff is None:
        raise PreventUpdate
        return []
    df = pd.read_json(dff, orient='split')
    return html.Div([
        dcc.Store(id={'type': 'points', 'method': 'kpca'}, storage_type='session'),
        html.P("Choose labels column"),
        html.Div([
            dcc.Dropdown(
                id='feature-column',
                options=[{'label': i, 'value': i} for i in df.columns],
                value=df.columns[-1]
            ),
            dcc.Checklist(
                id='legend-checklist',
                options=[{'label': 'Color plot using labels column', 'value': 'True'}]
                )
        ]),
        html.P("Number of components:"),
        dcc.RadioItems(
                id='KPCA-components',
                options=[{'label': i, 'value': i} for i in [2, 3]],
                value=2,
                labelStyle={'margin-right': '12px'}
            ),

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
              Input('feature-column', 'value'),
              Input("KPCA-components", "value"),
              Input("legend-checklist", "value"),
              State('data', 'data'))
def KPCA(categories, n_components, color_legend, dff):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')

    KPCA = KernelPCA(n_components=n_components)
    components = KPCA.fit_transform(df.loc[:, df.columns != categories])

    return create_figure(
                    n_components, 
                    df, 
                    components, 
                    color_legend == None or color_legend == [],
                    categories,
                    KPCA.lambdas_,
                    method='kpca'
            ), pd.DataFrame(components, columns=[i for i in range(n_components)]).to_json(date_format='iso', orient='split')
