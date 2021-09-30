import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from sklearn.decomposition import PCA
from utils.dimensionality_reduction_visualization import create_figure



import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


pca_view = html.Div(id='pca-layout')


@app.callback(Output('tolerance-div', 'hidden'),
              Input('svd-solver', 'value'))
def show_input(solver):
    return solver != 'arpack'


@app.callback(Output('pca-layout', 'children'),
              Input('data', 'data'),
              State('dataset-info', 'data'))
def create_visualization_pca(dff, ds_info):
    if dff is None:
        raise PreventUpdate
        return []
    df = pd.read_json(dff, orient='split')
    return html.Div([
        dcc.Store(id={'type': 'points', 'method': 'pca'}, storage_type='session'),
        dcc.Markdown('''
            ##### Choose SVD solver:
            '''),
            html.Div([
            dcc.Dropdown(
                id='svd-solver',
                options=[{'label': i, 'value': i} for i in ['auto', 'full', 'arpack', 'randomized']],
                value='auto'
            ),
            html.Div(id='tolerance-div', hidden=True, children=[
                dcc.Markdown('''
                    ##### Choose tolerance for singular values:
                    '''),                
                dcc.Input(
                id='tolerance',
                placeholder='0.0',
                type='number'
                )
            ])
        ]),

        dcc.Markdown('''
            ##### Number of components:
            '''),
        dcc.RadioItems(
                id='pca-components',
                options=[{'label': i, 'value': i} for i in [2, 3]],
                value=2,
                labelStyle={'margin-right': '12px'}
            ),

        dbc.Button("Generate", color='primary', outline=True, id={'generate': 'pca'}),

        html.Div([dcc.Graph(id='pca-graphic', style={'height': '90vh', 'width': '90vh'})],
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
        ),

        html.Div([dbc.Button("Export PCA", color='primary', outline=True, id={'type': 'export_points', 'method': 'pca'}, style={'margin-right':'12px'}),
                     dcc.Download(id={'type': 'download_points_btn', 'method' : 'pca'}), 
                  dbc.Button("Export Coefs", color='primary', outline=True, id={'type': 'export_coefs', 'method': 'pca'}, style={'margin-right':'12px'}), 
                    dcc.Download(id={'type': 'download_coefs_btn', 'method' : 'pca'})])
    ])




#Callback for the PCA 
@app.callback(Output('pca-graphic', 'figure'),
              Output({'type': 'points', 'method': 'pca'}, 'data'),
              Input({'generate': 'pca'}, 'n_clicks'),
              State("pca-components", "value"),
              State('data', 'data'),
              State('dataset-info', 'data'),
              State('svd-solver', 'value'),
              State('tolerance', 'value'),
              prevent_initial_call=True)
def pca(n_clicks, n_components, dff, ds_info, solver, tolerance):
    if dff is None:
        raise PreventUpdate
    
            
    df = pd.read_json(dff, orient='split')

    pca = PCA(n_components=n_components)
    components = pca.fit_transform(df.loc[:, df.columns != ds_info['label_column']])
    print('PCA done!')
    return create_figure(
                    n_components, 
                    df, 
                    components, 
                    ds_info['labeled'],
                    ds_info['label_column'],
                    pca.explained_variance_ratio_,
                    method='pca',
                    pca=pca
            ), pd.DataFrame(components, columns=[i for i in range(n_components)]).to_json(date_format='iso', orient='split')
