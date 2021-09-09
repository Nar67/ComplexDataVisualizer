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
        dcc.Store(id={'type': 'points', 'method': 'fda'}, storage_type='session'),
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
        dcc.RadioItems(
                id='fda-components',
                options=[{'label': i, 'value': i} for i in [2, 3]],
                value=2,
                labelStyle={'margin-right': '12px'}
            ),

        html.Div([dcc.Graph(id='fda-graphic', style={'height': '90vh', 'width': '90vh'})],
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
        ),

        html.Div([dbc.Button("Export FDA", color='primary', outline=True, id={'type': 'export_points', 'method': 'fda'}, style={'margin-right':'12px'}),
                     dcc.Download(id={'type': 'download_points_btn', 'method' : 'fda'}), 
                  dbc.Button("Export Coefs", color='primary', outline=True, id={'type': 'export_coefs', 'method': 'fda'}, style={'margin-right':'12px'}), 
                    dcc.Download(id={'type': 'download_coefs_btn', 'method' : 'fda'})])
    ])




#Callback for the FDA 
@app.callback(Output('fda-graphic', 'figure'),
              Output({'type': 'points', 'method': 'fda'}, 'data'),
              Input('feature-column-fda', 'value'),
              Input("fda-components", "value"),
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
                    method='fda'
            ), pd.DataFrame(components, columns=[i for i in range(n_components)]).to_json(date_format='iso', orient='split')

#improve both callbacks to use a stored pca instead of computing it again.
@app.callback(
    Output("download-fda", "data"),
    Input("export-fda", "n_clicks"),
    Input('feature-column-fda', 'value'),
    Input("fda-components", "value"),
    State('data', 'data'),
    prevent_initial_call=True,
)
def download_fda(n_clicks, categories, n_components, dff):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')
    
    fda = LinearDiscriminantAnalysis(n_components=n_components)
    components = fda.fit_transform(df.loc[:, df.columns != categories], df[categories])

    df = pd.DataFrame(components, columns=[i for i in range(n_components)])
    return dcc.send_data_frame(df.to_csv, "fda.csv")


@app.callback(
    Output("download-fda-coefs", "data"),
    Input("export-fda-coefs", "n_clicks"),
    Input('feature-column-fda', 'value'),
    Input("fda-components", "value"),
    State('data', 'data'),
    prevent_initial_call=True,
)
def download_fda_coefs(n_clicks, categories, n_components, dff):
    if dff is None:
        raise PreventUpdate
            
    df = pd.read_json(dff, orient='split')
    
    fda = LinearDiscriminantAnalysis(n_components=n_components)
    fda.fit_transform(df.loc[:, df.columns != categories], df[categories])

    df = pd.DataFrame(fda.scalings_, columns=["LD{i}".format(i=i+1) for i in range(n_components)], index=df.columns[df.columns != categories])
    return dcc.send_data_frame(df.to_csv, "fda_coefs.csv")