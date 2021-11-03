import plotly.graph_objs as go
from plotly.subplots import make_subplots

def create_figure(n_components, df, components, color_graph, categories, explained_variance, method=None, pca=None):
    fig = fill_figure(n_components, df, components, explained_variance, color_graph, categories=categories, method=method)
    if method == 'pca':
        draw_arrows(fig, n_components, df, pca.components_.T, categories)
    return fig

def create_mca_figure(n_components, df, components, categories, explained_inertia):
    return fill_figure(n_components, df, components, None, True, categories=categories, method='mca')
     

def create_figure_tSNE(n_components, df, components, color_graph, categories, divergence):
    fig = fill_figure(n_components, df, components, None, color_graph, categories=categories, method='tSNE')
    fig.update_layout(title=f'Divergence: {divergence:.2f}')
    return fig

def create_mds_figure(n_components, df, components, color_graph, categories, stress):
    fig = fill_figure(n_components, df, components, None, color_graph, categories=categories, method='mds')
    fig.update_layout(title=f'Stress: {stress:.2f}')
    return fig

def fill_figure(n_components, df, data, metrics, color_graph, categories=None, method=None):
    fig = go.Figure()
    axis = get_axis_string(method)
    if n_components == 2:
        for category in df[categories].unique():
            indexes = df.index[df[categories] == category].tolist()
            fig.add_trace(go.Scatter(
                    x=[data[i][0] for i in indexes],
                    y=[data[i][1] for i in indexes],
                    mode='markers',
                    name=str(category),
                    hovertemplate=get_hovertemplate(n_components, indexes, string), text=[str(i) for i in indexes]
        ))
        if metrics is not None:
            fig.update_xaxes(
                title_text = f'{axis} 1 ({metrics[0]*100:.1f}%)'
            )
            fig.update_yaxes(
                title_text = f'{axis} 2 ({metrics[1]*100:.1f}%)'
            )


    elif n_components == 3:
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
        if metrics is not None:
            fig.update_layout(scene = dict(
                xaxis_title=f'{axis} 1 ({metrics[0]*100:.1f}%)',
                yaxis_title=f'{axis} 2 ({metrics[1]*100:.1f}%)',
                zaxis_title=f'{axis} 3 ({metrics[2]*100:.1f}%)',
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

def get_axis_string(method):
    if method == 'pca' or method == 'kpca':
        return 'PC'  
    elif method == 'lda':
        return 'LD' 
    elif method == 'mca':
        return 'Component' 
    else:
        return 'Dimension'

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