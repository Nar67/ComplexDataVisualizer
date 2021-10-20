import plotly.graph_objs as go
from plotly.subplots import make_subplots

def create_figure(n_components, df, components, color_graph, categories, explained_variance, method=None, pca=None):
    fig = fill_figure(n_components, df, components, explained_variance, color_graph, categories=categories, method=method)
    if method == 'pca':
        draw_arrows(fig, n_components, df, pca.components_.T, categories)
    return fig

def create_mca_figure(n_components, df, components, explained_inertia):
    return fill_figure(n_components, df, components, None, True, explained_inertia, method='mca')
     

def create_figure_tSNE(n_components, df, components, color_graph, categories, divergence):
    fig = fill_figure(n_components, df, components, None, color_graph, categories=categories, method='tSNE')
    fig.update_layout(title='Divergence: {div}'.format(div=divergence))
    return fig

def create_mds_figure(n_components, df, components, color_graph, categories, stress):
    fig = fill_figure(n_components, df, components, None, color_graph, categories=categories, method='mds')
    fig.update_layout(title='Stress: {st}'.format(st=stress))
    return fig

def fill_figure(n_components, df, data, metrics, color_graph, categories=None, method=None):
    fig = go.Figure()
    string = 'PC' if method == 'pca' or method == 'kpca' else 'LD' if method == 'lda' else 'Component' if method == 'mca' else 'Dimension'
    if n_components == 2:
        if method in ['pca', 'lda', 'kpca', 'mds', 'tSNE']:
            for category in df[categories].unique():
                indexes = df.index[df[categories] == category].tolist()
                fig.add_trace(go.Scatter(
                        x=[data[i][0] for i in indexes],
                        y=[data[i][1] for i in indexes],
                        mode='markers',
                        name=str(category),
                        hovertemplate=get_hovertemplate(n_components, indexes, string), text=[str(i) for i in indexes]
            ))
        else:
            indexes = df.index.tolist()
            fig.add_trace(go.Scatter(
                x=data[:][0],
                y=data[:][1],
                mode='markers',
                hovertemplate=get_hovertemplate(n_components, indexes, string), text=[str(i) for i in indexes]
        ))
        if metrics is not None:
            fig.update_xaxes(
                title_text = "{ax} 1 ({var:.1f}%)".format(ax=string, var=metrics[0]*100)
            )
            fig.update_yaxes(
                title_text = "{ax} 2 ({var:.1f}%)".format(ax=string, var=metrics[1]*100),
        )


    elif n_components == 3:
        if method in ['pca', 'lda', 'kpca', 'mds', 'tSNE']:
            for category in df[categories].unique():
                indexes = df.index[df[categories] == category].tolist()
                fig.add_trace(go.Scatter3d(
                        x=[data[i][0] for i in indexes],
                        y=[data[i][1] for i in indexes],
                        z=[data[i][2] for i in indexes],
                        mode='markers',
                        name=str(category),
                        hovertemplate=get_hovertemplate(n_components, indexes, string), text=[str(i) for i in indexes]
                ))
        else:
            indexes = df.index.tolist()
            fig.add_trace(go.Scatter3d(
                x=data[:][0],
                y=data[:][1],
                z=data[:][2],
                mode='markers',
                hovertemplate=get_hovertemplate(n_components, indexes, string), text=[str(i) for i in indexes]
                ))
        
        if metrics is not None:
            fig.update_layout(scene = dict(
                xaxis_title="{ax} 1 ({var:.1f}%)".format(ax=string, var=metrics[0]*100),
                yaxis_title="{ax} 2 ({var:.1f}%)".format(ax=string, var=metrics[1]*100),
                zaxis_title="{ax} 3 ({var:.1f}%)".format(ax=string, var=metrics[2]*100),
            ))
        #uses 'data' which preserves the proportion of axes ranges unless one axis is 4 times the others, then 'cube' is used
        fig.update_scenes(aspectmode='auto')  
        fig.update_traces(marker_size=4)
    
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
    )
    if not color_graph:
        fig.update_traces(
            marker_color='blue',
            marker=dict(
                color='blue'
            ),
        )
    return fig


def get_hovertemplate(n_components, indexes, string):
    if n_components == 2:
        return '<br><b>' + string + ' 1</b>: %{x}<br>' + '<br><b>' + string + ' 2</b>: %{y}<br>' +  '<br><b>Index</b>: %{text}<br><extra></extra>'
    else:
        return '<br><b>' + string + '1</b>: %{x}<br>' + '<br><b>' + string + '2</b>: %{y}<br>' + '<br><b>' + string + '3</b>: %{z}<br>' + '<br><b>Index</b>: %{text}<br><extra></extra>'


def draw_arrows(fig, n_components, df, components, categories):
    if n_components == 2:
        for i, col in enumerate(df.drop(categories, axis=1).columns):
            fig.add_trace(go.Scatter(
                x = [0,components[i][0]],
                y = [0,components[i][1]],
                marker = dict(size = 1, color = "rgb(250,0,0)"),
                line = dict(width = 2),
                name = col,
                showlegend=False
            ))
    elif n_components == 3:
        for i, col in enumerate(df.drop(categories, axis=1).columns):
            fig.add_trace(go.Scatter3d(
                x = [0,components[i][0]],
                y = [0,components[i][1]],
                z = [0,components[i][2]],
                marker = dict(size = 1, color = "rgb(250,0,0)"),
                line = dict(width = 2),
                name = col,
                showlegend=False
            ))