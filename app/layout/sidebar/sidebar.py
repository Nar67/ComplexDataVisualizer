import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from layout.sidebar.sidebar_styles import SIDEBAR_STYLE

sidebar = html.Div(
    [
        html.H2("Menu"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", id="home-link", active="exact"),
                dbc.NavLink("Table View", href="/table", id="table-link", active="exact"),
                dbc.NavLink("Visualization", href="/visualization", id="visualization-link", active="exact"),
                dbc.NavLink("PCA", href="/pca", id="pca-link", active="exact"),
                dbc.NavLink("FDA", href="/fda", id="fda-link", active="exact"),
                dbc.NavLink("MCA", href="/mca", id="mca-link", active="exact"),
                dbc.NavLink("t-SNE", href="/tSNE", id="tSNE-link", active="exact"),
                dbc.NavLink("K-PCA", href="/KPCA", id="KPCA-link", active="exact"),
                dbc.NavLink("MDS", href="/mds", id="mds-link", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)
