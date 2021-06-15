import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from layout.layout import layout
from maindash import app
from layout.sidebar.sidebar_callbacks import *
from layout.upload.upload_callbacks import *
from layout.content.content_callbacks import *
from layout.visualization.visualization_callbacks import *
from layout.data_table.data_table_callbacks import *
from layout.pca.pca_callbacks import *

app.layout = layout

if __name__ == '__main__':
  app.run_server(host='0.0.0.0', port=8888, debug=True)