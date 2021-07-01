import plotly.graph_objs as go
from plotly.subplots import make_subplots

def create_figure(n_components, df, components, color_graph, categories, explained_variance, pca=None, fda=None):
    if pca == None and fda == None:
        return
    method_string = 'PC' if pca != None else 'LD'
    fig = go.Figure()
    if n_components == 2:
        for category in df[categories].unique():
            indexes = df.index[df[categories] == category].tolist()
            fig.add_trace(go.Scatter(
                    x=[components[i][0] for i in indexes],
                    y=[components[i][1] for i in indexes],
                    mode='markers',
                    name=str(category),
                    hovertemplate='<br><b>' + method_string + '1</b>: %{x}<br>' + 
                                '<br><b>' + method_string + '2</b>: %{y}<br>' + 
                                '<br><b>Index</b>: %{text}<br><extra></extra>', 
                                text=[str(i) for i in indexes],
            ))
    
        fig.update_xaxes(
            title_text = "{ax} 1 ({var:.1f}%)".format(ax=method_string, var=explained_variance[0]*100)
        )
        fig.update_yaxes(
            title_text = "{ax} 2 ({var:.1f}%)".format(ax=method_string, var=explained_variance[1]*100),
            scaleanchor = "x",
            scaleratio = 1,
        )
    elif n_components == 3:
        for category in df[categories].unique():
            indexes = df.index[df[categories] == category].tolist()
            fig.add_trace(go.Scatter3d(
                    x=[components[i][0] for i in indexes],
                    y=[components[i][1] for i in indexes],
                    z=[components[i][2] for i in indexes],
                    mode='markers',
                    name=str(category),
                    hovertemplate='<br><b>' + method_string + '1</b>: %{x}<br>' + 
                                '<br><b>' + method_string + '2</b>: %{y}<br>' + 
                                '<br><b>' + method_string + '3</b>: %{z}<br>' + 
                                '<br><b>Index</b>: %{text}<br><extra></extra>', 
                                text=[str(i) for i in indexes],
            ))
    
        fig.update_yaxes(
            scaleanchor = "x",
            scaleratio = 1,
        )

        fig.update_traces(marker_size=4)

        fig.update_layout(scene = dict(
            xaxis_title="{ax} 1 ({var:.1f}%)".format(ax=method_string, var=explained_variance[0]*100),
            yaxis_title="{ax} 2 ({var:.1f}%)".format(ax=method_string, var=explained_variance[1]*100),
            zaxis_title="{ax} 3 ({var:.1f}%)".format(ax=method_string, var=explained_variance[2]*100),
        ))
        #uses 'data' which preserves the proportion of axes ranges unless one axis is 4 times the others, then 'cube' is used
        fig.update_scenes(aspectmode='auto') 
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
                    fig.update_xaxes(title_text="{ax} {ld} ({var:.1f}%)".format(ax=method_string, ld=i, var=explained_variance[i-1]*100), row=i, col=j)
                    fig.update_yaxes(title_text="{ax} {ld} ({var:.1f}%)".format(ax=method_string, ld=i, var=explained_variance[j-1]*100), row=i, col=j)

    if color_graph and fda == None:
        fig.update_traces(
            marker_color='blue',
            marker=dict(
                color='blue'
            ),
        )
        fig.update_layout(showlegend=False)   
    return fig