import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from layout.upload.upload import upload

from layout.content.content_styles import CONTENT_STYLE, BUTTON


content = html.Div([
    dbc.Button("-", color="dark", id="btn_sidebar", style=BUTTON),
    html.Div(id="page-content"),
],
id="content",
style=CONTENT_STYLE)