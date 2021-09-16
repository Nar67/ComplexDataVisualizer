import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


upload_view = html.Div([
    dcc.Store("dataset-type", storage_type='session'),
    dcc.Store("dataset-column-text", storage_type='session'),
    html.P("Select according to the uploaded dataset"),
        dcc.RadioItems(
                id='dataset-kind',
                options=[
                    {'label': ' All numerical', 'value': 'numerical'},
                    {'label': ' All categorical', 'value': 'categorical'},
                    {'label': ' Mixed', 'value': 'mixed'},
                ],
                value="numerical",
                labelStyle={'margin-right': '12px'}
            ),
        html.Div(id='categorical_input', hidden=True, children=[
            html.P("Write all categorical columns in the same format as in the text placeholder (index starts at 0)"),
            dcc.Input(id='categorical_column_input', placeholder='Ex: \'5-10, 12-14, 17, 20-25\'')
        ]),
        dcc.Upload(
            id='upload-data',
            children=[dbc.Button("Upload", color="primary", id="confirm_upload_btn")],
            style={'margin-top': '12px'})
    ])


