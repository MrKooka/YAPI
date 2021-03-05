from googleapiclient.discovery import build
import json,io,codecs
from pprint import pprint 
import re
import pandas as pd
import plotly.express as px
token = 'AIzaSyDl__LeDHysLbzRCOfT6S5ephdIzgFA8Iw'

next_page_token='QURTSl9pMWlEa1hfaXp3em1rM2xoSERFa2NWTXVWS1l1LVJ4V1JhTWJjV2VxVDNKLWpIbE9XRDFQelkwWDJRc0dMRGI5ZHdwVXdSZlBKVkVIWVBST1FzS0dOX3VNSE5UQ3NydWc0X2xJRG1qRF9hanBOODlGNUZnM0pGYzE2RlBZaVRvMlVOR0RLam9DSXZ2VGhFV090N1drSEVpVzNJTVE3cFZWOVhaUTRKVFhUTGdEV2N5SjgxV1ZUekxUSjZwNjhYMjJvME1CaTdzR2xKM2FoOVgxLTBQSmpRRWNJSWx3MzFVMnotb3UyUUZRNXkzQXk3Tkh0WkFLSHgxSmhaNHJLdWpJYlpXRUZYd2Z3Y1BYZ0NfLUdDZ0dhNXlQbUpVQklObklPUTkxTmsyTTlUSlpSUjhYdktqa0ludk12bElBcDA='


class SaveComments:
	def __get__(self,instance, owner):
		return self.__value

	def __set__(self, instance, value):
		self.__value = value

	def __delete__(self,obg):
		del self.__value

class Api:
	comments = SaveComments()
	
	def __init__(self,url=None,n=None):
		self.videoId = re.findall(r'\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})',url)[0][-1]
		self.token = token
		self.n = n 
		self.comments = None
	
	def get_data(self,videoId,n):
		print('Начала работать get_data')
		youtube = build('youtube','v3', developerKey=token)
		results = youtube.commentThreads().list(
												pageToken = 'QURTSl9pMlJ6TUNuSkl4Qzg0QmJ1QlFmaVg3eENISGhoUmFKZjNQVFVjaFBDeHZDYmFLVWVoenYtcS1GWTNBTTd0RWhGS0c0MkpJNTV5cXVlUlpyTGhpT1ZwaHVRc3pzSmhQLTAwWWEzZmg0M3NCX1h3SUx3c09CMHBnWEdkeHVNV2pWcktBdHllNXE1aUdjY3J6OFU2TGlqcGIwYlIzaTFWQzN2bFJEemFYYVZCT3pBRGhqd2JtX3hNX3RoT28wUnN6VFFVNlFzS0YxN3FHRHB6aEJXNXZzbHkwVlhFb3ZrMUJqMlA4SDlWdERXLWxYcFloRVhTMTRJellxTnJjOU9JTWFEc21yVVVSeVNXc094UFlpaVNZVjNmMXNkNEdPVEZrbDFGSjItYkZXYTU5NjRKUUZ4b1Baa0F2QmRMd2NXbkMxazI5X0R3',
												part="snippet,replies",
												videoId=self.videoId,
												order='relevance',
												maxResults = self.n
												).execute()
		print()
		print('get_data отработала')
		return results

	def parse_data(self):
		print('начала работать parse_data')
		comment = []
		# if self.videoId in self._url_cache:
		# 	print('Сработало кеширование')
		# 	text = self._url_cache[videoId]
		# else:
		text = self.get_data(self.videoId,self.n)
		for item in text['items']:
			# print(item['snippet']['topLevelComment']['snippet']['textDisplay'])
			text = item['snippet']['topLevelComment' ]['snippet']['textDisplay']
			userName = item['snippet']['topLevelComment' ]['snippet']['authorDisplayName']
			authorChannelUrl =  item['snippet']['topLevelComment' ]['snippet']['authorChannelUrl']
			authorChannelId = item['snippet']['topLevelComment' ]['snippet']['authorChannelId']['value']
			likeCount = item['snippet']['topLevelComment' ]['snippet']['likeCount']
			datePublish =  item['snippet']['topLevelComment' ]['snippet']['publishedAt']
			authorProfileImageUrl = item['snippet']['topLevelComment' ]['snippet']['authorProfileImageUrl']
			comment.append({
				'text':text,
				'userName':userName,
				'authorChannelId':authorChannelId,
				'authorChannelUrl':authorChannelUrl,
				'datePublish':datePublish,
				'likeCount':likeCount,
				'authorProfileImageUrl':authorProfileImageUrl
				})
		print('parse_data отработала')
		return comment
		# s = ''
		# # results = self.data.get_data(self.videoId,self.n)[0]
		# results = self.data.get_data(self.videoId,self.n)
		# for i in range(1,self.n):
		# 	text = results['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay']
		# 	s = s+text

		# result  = re.findall(r"РЕЯ|[аА]тлас|[гГ]иперион|[дД]иона|[Ее]лена|[мМ]имас|[пП]андор[ау]|[рР]ея|[тТ]елесто|[Тт]ефия|[яЯ]пе[дт]",s)

		# result = list(map(str.lower,result))
		# wordfreq = {}
		# for word in result:
		# 	if word not in wordfreq:
		# 		wordfreq[word] = 0
			# wordfreq[word] += 1
		return wordfreq,s

	def get_df(self):
		print('Начала работать get_df')
		wordfreq = self.parse_data()[0]
		dfl = []
		for k in wordfreq:
			dfl.append( (k,wordfreq[k]) )

		df = pd.DataFrame(dfl)

		print('get_df отработала')
		return df
		# return self.make_graf(df)

	def get_all_comments(self):
		print('Начала работать get_text')
		self.comments = self.parse_data()
		print('get_text отработала')
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
	
	api = Api('https://www.youtube.com/watch?v=zwel95I7O88&list=PLA0M1Bcd0w8zo9ND-7yEFjoHBg_fzaQ-B&index=4&t=821s',50)
	print(len(api.get_all_comments()))
		# for comment in api.get_comment():	
			# print(comment['userName'])
				# print(name['userName'])
if __name__ == '__main__':
	main()