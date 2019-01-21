import praw
import sqlite3 as sql
from datetime import datetime
import configparser

config = configparser.RawConfigParser()
config.read("settings.ini")

class Config:
    database_location = config['settings']['DATABASE_LOCATION']
    table_name = config['settings']['TABLE_NAME']
    reddit_secret_id = config['settings']['REDDIT_SECRET_ID']
    yid = config['settings']['YID']
    username = config['settings']['USERNAME']
    password = config['settings']['PASSWORD']
    bot_token = config['settings']['BOT_TOKEN']
    channel_id = config['settings']['CHANNEL_ID']

class Veritabani:
	def __init__(self):
		self.database_location = Config.database_location
		self.table_name = Config.table_name
		try:
			self.connection = sql.connect(self.database_location)
			self.db_cursor = self.connection.cursor()
			self.create_table()
		except Exception as ex:
			print("Connection",str(ex))
	def create_table(self):
		query = '''
		CREATE TABLE if not exists {}(
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		link TEXT NOT NULL UNIQUE,
		title TEXT NOT NULL,
		tarih DATE NOT NULL,
		cekildimi BOOLEAN NOT NULL
		)
		'''.format(self.table_name)
		try:
			self.db_cursor.execute(query)
		except Exception as e:
			print("create_table function",query,str(e))
	def new_item(self,object):
		query = "insert or ignore into {}(link,title,tarih,cekildimi) VALUES('{}','{}','{}','{}')".format(
			self.table_name,
			object['link'],
			str(object['title']).replace("'",""),
			object['tarih'],
			False
		)
		try:
			self.db_cursor.execute(query)
		except Exception as ex:
			print("new_item function",query,str(ex))
		self.connection.commit()
	def get_items(self):
		query = "select * from {} where cekildimi='False'".format(self.table_name)
		objects = self.db_cursor.execute(query).fetchall()
		return objects
	def update_item(self,object):
		query = "update {} set cekildimi='True' where id={}".format(self.table_name,object[0])
		self.db_cursor.execute(query)
		self.connection.commit()

			 

reddit = praw.Reddit(client_id=Config.yid,
					 client_secret=Config.reddit_secret_id,
					 user_agent='ChangeMeClient/0.1 by',
					 username=Config.username,
					 password=Config.password)

Vt = Veritabani()



async def updater():
	for item in reddit.subreddit("freegamesonsteam").new(limit=10):
		if item.link_flair_text != "Ended" and item.link_flair_text != "Discussion":
			title = item.title
			url = item.url 
			date = datetime.fromtimestamp(item.created)
			Vt.new_item({'link':url,'title':title,'tarih':date})