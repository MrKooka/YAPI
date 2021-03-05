from .main import apply_layout_with_auth
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import sys
from pprint import pprint
from api import Api

import dash_bootstrap_components as dbc

url_base = '/dash/app1/'


layout = html.Div([
    dcc.Input(id='pattern', type='text'),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    html.Div(id='output-state')
])

def Add_Dash(server):
    app = dash.Dash(server=server, url_base_pathname=url_base)
    apply_layout_with_auth(app, layout)

    @app.callback(Output('output-state', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('pattern', 'value'))
    def update_output(n_clicks,input1):
        return u'''{} - {}'''.format(n_clicks,input1)

    
    return app.server

# layout = html.Div([
    
#     html.Div('URL'),
#     dcc.Input(id='url'), html.Br(), html.Br(),
#     html.Div('Количество комментариев'),
#     dcc.Input(id='count'), html.Br(), html.Br(),
#     html.Button(id='my-button', n_clicks=0, children="Show breakdown"),
#     html.Div('Фильтр'),
#     dcc.Input(id = 'input_text'), html.Br(), html.Br(),
#     dbc.Alert("This is a primary alert", color="primary",id='target'),
# ])

# def Add_Dash(server):
#     app = dash.Dash(server=server, url_base_pathname=url_base,external_stylesheets=[dbc.themes.BOOTSTRAP])
#     apply_layout_with_auth(app, layout)

#     # @app.callback(
#     #         Output('target', 'children'),
#     #         [Input('input_text', 'value')])
#     # def callback_filter(value):
#     #     return 'your input is {}'.format(value)
        
#     @app.callback(
#         Output('target','children'),
#         Input('my-button','n_clicks'),
#         State('count','count'),     
#         State('url','url'),
# )
#     def callback_get_comments(n):
#         api = Api(url,count)
#         print(n)
#     return app.server