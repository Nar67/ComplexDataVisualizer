import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from sklearn.decomposition import PCA


import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

import plotly.express as px




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
            )
        ]),

        html.P("Number of components:"),
        dcc.Slider(
            id='pca-slider',
            min=2, max=5, value=2,
            marks={i: str(i) for i in range(2,6)}),

        
        dcc.Graph(id='pca-graphic')
    ])




#Callback for the PCA button 
@app.callback(Output('pca-graphic', 'figure'),
              Input('feature-column', 'value'),
              Input("pca-slider", "value"),
              State('data', 'data'))
def pca(categories, n_components, dff):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')

    pca = PCA(n_components=n_components)
    components = pca.fit_transform(df.loc[:, df.columns != categories])
    labels = {
        str(i): f"PC {i+1} ({var*100:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_)
    }

    if n_components == 2:
        print(labels)
        return px.scatter(
            components,
            color=df[categories].tolist(),
            labels=labels
        )
    else:
        fig = px.scatter_matrix(
            components,
            labels=labels,
            dimensions=range(n_components),
            color=df[categories].tolist()
        )
        fig.update_traces(diagonal_visible=False)
        return fig

