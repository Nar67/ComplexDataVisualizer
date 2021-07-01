import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from utils.dimensionality_reduction_visualization import create_figure


import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc



fda_view = html.Div(id='fda-layout')


@app.callback(Output('fda-layout', 'children'),
              Input('data', 'data'))
def create_visualization_fda(dff):
    if dff is None:
        raise PreventUpdate
        return []
    df = pd.read_json(dff, orient='split')
    return html.Div([
        html.P("Choose labels column"),
        html.Div([
            dcc.Dropdown(
                id='feature-column-fda',
                options=[{'label': i, 'value': i} for i in df.columns],
                value=df.columns[-1]
            ),
            dcc.Checklist(
                id='legend-checklist-fda',
                options=[{'label': 'Color plot using labels column', 'value': 'True'}]
                )
        ]),

        html.P("Number of components:"),
        dcc.Slider(
            id='fda-slider',
            min=2, max=5, value=2,
            marks={i: str(i) for i in range(2,6)}),

        html.Div([dcc.Graph(id='fda-graphic', style={'height': '90vh', 'width': '90vh'})],
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
        )
    ])




#Callback for the FDA 
@app.callback(Output('fda-graphic', 'figure'),
              Input('feature-column-fda', 'value'),
              Input("fda-slider", "value"),
              Input("legend-checklist-fda", "value"),
              State('data', 'data'))
def fda(categories, n_components, color_legend, dff):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')

    fda = LinearDiscriminantAnalysis(n_components=n_components)
    components = fda.fit_transform(df.loc[:, df.columns != categories], df[categories])

    return create_figure(
                    n_components, 
                    df, 
                    components, 
                    color_legend == None or color_legend == [],
                    categories,
                    fda.explained_variance_ratio_,
                    fda=fda,
            )
