import pandas as pd
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate
from app import app
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from utils.dimensionality_reduction_visualization import create_figure
import dash

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc



lda_view = html.Div(id='lda-layout')

hidden = {
    'shrinkage-div': ['eigen'],
}

@app.callback(Output({'lda-div': MATCH}, 'hidden'),
              Input('solver-lda', 'value'))
def show_input(solver):
    return solver not in hidden[dash.callback_context.outputs_list['id']['lda-div']]



@app.callback(Output('lda-layout', 'children'),
              Input('data', 'data'))
def create_visualization_lda(dff):
    if dff is None:
        raise PreventUpdate
        return []
    df = pd.read_json(dff, orient='split')
    return html.Div([
        dcc.Store(id={'type': 'points', 'method': 'lda'}, storage_type='session'),
        dcc.Markdown('''
            ##### Choose solver for the LDA:
            '''),
            html.Div([
            dcc.Dropdown(
                id='solver-lda',
                options=[{'label': i, 'value': i} for i in ['svd', 'eigen']],
                value='svd'
            ),
            html.Div(id={'lda-div': 'shrinkage-div'}, hidden=True, children=[
                dcc.Markdown('''
                    ##### Choose shrinkage for solver:
                    '''),                
                dcc.Input(
                id='shrinkage',
                placeholder='\'auto\', \'None\' or float [0-1]',
                type='text',
                pattern='(auto)|(None)|(^(?:0*(?:\.\d+)?|1(\.0*)?)$)'
                )
            ])]),

        dcc.Markdown('''
            ##### Number of components:
            '''),
        dcc.RadioItems(
                id='lda-components',
                options=[{'label': i, 'value': i} for i in [2, 3]],
                value=2,
                labelStyle={'margin-right': '12px'}
            ),

        dbc.Button("Generate", color='primary', outline=True, id={'generate': 'lda'}),


        html.Div([dcc.Graph(id='lda-graphic', style={'height': '90vh', 'width': '90vh'})],
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
        ),

        html.Div([dbc.Button("Export LDA", color='primary', outline=True, id={'type': 'export_points', 'method': 'lda'}, style={'margin-right':'12px'}),
                     dcc.Download(id={'type': 'download_points_btn', 'method' : 'lda'}), 
                  dbc.Button("Export Coefs", color='primary', outline=True, id={'type': 'export_coefs', 'method': 'lda'}, style={'margin-right':'12px'}), 
                    dcc.Download(id={'type': 'download_coefs_btn', 'method' : 'lda'})])
    ])




#Callback for the lda 
@app.callback(Output('lda-graphic', 'figure'),
              Output({'type': 'points', 'method': 'lda'}, 'data'),
              Input({'generate': 'lda'}, 'n_clicks'),
              State("lda-components", "value"),
              State('data', 'data'),
              State('solver-lda', 'value'),
              State('shrinkage', 'value'),
              State('dataset-info', 'data'),
              prevent_initial_call=True)
def lda(n_clicks, n_components, dff, solver, shrinkage, ds_info):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')

    lda = LinearDiscriminantAnalysis(n_components=n_components, solver=solver, shrinkage= None if shrinkage == 'None' else shrinkage)
    components = lda.fit_transform(df.loc[:, df.columns != ds_info['label_column']], df[ds_info['label_column']])

    return create_figure(
                    n_components, 
                    df, 
                    components, 
                    ds_info['labeled'],
                    ds_info['label_column'],
                    lda.explained_variance_ratio_,
                    method='lda'
            ), pd.DataFrame(components, columns=[i for i in range(n_components)]).to_json(date_format='iso', orient='split')


# @app.callback(
#     Output("download-lda-coefs", "data"),
#     Input("export-lda-coefs", "n_clicks"),
#     Input('feature-column-lda', 'value'),
#     Input("lda-components", "value"),
#     State('data', 'data'),
#     prevent_initial_call=True,
# )
# def download_lda_coefs(n_clicks, categories, n_components, dff):
#     if dff is None:
#         raise PreventUpdate
            
#     df = pd.read_json(dff, orient='split')
    
#     lda = LinearDiscriminantAnalysis(n_components=n_components)
#     lda.fit_transform(df.loc[:, df.columns != categories], df[categories])

#     df = pd.DataFrame(lda.scalings_, columns=["LD{i}".format(i=i+1) for i in range(n_components)], index=df.columns[df.columns != categories])
#     return dcc.send_data_frame(df.to_csv, "lda_coefs.csv")