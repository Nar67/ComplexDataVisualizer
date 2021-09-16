 
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


from layout.sidebar.sidebar import sidebar
from layout.content.content import content


navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("Upload", color="primary", id="upload_btn")
#        dbc.DropdownMenu(
#            children=[
#                dbc.DropdownMenuItem("More pages", header=True),
#                dbc.DropdownMenuItem("Page 2", href="#"),
#                dbc.DropdownMenuItem("Page 3", href="#"),
#            ],
#            nav=True,
#            in_navbar=True,
#            label="More",
#        ),
    ],
    id="navBar",
    brand="Complex Data Visualizer",
    brand_href="/",
    color="dark",
    dark=True,
    fluid=True,
)

layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
    ],
)