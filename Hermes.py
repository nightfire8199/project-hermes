from User import *
from ClientHandler import *
from Player import *
from os import path
import os
import sqlite3
import string

from collections import defaultdict

def sync(cursor):
	G_list = client.G_client.get_all_songs()

	Fav_Size = 0
	S_list = client.S_client.get('/me/favorites', limit=300)
	while Fav_Size != len(S_list):
		Fav_Size = len(S_list)
		S_list += client.S_client.get('/me/favorites', limit=300, offset=len(S_list))

	# cursor.execute('''DROP TABLE tracks''')
	cursor.execute('''
	    CREATE TABLE IF NOT EXISTS tracks(id INTEGER PRIMARY KEY, title TEXT, album TEXT, artist TEXT, location TEXT, streamid TEXT)
	''')
	iden = 0
	for track in G_list:
		cursor.execute('''
			INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?)
			''', (iden, track['title'], track['album'], track['artist'], 'G', track['id']))
		iden+=1

	for track in S_list:
		cursor.execute('''
			INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?)
			''', (iden, track.title, "Unknown Album", track.user['username'], 'S', track.id))
		iden+=1

	db.commit()

def play(title, cursor):
	if len(title) > 0:
		cursor.execute("SELECT DISTINCT(id), streamid, location FROM tracks WHERE id LIKE ?", (title,))
		track = cursor.fetchone()
		player.play_track(client.get_stream_URL(track[1].encode("utf-8"), track[2].encode("utf-8")))
	else:
		player.play()

def stop(title, cursor):
	player.stop()

def add(title, cursor):
	cursor.execute("SELECT DISTINCT(id), streamid, location FROM tracks WHERE id LIKE ?", (title,))
	track = cursor.fetchone()
	player.add(track[1].encode("utf-8"), track[2].encode("utf-8"), track[0])

def print_queue(title, cursor):
	player.print_queue(cursor)
def pause(title, cursor):
	player.pause()
def next(title, cursor):
	player.play_next()
def prev(title, cursor):
	player.play_prev()
def start(title, cursor):
	player.play_queue()
def clear_queue(title, cursor):
	player.clear_queue()
def sync(title, cursor):
	sync(cursor)


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

### Allow User Search

player = Player()
player.client = client

func_dict = {
	'play' : play,
	'stop' : stop,
	'add'  : add,
	'print': print_queue,
	'pause': pause,
	'next' : next,
	'prev' : prev,
	'start': start,
	'clear': clear_queue,
	'sync' : sync
}

while(True):
	USI = raw_input("$> ")

	if len(USI.split()) > 1:
		command, tail = USI.split()
	else:
		command = USI
		tail = ''

	if command == 'quit':
		db.close()
		break
	elif command in func_dict.keys():
		func_dict[command](tail, cursor)
	else:
		Art_res = set()
		Alb_res = set()
		Tra_res = set()
		for word in USI.split():
			cursor.execute("SELECT DISTINCT(artist) FROM tracks WHERE artist LIKE ? OR artist LIKE ? ORDER BY artist", (word+'%', '% '+word+'%',))
			all_rows = cursor.fetchall()
			if(len(Art_res) == 0):
				for row in all_rows:
			    		 Art_res.add(row[0].encode("utf-8"))
			else:
				temp = set()
				for row in all_rows:
			    		 temp.add(row[0].encode("utf-8"))
				Art_res = Art_res.intersection(temp)

			
			cursor.execute("SELECT DISTINCT(album) FROM tracks WHERE album LIKE ? OR album LIKE ? ORDER BY album", (word+'%', '% '+word+'%',))
			all_rows = cursor.fetchall()
			if(len(Alb_res) == 0):
				for row in all_rows:
			    		 Alb_res.add(row[0].encode("utf-8"))
			else:
				temp = set()
				for row in all_rows:
			    		 temp.add(row[0].encode("utf-8"))
				Alb_res = Alb_res.intersection(temp)

			
			cursor.execute("SELECT DISTINCT(id), artist, album, title FROM tracks WHERE title LIKE ? OR title LIKE ? ORDER BY artist, album", (word+'%', '% '+word+'%',))
			all_rows = cursor.fetchall()
			if(len(Tra_res) == 0):
				for row in all_rows:
			    		 Tra_res.add(row)
			else:
				temp = set()
				for row in all_rows:
			    		 temp.add(row)
				Tra_res = Tra_res.intersection(temp)

		print "\n...ARTISTS..............."
		for artist in Art_res:
			print artist
		print "\n...ALBUMS..............."
		for album in Alb_res:
			print album
		print "\n...TRACKS..............."
		for [ident,artist,album,track] in Tra_res:
			print ident, '\t', artist.encode("utf-8"), ' - ', album.encode("utf-8"), ' - ', track.encode("utf-8")
