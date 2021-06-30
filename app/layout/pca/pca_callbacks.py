import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from sklearn.decomposition import PCA


import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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




#Callback for the PCA button 
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

    if n_components == 2:
        fig = go.Figure()

        for category in df[categories].unique():
            indexes = df.index[df[categories] == category].tolist()
            fig.add_trace(go.Scatter(
                    x=[components[i][0] for i in indexes],
                    y=[components[i][1] for i in indexes],
                    mode='markers',
                    name=str(category),
                    hovertemplate='<br><b>PC1</b>: %{x}<br>' + 
                                '<br><b>PC2</b>: %{y}<br>' + 
                                '<br><b>Index</b>: %{text}<br><extra></extra>', 
                                text=[str(i) for i in indexes],
            ))
        
        if color_legend == None or color_legend == []:
            fig.update_traces(marker_color='blue')
            fig.update_layout(showlegend=False)
    
        fig.update_xaxes(
            title_text = "PC 1 ({var:.1f}%)".format(var=pca.explained_variance_ratio_[0]*100)
        )
        fig.update_yaxes(
            title_text = "PC 2 ({var:.1f}%)".format(var=pca.explained_variance_ratio_[1]*100),
            scaleanchor = "x",
            scaleratio = 1,
        )
        return fig
    elif n_components == 3:
        fig = go.Figure()
        for category in df[categories].unique():
            indexes = df.index[df[categories] == category].tolist()
            fig.add_trace(go.Scatter3d(
                    x=[components[i][0] for i in indexes],
                    y=[components[i][1] for i in indexes],
                    z=[components[i][2] for i in indexes],
                    mode='markers',
                    name=str(category),
                    hovertemplate='<br><b>PC1</b>: %{x}<br>' + 
                                '<br><b>PC2</b>: %{y}<br>' + 
                                '<br><b>Index</b>: %{text}<br><extra></extra>', 
                                text=[str(i) for i in indexes],
            ))
        
        if color_legend == None or color_legend == []:
            fig.update_traces(marker_color='blue')
            fig.update_layout(showlegend=False)
    
        fig.update_yaxes(
            scaleanchor = "x",
            scaleratio = 1,
        )

        fig.update_layout(scene = dict(
            xaxis_title="PC 1 ({var:.1f}%)".format(var=pca.explained_variance_ratio_[0]*100),
            yaxis_title="PC 2 ({var:.1f}%)".format(var=pca.explained_variance_ratio_[1]*100),
            zaxis_title="PC 3 ({var:.1f}%)".format(var=pca.explained_variance_ratio_[2]*100)),
        )
        fig.update_scenes(aspectmode='auto') #uses 'data' which preserves the proportion of axes ranges unless one axis is 4 times the others, then 'cube' is used
        
        return fig      
    else:
        fig = make_subplots(rows=n_components , cols=n_components)

        for i in range(1, n_components+1):
            for j in range(1, n_components+1):
                if i != j:
                    for category in df[categories].unique():
                        indexes = df.index[df[categories] == category].tolist()
                        fig.add_trace(
                            go.Scatter(
                            x=[components[k][i-1] for k in indexes],
                            y=[components[k][j-1] for k in indexes],
                            mode='markers',
                            name=str(category),
                            hovertemplate='<br><b>x:</b>: %{x}<br>' + 
                                        '<br><b>y:</b>: %{y}<br>' + 
                                        '<br><b>Index</b>: %{text}<br><extra></extra>', 
                                        text=[str(i) for i in indexes],
                        ), row=i, col=j)
                    fig.update_xaxes(title_text="PC {pc} ({var:.1f}%)".format(pc=i, var=pca.explained_variance_ratio_[0]*100), row=i, col=j)
                    fig.update_yaxes(title_text="PC {pc} ({var:.1f}%)".format(pc=i, var=pca.explained_variance_ratio_[0]*100), row=i, col=j)

        
        return fig
