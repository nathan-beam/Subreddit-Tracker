import sqlite3
import json

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

			
db = sqlite3.connect('tracker.db')
cur = db.cursor()
cur.execute("SELECT * FROM users")
rows = cur.fetchall()

with open("out.txt","w") as file:
	tagged = []
	for row in rows: 
		if not row[0] in tagged:
			tagged.append(row[0])
			color = "red"
			if row[1] == "the_donald":
				color = "orange"
			file.writelines(',"tag.'+row[0]+'":{"color":"' + color + '","link":"'+row[2]+'","tag":"/r/'+row[1]+' user"}')

print("Done")
all_subreddits = Object()
cur.execute("SELECT distinct(subreddit) FROM users")
rows = cur.fetchall()
sub_list = []
for row in rows:
	cur.execute('SELECT username,url FROM users where subreddit=?',row)
	users = cur.fetchall()
	sub = Object()
	sub.Name = row[0]
	sub_users = []
	for user in users:
		u = Object()
		u.name = user[0]
		u.link = user[1]
		sub_users.append(u)
	sub.Users = sub_users
	sub_list.append(sub)	
all_subreddits.subreddits = sub_list
with open("subs.json","w") as file:
	file.writelines(all_subreddits.toJSON())
		
