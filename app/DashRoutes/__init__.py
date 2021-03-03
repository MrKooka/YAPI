from flask import Blueprint

dash = Blueprint(
    'dash',
    __name__,
    url_prefix='/DashExample',
    template_folder='templates',
    static_folder='static'
)
