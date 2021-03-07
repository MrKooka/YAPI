from googleapiclient.discovery import build
import json,io,codecs
from pprint import pprint 
import re
import pandas as pd
import plotly.express as px
token = 'AIzaSyDl__LeDHysLbzRCOfT6S5ephdIzgFA8Iw'

class SaveComments:
	def __get__(self,instance, owner):
		return self.__value

	def __set__(self, instance, value):
		self.__value = value

	def __delete__(self,obg):
		del self.__value


class Api:
	comments = SaveComments()

	def __init__(self,url,maxResults,replice=None):
		self.videoId = re.findall(r'\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})',url)[0][-1]
		self.token = token
		self.maxResults = maxResults 
		self.comments = None
		self.replice = replice

	def get_data(self,maxResults,videoId=None,parentId=None,pageToken=None):
		print('get_data started working')
		youtube = build('youtube','v3', developerKey=token)
		results = youtube.commentThreads().list(pageToken = pageToken,
												part="snippet",
												videoId=self.videoId,
												order='relevance',
												maxResults = self.maxResults,
												textFormat = 'plainText'
												).execute()
		print('get_data is done')
		return results

	def parse_data(self):
		print('parse_data started working')
		
		comments = []

		data = self.get_data(self.videoId,self.maxResults)
		for item in data["items"]:
			text = item['snippet']['topLevelComment' ]['snippet']['textDisplay']
			userName = item['snippet']['topLevelComment' ]['snippet']['authorDisplayName']
			authorChannelUrl =  item['snippet']['topLevelComment' ]['snippet']['authorChannelUrl']
			authorChannelId = item['snippet']['topLevelComment' ]['snippet']['authorChannelId']['value']
			likeCount = item['snippet']['topLevelComment' ]['snippet']['likeCount']
			datePublish =  item['snippet']['topLevelComment' ]['snippet']['publishedAt']
			authorProfileImageUrl = item['snippet']['topLevelComment' ]['snippet']['authorProfileImageUrl']

			comments.append({
				'text':text,
				'userName':userName,
				'authorChannelId':authorChannelId,
				'authorChannelUrl':authorChannelUrl,
				'datePublish':datePublish,
				'likeCount':likeCount,
				'authorProfileImageUrl':authorProfileImageUrl
				})

			
			# ckecking a replice checkbox 
			if self.replice:
				print('self.replice is True')
				self._scrape_answers(item,comments)

			# maxResults control 
			if len(comments) >= int(self.maxResults):
				return comments

		while ("nextPageToken" in data):
			print('Start of new while'+'-'*50)
			data = self.get_data(videoId=self.videoId, maxResults=100, pageToken=data['nextPageToken'])

			for item in data["items"]:
				text = item['snippet']['topLevelComment' ]['snippet']['textDisplay']
				userName = item['snippet']['topLevelComment' ]['snippet']['authorDisplayName']
				authorChannelUrl =  item['snippet']['topLevelComment' ]['snippet']['authorChannelUrl']
				authorChannelId = item['snippet']['topLevelComment' ]['snippet']['authorChannelId']['value']
				likeCount = item['snippet']['topLevelComment' ]['snippet']['likeCount']
				datePublish =  item['snippet']['topLevelComment' ]['snippet']['publishedAt']
				authorProfileImageUrl = item['snippet']['topLevelComment' ]['snippet']['authorProfileImageUrl']
				comments.append({
					'text':text,
					'userName':userName,
					'authorChannelId':authorChannelId,
					'authorChannelUrl':authorChannelUrl,
					'datePublish':datePublish,
					'likeCount':likeCount,
					'authorProfileImageUrl':authorProfileImageUrl
					})
				if len(comments) >= int(self.maxResults):
					return comments

				if self.replice:
					self._scrape_answers(item,comments)
		print('parse_data is done')
		return comments

	def _scrape_answers(self,item,comments):

		totalReplyCount = item["snippet"]['totalReplyCount']
		if totalReplyCount > 0:
			print('Scraping answers of comments ')

			parent = item["snippet"]['topLevelComment']["id"]

			data2 = build('youtube','v3', developerKey=token).comments().list(part='snippet',
			 maxResults='100', parentId=parent,textFormat="plainText").execute()
			for item in data2["items"]:
				text = item['snippet']['textDisplay']
				userName = item['snippet']['authorDisplayName']
				authorChannelUrl =  item['snippet']['authorChannelUrl']
				authorChannelId = item['snippet']['authorChannelId']['value']
				likeCount = item['snippet']['likeCount']
				datePublish =  item['snippet']['publishedAt']
				authorProfileImageUrl = item['snippet']['authorProfileImageUrl']
				comments.append({
            		'text':text,
                	'userName':userName,
                	'authorChannelId':authorChannelId,
                	'authorChannelUrl':authorChannelUrl,
                	'datePublish':datePublish,
                	'likeCount':likeCount,
                	'authorProfileImageUrl':authorProfileImageUrl
				})
				if len(comments) >= int(self.maxResults):
					return comments
		return comments

	def get_df(self):
		print('get_df started working')
		wordfreq = self.parse_data()[0]
		dfl = []
		for k in wordfreq:
			dfl.append( (k,wordfreq[k]) )

		df = pd.DataFrame(dfl)

		print('get_df is done')
		return df
		# return self.make_graf(df)

	def get_all_comments(self):
		print('get_text started working')
		self.comments = self.parse_data() #parse_data() return a list of comment date  
		print('get_text is done')
		return self.comments

	# def filter_comment(self,comments,pattern=None):
		# print(comments)


	# def make_graf(self,df):
	# 	return px.bar(df,x=0,y=1)
	# def write_json(self,df):
	# 	result = df.to_json(orient='split')
	# 	parsed = json.loads(result)
		# print(json.dumps(parsed,indent=4))
		# with open('json.json','w') as file:
		# 	json.dump(parsed,file,  indent = 2,ensure_ascii=False)
def main():
	
	api = Api('https://www.youtube.com/watch?v=ypKzLl5YyXo',100)
	# data2 = api.get_data(maxResults=100,parentId='UgzvJkt5VjEQDNed2294AaABAg')
	# youtube = build('youtube','v3', developerKey=token)
	# data2  = youtube.comments().list(part='snippet', maxResults='100', parentId='UgzxCQMrWHtz0Y6109l4AaABAg',textFormat="plainText").execute()
	# print(data2)
	# print(data2)
	# for i in api.get_data('ypKzLl5YyXo',100)['items']:
		# print(i["snippet"]['topLevelComment']["id"])
	# print(nextPageToken in api.get_data('uA8bCNEuTZ0',100))
	data = api.get_all_comments() 
	p = 0
	for i in data:
		p += 1
		print(p,'==',i)
# def write_json(data):
		# result = df.to_json(orient='split')
		# parsed = json.loads(result)
		# print(json.dumps(parsed,indent=4))
		# with open('json.json','w') as file:
			# json.dump(data,file,  indent = 2,ensure_ascii=False)
		# print(p,'===',i)
if __name__ == '__main__':
	main()