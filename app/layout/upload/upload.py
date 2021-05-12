import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


from layout.upload.upload_styles import UPLOAD_STYLE

upload = html.Div([
    dcc.Upload(
        id='upload-data',
        children=[dbc.Button("Upload", color="primary", id="upload_btn")],
        # Allow multiple files to be uploaded
        multiple=True
    )])


