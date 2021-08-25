import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from utils.dimensionality_reduction_visualization import create_mca_figure
from utils.data_type_check import check_all_categorical
from prince import MCA


import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


mca_view = html.Div(id='mca-layout')


@app.callback(Output('mca-layout', 'children'),
              Input('data', 'data'))
def create_visualization_mca(dff):
    if dff is None:
        raise PreventUpdate
        return []
    df = pd.read_json(dff, orient='split')
    return html.Div([
        html.P("Number of components:"),
        dcc.RadioItems(
                id='mca-components',
                options=[{'label': i, 'value': i} for i in [2, 3]],
                value=2,
                labelStyle={'margin-right': '12px'}
            ),

        html.Div([dcc.Graph(id='mca-graphic', style={'height': '90vh', 'width': '90vh'})],
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
        ),

        html.Div([dbc.Button("Export MCA", color='primary', outline=True, id="export-mca", style={'margin-right':'12px'}), dcc.Download(id="download-mca"), 
                  dbc.Button("Export Coefs", color='primary', outline=True, id="export-mca-coefs"), dcc.Download(id="download-mca-coefs")])
    ])




#Callback for the mca 
@app.callback(Output('mca-graphic', 'figure'),
              Input("mca-components", "value"),
              State('data', 'data'))
def mca(n_components, dff):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')

    # if not check_all_categorical(df):
    #     return

    mca = MCA(n_components=n_components)
    components = mca.fit_transform(df)

    return create_mca_figure(
                    n_components, 
                    df, 
                    components, 
                    mca.explained_inertia_,
            )


# #improve both callbacks to use a stored mca instead of computing it again.
# @app.callback(
#     Output("download-mca", "data"),
#     Input("export-mca", "n_clicks"),
#     Input('feature-column', 'value'),
#     Input("mca-components", "value"),
#     State('data', 'data'),
#     prevent_initial_call=True,
# )
# def download_mca(n_clicks, categories, n_components, dff):
#     if dff is None:
#         raise PreventUpdate
            
#     df = pd.read_json(dff, orient='split')
#     mca = mca(n_components=n_components)
#     components = mca.fit_transform(df.loc[:, df.columns != categories])

#     df = pd.DataFrame(components, columns=[i for i in range(n_components)])
#     return dcc.send_data_frame(df.to_csv, "mca.csv")


# @app.callback(
#     Output("download-mca-coefs", "data"),
#     Input("export-mca-coefs", "n_clicks"),
#     Input('feature-column', 'value'),
#     Input("mca-components", "value"),
#     State('data', 'data'),
#     prevent_initial_call=True,
# )
# def download_mca_coefs(n_clicks, categories, n_components, dff):
#     if dff is None:
#         raise PreventUpdate
            
#     df = pd.read_json(dff, orient='split')
#     mca = mca(n_components=n_components)
#     mca.fit_transform(df.loc[:, df.columns != categories])

#     df = pd.DataFrame(mca.components_.T, columns=["PC{i}".format(i=i+1) for i in range(n_components)], index=df.columns[df.columns != categories])
#     return dcc.send_data_frame(df.to_csv, "mca_coefs.csv")