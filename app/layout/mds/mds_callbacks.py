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
                id='mds-components',
                options=[{'label': i, 'value': i} for i in [2, 3]],
                value=2,
                labelStyle={'margin-right': '12px'}
            ),

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
              Input("mds-components", "value"),
              Input('feature-column', 'value'),
              Input("legend-checklist", "value"),
              State('data', 'data'))
def mds(n_components, categories, color_legend, dff):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')

    mds = MDS(n_components=n_components)
    components = mds.fit_transform(df.loc[:, df.columns != categories])

    return create_mds_figure(
                    n_components, 
                    df, 
                    components,
                    True,
                    categories,
                    mds.stress_,
            ), pd.DataFrame(components, columns=[i for i in range(n_components)]).to_json(date_format='iso', orient='split')
