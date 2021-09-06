import plotly.graph_objs as go
from plotly.subplots import make_subplots

def create_figure(n_components, df, components, color_graph, categories, explained_variance, pca=None, fda=None, kpca=None):
    if pca == None and fda == None and kpca == None:
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
        if pca != None:
            for i, col in enumerate(df.drop(categories, axis=1).columns):
                fig.add_trace(go.Scatter(
                    x = [0,pca.components_.T[i][0]],
                    y = [0,pca.components_.T[i][1]],
                    marker = dict(size = 1, color = "rgb(250,0,0)"),
                    line = dict(width = 2),
                    name = col
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
        if pca != None:
            for i, col in enumerate(df.drop(categories, axis=1).columns):
                fig.add_trace(go.Scatter3d(
                    x = [0,pca.components_.T[i][0]],
                    y = [0,pca.components_.T[i][1]],
                    z = [0,pca.components_.T[i][2]],
                    marker = dict(size = 1, color = "rgb(250,0,0)"),
                    line = dict(width = 2),
                    name = col
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
    return fig

def create_mca_figure(n_components, df, components, explained_inertia):
    method_string = 'Component'
    fig = go.Figure()
    indexes = df.index.tolist()
    if n_components == 2:
        fig.add_trace(go.Scatter(
                x=components[:][0],
                y=components[:][1],
                mode='markers',
                #name=str(category),
                hovertemplate='<br><b>' + method_string + ' 1</b>: %{x}<br>' + 
                            '<br><b>' + method_string + ' 2</b>: %{y}<br>' + 
                            '<br><b>Index</b>: %{text}<br><extra></extra>', 
                            text=[str(i) for i in indexes],
        ))
    
        fig.update_xaxes(
            title_text = "{ax} 1 ({var:.1f}%)".format(ax=method_string, var=explained_inertia[0]*100)
        )
        fig.update_yaxes(
            title_text = "{ax} 2 ({var:.1f}%)".format(ax=method_string, var=explained_inertia[1]*100),
            scaleanchor = "x",
            scaleratio = 1,
        )
    elif n_components == 3:
        fig.add_trace(go.Scatter3d(
            x=components[:][0],
            y=components[:][1],
            z=components[:][2],
            mode='markers',
            #name=str(category),
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
            xaxis_title="{ax} 1 ({var:.1f}%)".format(ax=method_string, var=explained_inertia[0]*100),
            yaxis_title="{ax} 2 ({var:.1f}%)".format(ax=method_string, var=explained_inertia[1]*100),
            zaxis_title="{ax} 3 ({var:.1f}%)".format(ax=method_string, var=explained_inertia[2]*100),
        ))
        #uses 'data' which preserves the proportion of axes ranges unless one axis is 4 times the others, then 'cube' is used
        fig.update_scenes(aspectmode='auto') 
    return fig

def create_figure_tSNE(n_components, df, components, color_graph, categories, divergence):
    method_string = 'Dimension '
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
    

        fig.update_traces(marker_size=4)
        #uses 'data' which preserves the proportion of axes ranges unless one axis is 4 times the others, then 'cube' is used
        fig.update_scenes(aspectmode='auto')  

    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
    )
    fig.update_layout(title='Divergence: {div}'.format(div=divergence))
    return fig

def create_mds_figure(n_components, df, components, categories, stress):
    method_string = 'Dimension '
    fig = go.Figure()
    indexes = df.index.tolist()
    if n_components == 2:
        for category in df[categories].unique():
            indexes = df.index[df[categories] == category].tolist()
            fig.add_trace(go.Scatter(
                    x=[components[i][0] for i in indexes],
                    y=[components[i][1] for i in indexes],
                    mode='markers',
                    name=str(category),
                    hovertemplate='<br><b>X</b>: %{x}<br>' + 
                                '<br><b>Y</b>: %{y}<br>' + 
                                '<br><b>Index</b>: %{text}<br><extra></extra>', 
                                text=[str(i) for i in indexes],
            ))
        fig.update_yaxes(
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
                    hovertemplate='<br><b>X</b>: %{x}<br>' + 
                                '<br><b>Y</b>: %{y}<br>' + 
                                '<br><b>Z</b>: %{z}<br>' + 
                                '<br><b>Index</b>: %{text}<br><extra></extra>', 
                                text=[str(i) for i in indexes],
            ))
        fig.update_yaxes(
            scaleanchor = "x",
            scaleratio = 1,
        )

        fig.update_traces(marker_size=4)
        #uses 'data' which preserves the proportion of axes ranges unless one axis is 4 times the others, then 'cube' is used
        fig.update_scenes(aspectmode='auto')
    fig.update_layout(title='Stress: {st}'.format(st=stress))

    return fig