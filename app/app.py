from pprint import pprint
import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, current_dir) 
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from Dashboards.DashApp1 import Dash_app
# from Dashboards import DashApp1
class Config:
	SECRET_KEY = 'key'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1@localhost:27017/gshop'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	UPLOAD_FOLDER = '/media/alex/Data1/two/YAPI3/app/DashRoutes/csv_files'
	SEND_FILE_MAX_AGE_DEFAULT = 0

class App:
	def __init__(self):
		self.app = Flask(__name__, static_folder='base/static',template_folder = 'base/templates')
		self.app.config.from_object(Config)

	def register_blueprints(self):
		from setting.routes  import setting
		from home.routes import home
		from base.routes import base 
		from DashRoutes.routes import dash
		self.app.register_blueprint(home,url_prefix='/home')
		self.app.register_blueprint(base,url_prefix='')
		self.app.register_blueprint(setting,url_prefix='/setting')
		self.app.register_blueprint(dash,url_prefix='/DashExample')
		Dash_app(self.app).get_dash_app()
		# DashApp1.Add_Dash(self.app)

	def get_app(self):
		return self.app

	def get_db(self):
		return self.db

