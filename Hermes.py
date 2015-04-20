from User import *
from Library import *
from ClientHandler import *
from Player import *
from os import path
import os
import sqlite3
from collections import defaultdict

def sync(cursor):
	### Generate Google Play Songs
	G_list = client.G_client.get_all_songs()

	### Generate Soundcloud Songs
	Fav_Size = 0
	S_list = client.S_client.get('/me/favorites', limit=300)
	while Fav_Size != len(S_list):
		Fav_Size = len(S_list)
		S_list += client.S_client.get('/me/favorites', limit=300, offset=len(S_list))

	# cursor.execute('''DROP TABLE tracks''')
	cursor.execute('''
	    CREATE TABLE IF NOT EXISTS tracks(id INTEGER PRIMARY KEY, title TEXT, album TEXT, artist TEXT, location TEXT, streamid TEXT)
	''')

	for track in G_list:
		cursor.execute('''
			INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?)
			''', (len(user.library), track['title'], track['album'], track['artist'], 'G', track['id']))

	for track in S_list:
		cursor.execute('''
			INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?)
			''', (len(user.library), track.title, "Unknown Album", track.user['username'], 'S', track.id))

	db.commit()

print "   ___           _           _                        "                    
print "  / _ \\_ __ ___ (_) ___  ___| |_       /\\  /\\___ _ __ _ __ ___   ___  ___" 
print " / /_)/ '__/ _ \\| |/ _ \\/ __| __|____ / /_/ / _ \\ '__| '_ ` _ \\ / _ \\/ __|"
print "/ ___/| | | (_) | |  __/ (__| ||_____/ __  /  __/ |  | | | | | |  __/\__ \\"
print "\\/    |_|  \\___// |\\___|\\___|\\__|    \\/ /_/ \\___|_|  |_| |_| |_|\\___||___/"
print "              |__/   \n"                                                     


user = User()
client = Client_Handler(user)

db_relpath = path.join('..', 'hermes-userdata')
if not path.exists(db_relpath):
	os.mkdir(db_relpath)

db_path = path.join(db_relpath, user.profile_name+'_db')
db = sqlite3.connect(db_path)

cursor = db.cursor()

print ""


# cursor.execute('''
# 	SELECT artist, album, title FROM tracks
# 	''')
# user1 = cursor.fetchone() #retrieve the first row
# print(user1[0]) #Print the first column retrieved(user's name)
# all_rows = cursor.fetchall()
# for row in all_rows:
#     # row[0] returns the first column in the query (name).
#     print row[0].encode("utf-8"), row[1].encode("utf-8"), row[2].encode("utf-8")


player = Player()
player.client = client

while(True):
	USI = raw_input("$> ")
	if USI[:4] == 'play' and len(USI) > 5:
		cursor.execute("SELECT DISTINCT(id), streamid, location FROM tracks WHERE id LIKE ?", (USI[5:],))
		track = cursor.fetchone()
		player.play_track(client.get_stream_URL(track[1].encode("utf-8"), track[2].encode("utf-8")))
	elif USI[:4] == 'stop':
		player.stop()
	elif USI[:3] == 'add':
		cursor.execute("SELECT DISTINCT(id), streamid, location FROM tracks WHERE id LIKE ?", (USI[4:],))
		track = cursor.fetchone()
		player.add(track[1].encode("utf-8"), track[2].encode("utf-8"), track[0])
	elif USI[:5] == 'print':
		player.print_queue(cursor)
	elif USI[:5] == 'pause':
		player.pause()
	elif USI[:4] == 'play':
		player.play()
	elif USI[:4] == 'next':
		player.play_next()
	elif USI[:4] == 'prev':
		player.play_prev()
	elif USI[:5] == 'start':
		player.play_queue()
	elif USI[:4] == 'quit':
		db.close()
		break
	elif USI[:4] == 'sync':
		sync(cursor)
	else:

		print "\n...ARTISTS..............."
		cursor.execute("SELECT DISTINCT(artist) FROM tracks WHERE artist LIKE ? OR artist LIKE ? ORDER BY artist", (USI+'%', '% '+USI+'%',))
		all_rows = cursor.fetchall()
		for row in all_rows:
		    # row[0] returns the first column in the query (name).
		    print row[0].encode("utf-8")

		print "\n...ALBUMS..............."
		cursor.execute("SELECT DISTINCT(album) FROM tracks WHERE album LIKE ? OR album LIKE ? ORDER BY album", (USI+'%', '% '+USI+'%',))
		all_rows = cursor.fetchall()
		for row in all_rows:
		    # row[0] returns the first column in the query (name).
		    print row[0].encode("utf-8")

		print "\n...TRACKS..............."
		cursor.execute("SELECT DISTINCT(id), artist, album, title FROM tracks WHERE title LIKE ? OR title LIKE ? ORDER BY artist, album", (USI+'%', '% '+USI+'%',))
		all_rows = cursor.fetchall()
		for row in all_rows:
		    # row[0] returns the first column in the query (name).
		    print row[0], '\t', row[1].encode("utf-8"), ' - ', row[3].encode("utf-8"), ' - ', row[2].encode("utf-8")
