import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


upload_view = html.Div([
    dcc.Store("predata"),
    html.Div(id='upload-comp', hidden=False, children=[
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },)
        ]),
    html.Div(id='upload-info')
    ])



def upload_info(df):
    return [html.P("Select according to the uploaded dataset"),
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
                html.P("Write all categorical columns in the same format as in the text placeholder (from 1 to {}):".format(df.shape[1])),
                dcc.Input(id='categorical_column_input', placeholder='Ex: \'5-10,12-14,17,20-25\'', pattern='(\d+(-\d+)|\d+)(,(\d+(-\d+)|\d+))*'),
                html.P("Choose an option for variables of different type (categorical and numerical):", style={'margin-top': '12px'}),
                dcc.RadioItems(
                    id='convert-vars',
                    options=[
                        {'label': ' Ignore (Only one type will be visualized at a time)', 'value': 'ignore'},
                        {'label': ' Convert all to numerical', 'value': 'conv_numerical'},
                        {'label': ' Convert all to categorical', 'value': 'conv_categorical'}
                    ],
                    value="ignore",
                    labelStyle={'margin-right': '12px', 'margin-top': '12px', 'margin-bottom': '12px', 'display': 'block'}
                    ),
            ]),

            dcc.RadioItems(
                id='dataset-labeled',
                options=[
                    {'label': ' Labeled', 'value': 'labeled'},
                    {'label': ' Unlabeled', 'value': 'unlabeled'}
                ],
                value="unlabeled",
                labelStyle={'margin-right': '12px', 'margin-top': '12px', 'margin-bottom': '12px'}
                ),
            html.Div(id='label-column-dropdown', hidden=True, children=[
                html.P("Choose labels column"),
                dcc.Dropdown(
                    id='feature-column',
                    options=[{'label': i, 'value': i} for i in df.columns],
                    value=df.columns[-1]
                )
            ], style={'margin-bottom': '16px'}),
            
            html.Div(hidden=df.isnull().sum().sum() < 1, children=[
                html.P("Dataset contains {} missing values. Choose an option for treating the missing values".format(df.isnull().sum().sum())),
                dcc.RadioItems(
                    id='missing-values',
                    options=[
                        {'label': ' Delete', 'value': 'delete'},
                        {'label': ' Impute', 'value': 'impute'}
                    ],
                    value="delete",
                    labelStyle={'margin-right': '12px', 'margin-top': '12px', 'margin-bottom': '12px'}
                    )
                ]),
            dbc.Button("Save", color="primary", id="confirm_upload_btn")
    ]