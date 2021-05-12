from dash.dependencies import Input, Output, State
from maindash import app

from layout.sidebar.sidebar_styles import SIDEBAR_HIDEN, SIDEBAR_STYLE
from layout.content.content_styles import CONTENT_STYLE, CONTENT_STYLE1


@app.callback(
    Output("sidebar", "style"),
    Output("content", "style"),
    Output("side_click", "data"),
    Input("btn_sidebar", "n_clicks"),
    State("side_click", "data")
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

