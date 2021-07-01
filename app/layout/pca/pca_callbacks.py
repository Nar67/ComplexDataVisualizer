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
        dcc.Slider(
            id='pca-slider',
            min=2, max=5, value=2,
            marks={i: str(i) for i in range(2,6)}),

        html.Div([dcc.Graph(id='pca-graphic', style={'height': '90vh', 'width': '90vh'})],
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
        )
    ])




#Callback for the PCA 
@app.callback(Output('pca-graphic', 'figure'),
              Input('feature-column', 'value'),
              Input("pca-slider", "value"),
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