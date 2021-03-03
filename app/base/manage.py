import sys,os,inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from app import App
from models import *
from .imports import app

if __name__ == '__main__':
	app.migrate().run()