from dash.dependencies import Input, Output, State
from app import app

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from layout.visualization.visualization import visualization
from layout.data_table.data_table import data_table



@app.callback(
    Output("page-content", "children"), 
    Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([html.P("This is the content of Home!")])
    elif pathname == "/table":
        return data_table
    elif pathname == "/visualization":
        return visualization
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
