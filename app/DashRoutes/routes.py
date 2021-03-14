import sys,os,inspect
from pprint import pprint
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
from . import dash
from flask import render_template,request,send_file,send_from_directory,current_app
from flask_login import login_required
from Dashboards import DashApp1
from Dashboards.DashApp1 import Layout
from api import Api,Graph
import pandas as pd
import plotly.express as px
from .forms import Search_form
import csv
import json
@dash.route('/app1',methods = ['POST','GET'])
def app1_template():
	form = Search_form()

	q = request.args.get('q') # q variable contains a search pattert  

	if form.validate_on_submit():
		print('Сработала app1_template POST')
		url = form.url.data
		n = form.maxResults.data
		print(url,n)
		if 'replice' in request.form:
			print('replise in request.form')
			replice = request.form['replice']
			api = Api(url,n,replice)
			comments = api.get_all_comments()
			total = len(comments)
			return render_template('app1.html', dash_url = DashApp1.url_base,comments=comments,total=total,form=form)

		api = Api(url,n)
		comments = api.get_all_comments()
		total = len(comments)

		return render_template('app1.html', dash_url = DashApp1.url_base,comments=comments,total=total,form=form)

	q_comments = []

	if q and hasattr(Api,'comments') and Api.comments != None:
		comments = Api.comments
		for i in comments:
			if q in i['textDisplay']:
				q_comments.append(i)
		total = len(q_comments)

		return render_template('app1.html', dash_url = DashApp1.url_base,comments=q_comments,total=total,form=form)
	
	else: 
		if hasattr(Api,'comments') and Api.comments != None:
			print('Сработало else hasattr(Api,"comments"')
			comments = Api.comments
			total = len(comments)
			return render_template('app1.html', dash_url = DashApp1.url_base,comments=comments,total=total,form=form)

	return render_template('app1.html', dash_url = DashApp1.url_base,form=form)



@dash.route('/app1<p>')
def select_type_request(p):
	form = Search_form()

	text = '''Ведите слючевые слова через запятую. Дальше на основе частоты встречаимости выведится график'''
	if p == 'search_by_word':
		if hasattr(Api,'comments') and Api.comments != None:
			comments = Api.comments
			return render_template('app1.html', dash_url = DashApp1.url_base,form=form,comments=comments)

		return render_template('app1.html', dash_url = DashApp1.url_base,form=form)


	if p == 'graph':
		
		if hasattr(Api,'comments') and Api.comments != None:
			
			comments = Api.comments
			
			return render_template('app1.html',dash_url = DashApp1.url_base,
									text=text,comments=comments,type_input='graph',form=form)


		return render_template('app1.html',dash_url = DashApp1.url_base,
									text=text,type_input='graph',form=form)
	if p == 'csv':
		return render_template('app1.html',dash_url = DashApp1.url_base,
									text=text,type_input='csv',form=form)
	return render_template('app1.html',dash_url = DashApp1.url_base,form=form)

@dash.route('/dataCSV')
def download_csv():
	form = Search_form()
	if hasattr(Api,'comments') and Api.comments != None:
		fieldnames = ['authorChannelId','authorChannelUrl','authorDisplayName','authorProfileImageUrl',
					  'canRate','likeCount','textDisplay','textOriginal','updatedAt','publishedAt','totalReplyCount']
		comments = Api.comments
		uploads = os.path.join(current_app.root_path, '/media/alex/Data1/two/YAPI3/app/DashRoutes/csv_files')
		with open('/media/alex/Data1/two/YAPI3/app/DashRoutes/csv_files/data.csv','w',newline='') as f:
			writer = csv.DictWriter(f, fieldnames=fieldnames)
			writer.writeheader()
			for i in comments:
				writer.writerow(i)
		return send_from_directory(directory=uploads,filename='data.csv',as_attachment=True)
	alert = 'Загрузите комментарии'
	return render_template('app1.html',dash_url = DashApp1.url_base,
									alert = alert,type_input='csv',form=form)

@dash.route('/dataJSON')
def download_json():
	form = Search_form()
	uploads = os.path.join(current_app.root_path, '/media/alex/Data1/two/YAPI3/app/DashRoutes/csv_files')

	if hasattr(Api,'comments') and Api.comments != None:
		comments = Api.comments
		data = {'items':comments}
		with open('/media/alex/Data1/two/YAPI3/app/DashRoutes/csv_files/data.json','w') as f:
			json.dump(data, f, ensure_ascii=False, indent=4)
		return send_from_directory(directory=uploads,filename='data.json',as_attachment=True)

	alert = 'Загрузите комментарии'
	return render_template('app1.html',dash_url = DashApp1.url_base,
									alert = alert,type_input='csv',form=form)


@dash.route('/app1r')
def reset_comments():
	form = Search_form()
	Api.reset_comments()
	return render_template('app1.html', dash_url = DashApp1.url_base,form=form)



@dash.route('/app2/<type>')
def app2_template():
	form = Search_form()
	return render_template('app2.html', dash_url = Dash_App2.url_base,form=form)

