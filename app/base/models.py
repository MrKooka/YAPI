from bcrypt import gensalt,hashpw,checkpw
from flask_login import UserMixin
from pprint import pprint
from .imports import app,login_manager
db = app.get_db()

class User(db.Model,UserMixin):
	id = db.Column(db.Integer(),primary_key=True)
	username = db.Column(db.String(225),unique=True)
	email = db.Column(db.String(225),unique=True)
	password = db.Column(db.String(225))

	def __repr__(self):
		return str(self.username)
	@staticmethod
	def get_db():
		db.session.commit()
		
@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None