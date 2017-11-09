import praw
import json
import operator
import sys
import threading
import copy
import sqlite3
import queue
subreddits = {}

reddit = None
queue = queue.Queue()
def init():
	global subreddits
	global reddit
	with open('ExampleConfig.json') as settings_file:    
		settings = json.load(settings_file)
		subreddits= settings["subreddits"]
	
	reddit = praw.Reddit(client_id=settings["client_id"],
						 client_secret=settings["secret"],
						 password=settings["password"],
						 user_agent='Script by /u/morpen: Sub tracker',
						 username=settings["username"])

def get_subreddit_name():
	sub_name = ""
	for sub in subreddits:
		sub_name+="+"
		sub_name+=sub
	return sub_name[1:]

def monitor_comments(subreddit):
	for comment in subreddit.stream.comments():
		if not comment.author.name.lower() == "automoderator":
			queue.put((comment.author.name.lower(), comment.subreddit.display_name.lower(), "https://np.reddit.com"+comment.permalink))
		
def monitor_submissions(subreddit):
	for submission in subreddit.stream.submissions():
		if not submission.author.name.lower() == "automoderator":
			queue.put((submission.author.name.lower(), submission.subreddit.display_name.lower(), "https://np.reddit.com"+submission.permalink))
		
def insertion_listener():
	db = sqlite3.connect('tracker.db')
	create_table(db.cursor())
	while True:
		if(not queue.empty()):
			row = queue.get()
			insert(db,row[0],row[1], row[2])
			
def create_table(c):
	try:
		create_users_table = """ CREATE TABLE IF NOT EXISTS users (
									username varchar,
									subreddit varchar,
									link varchar
								); """
		c.execute(create_users_table)
	except Error as e:
		print(e)

def insert(db,username, subreddit, link):
	db.cursor().execute("SELECT EXISTS(SELECT 1 FROM users WHERE username=? AND subreddit=?)",(username,subreddit,))
	if not db.cursor().fetchone():
		db.cursor().execute("INSERT INTO users VALUES(?,?,?)",[username,subreddit,link])
		db.commit()
	
init()
sub_name = get_subreddit_name()
subreddit = reddit.subreddit(sub_name)

t1 = threading.Thread(target=monitor_comments, args=(subreddit,))
t2 = threading.Thread(target=monitor_submissions, args=(subreddit,))
t3 = threading.Thread(target=insertion_listener)
t1.start()
t2.start()
t3.start()
