from flask import Blueprint

home = Blueprint(
    'home',
    __name__,
    url_prefix='/home',
    template_folder='templates',
    static_folder='static'
)