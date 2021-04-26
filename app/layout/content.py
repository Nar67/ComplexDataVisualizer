import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from layout.upload import upload

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "16rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

BUTTON = {
    "position": "relative",
    "top": 0,
    "right": "0rem",
    "bottom": 0,
    "width": "2rem",
    "height": "2rem",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
}


content = html.Div([
    dbc.Button("-", color="dark", id="btn_sidebar", className="mr-2", style=BUTTON),
    html.Div(id="page-content"),
    upload,
],
id="content",
style=CONTENT_STYLE)