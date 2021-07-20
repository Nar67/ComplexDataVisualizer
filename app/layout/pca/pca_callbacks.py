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


@app.callback(Output('pca-layout', 'children'),
              Input('data', 'data'))
def create_visualization_pca(dff):
    if dff is None:
        raise PreventUpdate
        return []
    df = pd.read_json(dff, orient='split')
    return html.Div([
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
                id='pca-components',
                options=[{'label': i, 'value': i} for i in [2, 3]],
                value=2,
                labelStyle={'margin-right': '12px'}
            ),

        html.Div([dcc.Graph(id='pca-graphic', style={'height': '90vh', 'width': '90vh'})],
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
        ),

        html.Div([dbc.Button("Export PCA", color='primary', outline=True, id="export-pca", style={'margin-right':'12px'}), dcc.Download(id="download-pca"), 
                  dbc.Button("Export Coefs", color='primary', outline=True, id="export-pca-coefs"), dcc.Download(id="download-pca-coefs")])
    ])




#Callback for the PCA 
@app.callback(Output('pca-graphic', 'figure'),
              Input('feature-column', 'value'),
              Input("pca-components", "value"),
              Input("legend-checklist", "value"),
              State('data', 'data'))
def pca(categories, n_components, color_legend, dff):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')

    pca = PCA(n_components=n_components)
    components = pca.fit_transform(df.loc[:, df.columns != categories])

    return create_figure(
                    n_components, 
                    df, 
                    components, 
                    color_legend == None or color_legend == [],
                    categories,
                    pca.explained_variance_ratio_,
                    pca=pca,
            )


#improve both callbacks to use a stored pca instead of computing it again.
@app.callback(
    Output("download-pca", "data"),
    Input("export-pca", "n_clicks"),
    Input('feature-column', 'value'),
    Input("pca-components", "value"),
    State('data', 'data'),
    prevent_initial_call=True,
)
def download_pca(n_clicks, categories, n_components, dff):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')
    pca = PCA(n_components=n_components)
    components = pca.fit_transform(df.loc[:, df.columns != categories])

    df = pd.DataFrame(components, columns=[i for i in range(n_components)])
    return dcc.send_data_frame(df.to_csv, "pca.csv")


@app.callback(
    Output("download-pca-coefs", "data"),
    Input("export-pca-coefs", "n_clicks"),
    Input('feature-column', 'value'),
    Input("pca-components", "value"),
    State('data', 'data'),
    prevent_initial_call=True,
)
def download_pca_coefs(n_clicks, categories, n_components, dff):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')
    pca = PCA(n_components=n_components)
    pca.fit_transform(df.loc[:, df.columns != categories])

    df = pd.DataFrame(pca.components_.T, columns=["PC{i}".format(i=i+1) for i in range(n_components)], index=df.columns[df.columns != categories])
    return dcc.send_data_frame(df.to_csv, "pca_coefs.csv")