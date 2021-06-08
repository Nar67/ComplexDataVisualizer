import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from sklearn.decomposition import PCA


import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

import plotly.express as px


@app.callback(
    Output('viz-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('data', 'data'))
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type, dff):
    if dff is None:
        raise PreventUpdate
    
    df = pd.read_json(dff, orient='split')

    fig = go.Figure(data=[go.Scatter(
            x=df[xaxis_column_name],
            y=df[yaxis_column_name],
            # name='Scatter',
            mode= 'markers'
    )], layout ={'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'}
    )

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    return fig


@app.callback(Output('viz-layout', 'children'),
              Input('data', 'data'))
def create_visualization(dff):
    if dff is None:
        raise PreventUpdate
        return []
    df = pd.read_json(dff, orient='split')
    return html.Div([
        dbc.Button("PCA", color="primary", id="pca_btn"),
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in df.columns],
                value=df.columns[0]
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in df.columns],
                value=df.columns[0]
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='feature-column',
                options=[{'label': i, 'value': i} for i in df.columns],
                value=df.columns[-1]
            )
        ]),
        
        dcc.Graph(id='viz-graphic')
    ])




#Callback for the PCA button 
@app.callback(Output('viz-graphic', 'figure'),
              Input('pca_btn', 'n_clicks'), 
              Input('feature-column', 'value'),
              State('data', 'data'), prevent_initial_call=True)
def pca(n_clicks, features, dff):
    if dff is None:
        raise PreventUpdate
    
    df = pd.read_json(dff, orient='split')

    pca = PCA()
    components = pca.fit_transform(df[features])
    labels = {
        str(i): f"PC {i+1} ({var:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_ * 100)
    }

    fig = px.scatter_matrix(
    components,
    labels=labels,
    color=df[features]
    )

    return fig


