from . import setting
from flask import render_template, current_app, request, redirect,url_for
from flask_login import login_required, current_user
from .forms import RgisterForm, ChangePasswordForm
from base.models import User,db
from werkzeug.security import generate_password_hash, check_password_hash


@setting.route('/',methods = ['POST','GET'])
def rgister():
	form = RgisterForm()
	if request.method == 'POST':
		user = User.query.filter_by(username = form.username.data).first()
		email = User.query.filter_by(email = form.email.data).first()
		if user:
	 		status = 'Такой пользователь существует'
		if email:
			status = 'Этот email уже испальзуется'
		else:
			hashed_pass = generate_password_hash(form.password.data,method='sha256')
			new_user = User(email=form.email.data,
							username = form.username.data,
							password = hashed_pass)
			db.session.add(new_user)
			db.session.commit()
			return redirect(url_for('home.index'))
	return render_template('login.html',form=form,status='')

