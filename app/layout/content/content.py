import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from layout.content.content_styles import CONTENT_STYLE, BUTTON


content = html.Div([
    dbc.Button("-", color="dark", id="btn_sidebar", style=BUTTON),
    dcc.Store("data", storage_type='session'),
    dcc.Store("dataset-info", storage_type='session'),
    html.Div(id="page-content"),
],
id="content",
style=CONTENT_STYLE)