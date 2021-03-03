from pprint import pprint
import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, current_dir) 
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from Dashboards import DashApp1
class Config:
	SECRET_KEY = 'key'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1@localhost:27017/gshop'
	SQLALCHEMY_TRACK_MODIFICATIONS = True

class App:
	def __init__(self):
		self.app = app = Flask(__name__, static_folder='base/static',template_folder = 'base/templates')
		self.app.config.from_object(Config)
		self.db = db = SQLAlchemy(self.app)

	def register_blueprints(self):
		from setting.routes  import setting
		from home.routes import home
		from base.routes import base 
		from DashRoutes.routes import dash
		self.app.register_blueprint(home,url_prefix='/home')
		self.app.register_blueprint(base,url_prefix='')
		self.app.register_blueprint(setting,url_prefix='/setting')
		self.app.register_blueprint(dash,url_prefix='/DashExample')
		app = DashApp1.Add_Dash(self.app)

	def login_manager(self):
		login_manager = LoginManager()
		login_manager.init_app(self.app)
		login_manager.login_viwe = 'login'
		return login_manager

	def migrate(self):
		migrate = Migrate(self.app,self.db)
		manager = Manager(self.app)
		manager.add_command('db',MigrateCommand)
		return manager
		
	def get_app(self):
		return self.app

	def get_db(self):
		return self.db

