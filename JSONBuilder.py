import sqlite3
db = sqlite3.connect('HST.db')
cur = db.cursor()
cur.execute("SELECT * FROM users")
rows = cur.fetchall()

with open("out.txt","w") as file:
	for row in rows: 
		color = "red"
		if row[1] == "the_donald":
			color = "orange"
		file.writelines(',"tag.'+row[0]+'":{"color":"' + color + '","link":"'+row[2]+'","tag":"/r/'+row[1]+' user"}')

print("Done")
