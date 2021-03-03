from .main import apply_layout_with_auth
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

url_base = '/dash/app1/'

layout = html.Div([
    html.Div('This is dash app1'), html.Br(),
    dcc.Input(id = 'input_text'), html.Br(), html.Br(),
    html.Div(id = 'target')
])

def Add_Dash(server):
    app = dash.Dash(server=server, url_base_pathname=url_base)
    apply_layout_with_auth(app, layout)

    @app.callback(
            Output('target', 'children'),
            [Input('input_text', 'value')])
    def callback_fun(value):
        return 'your input is {}'.format(value)
    
    return app.server