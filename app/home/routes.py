from . import home
from flask import render_template
from flask_login import login_required, current_user


@home.route('/')
@login_required
def index():
    return render_template('index.html')