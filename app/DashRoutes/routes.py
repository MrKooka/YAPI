import sys,os,inspect
from pprint import pprint
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
from . import dash
from flask import render_template
from flask_login import login_required
from Dashboards import DashApp1
@dash.route('/app1')
# @login_required
def app1_template():
    return render_template('app1.html', dash_url = DashApp1.url_base)

@dash.route('/app2')
# @login_required
def app2_template():
    return render_template('app2.html', dash_url = Dash_App2.url_base)