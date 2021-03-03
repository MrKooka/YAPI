from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from pprint import pprint
from .forms import LoginForm,CreateAccountForm
from . import base
from .models import User

@base.route('/')
def index():
	return render_template('index.html')
