from googleapiclient.discovery import build
import json,io,codecs
from pprint import pprint 
import re
import pandas as pd
import plotly.express as px
from collections import Counter
token = 'AIzaSyDl__LeDHysLbzRCOfT6S5ephdIzgFA8Iw'
youtube = build('youtube','v3', developerKey=token)
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
		self.__videoId = re.findall(r'\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})',url)[0][-1]
		self.token = token
		self.maxResults = maxResults 
		self.comments = None
		self.replice = replice
	def __check_videoId(self,maxResults,videoId):
		
			results  = youtube.commentThreads().list(pageToken = pageToken,
													part="snippet",
													videoId=self.__videoId,
													order='relevance',
													maxResults = self.maxResults,
													textFormat = 'plainText'
													).execute()

		return results
	def get_data(self,maxResults,videoId=None,parentId=None,pageToken=None):
		print('get_data started working')
		results = Api.__check_videoId(self.maxResults,videoId=self.__videoId,parentId=None,pageToken=None)
		print('get_data is done')
		return results


	# @property
	# def maxResults(self):
	# 	print('Сработал get maxResults')
	# 	return self.__maxResults
	
	# @maxResults.setter
	# def maxResults(self,maxResults):
	# 	print('сработал setter maxResults')
	# 	try:
	# 		int(maxResults)
	# 		self.__maxResults = maxResults
	# 	except:
	# 		raise TypeError
			

	def parse_data(self):
		print('parse_data started working')
		
		comments = []

		data = self.get_data(self.__videoId,self.maxResults)
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
			data = self.get_data(videoId=self.__videoId, maxResults=100, pageToken=data['nextPageToken'])

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


	def get_all_comments(self):
		print('get_text started working')
		self.comments = self.parse_data() #parse_data() return a list of comment date  
		print('get_text is done')
		return self.comments


	# def write_json(self,df):
	# 	result = df.to_json(orient='split')
	# 	parsed = json.loads(result)
		# print(json.dumps(parsed,indent=4))
		# with open('json.json','w') as file:
		 # 	json.dump(parsed,file,  indent = 2,ensure_ascii=False)



class Graph(Api):
	def __init__(self):
		self.pattern = None

	def _make_df(self,pattern):
		pattern = pattern.replace(',','|')
		text = ''
		for i in self.comments:
			text = text + i['text']

		result  = re.findall('{}'.format(pattern),text) # list of words found by pattern
		calculated_result = Counter(result).most_common() #[(word_1,1),(word_2,3)] - a list of the occurrence of each word
		df = pd.DataFrame(calculated_result)

		return df

	def make_graph(self,pattern):
		self.pattern = pattern
		df = self._make_df(pattern)
		fig = px.bar(df,x=0,y=1)

		return fig

def main():
	
	api = Api('https://www.youtube.com/watch?v=aSP97Pk6ojI',10)

	data = api.get_all_comments() 
	g = Graph()
	print(g._make_df())
# def write_json(data):
		# result = df.to_json(orient='split')
		# parsed = json.loads(result)
		# print(json.dumps(parsed,indent=4))
		# with open('json.json','w') as file:
			# json.dump(data,file,  indent = 2,ensure_ascii=False)
		# print(p,'===',i)
if __name__ == '__main__':
	main()