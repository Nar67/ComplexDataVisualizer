import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots


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

    if n_components == 2:
        fig = go.Figure()
        for category in df[categories].unique():
            indexes = df.index[df[categories] == category].tolist()
            fig.add_trace(go.Scatter(
                    x=[components[i][0] for i in indexes],
                    y=[components[i][1] for i in indexes],
                    mode='markers',
                    name=str(category),
                    hovertemplate='<br><b>LD1</b>: %{x}<br>' + 
                                '<br><b>LD2</b>: %{y}<br>' + 
                                '<br><b>Index</b>: %{text}<br><extra></extra>', 
                                text=[str(i) for i in indexes],
            ))
        
        if color_legend == None or color_legend == []:
            fig.update_traces(marker_color='blue')
            fig.update_layout(showlegend=False)
    
        fig.update_xaxes(
            title_text = "LD 1 ({var:.1f}%)".format(var=fda.explained_variance_ratio_[0]*100)
        )
        fig.update_yaxes(
            title_text = "LD 2 ({var:.1f}%)".format(var=fda.explained_variance_ratio_[1]*100),
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
                    hovertemplate='<br><b>LD1</b>: %{x}<br>' + 
                                '<br><b>LD2</b>: %{y}<br>' + 
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
            xaxis_title="LD 1 ({var:.1f}%)".format(var=fda.explained_variance_ratio_[0]*100),
            yaxis_title="LD 2 ({var:.1f}%)".format(var=fda.explained_variance_ratio_[1]*100),
            zaxis_title="LD 3 ({var:.1f}%)".format(var=fda.explained_variance_ratio_[2]*100)),
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
                    fig.update_xaxes(title_text="LD {ld} ({var:.1f}%)".format(ld=i, var=fda.explained_variance_ratio_[0]*100), row=i, col=j)
                    fig.update_yaxes(title_text="LD {ld} ({var:.1f}%)".format(ld=i, var=fda.explained_variance_ratio_[0]*100), row=i, col=j)

        
        return fig
