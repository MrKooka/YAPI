import sys,os,inspect
from pprint import pprint
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
from . import dash
from flask import render_template,request
from flask_login import login_required
from Dashboards import DashApp1
from api import Api

@dash.route('/app1',methods = ['POST','GET'])
def app1_template():
	print('Сработала app1_template ')

	q = request.args.get('q') # q variable contains a search pattert  

	if request.method == 'POST':
		print('Сработала app1_template POST')
		url = request.form['url']
		n = request.form['n']
		if 'replice' in request.form:
			print('replise in request.form')
			replice = request.form['replice']
			# print(replice)
			api = Api(url,n,replice)
			comments = api.get_all_comments()
			total = len(comments)
			return render_template('app1.html', dash_url = DashApp1.url_base,comments=comments,total=total)
				
		api = Api(url,n)
		comments = api.get_all_comments()
		total = len(comments)

		return render_template('app1.html', dash_url = DashApp1.url_base,comments=comments,total=total)

	q_comments = []

	if q:

		comments = Api.comments

		for i in comments:
			if q in i['text']:
				q_comments.append(i)
		total = len(q_comments)

		return render_template('app1.html', dash_url = DashApp1.url_base,comments=q_comments,total=total)
	
	else: 
		if hasattr(Api,'comments'):
			comments = Api.comments
			total = len(comments)
			return render_template('app1.html', dash_url = DashApp1.url_base,comments=comments,total=total)
		else:
			pass 
	return render_template('app1.html', dash_url = DashApp1.url_base)


		
@dash.route('/app2')
def reset_comments():
	if hasattr(Api,'comments'):
		Api.comments = None
	return render_template('app1.html', dash_url = DashApp1.url_base)



@dash.route('/app2')
# @login_required
def app2_template():
    return render_template('app2.html', dash_url = Dash_App2.url_base)

