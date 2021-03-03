from flask import Blueprint

setting = Blueprint(
    'setting',
    __name__,
    url_prefix='/setting',
    template_folder='templates',
    static_folder='static'
)