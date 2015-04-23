from User import *
from ClientHandler import *
from Player import *
from IO import *


def play(title):
	if player.Queue.title == 'stream':
		player.stop()
		player.Queue.clear()
		player.Queue.title = 'queue'
		player.pos = 0
	if title.startswith('T'):	
		track = user.library_get('id', ['streamid', 'location'], 'id', [], str(recent_Tra[int(title[1:])]), True)
		player.play_track(client.get_stream_URL(track[1].encode("utf-8"), track[2].encode("utf-8")))
	elif title.startswith('AL'):
		clear_queue('')
		track = user.library_get('id', ['streamid', 'location'], 'album', ['tracknum'], str(recent_Alb[int(title[2:])]))
		add(track)
		start('')
	elif title.startswith('AR'):
		clear_queue('')
		track = user.library_get('id', ['streamid', 'location'], 'artist', ['artist','album','tracknum'], str(recent_Art[int(title[2:])]))
		add(track)
		start('')
	else:
		player.play()

def stop(title):
	player.stop()

def add(title):

	if player.Queue.title == 'stream':
		player.stop()
		player.Queue.clear()
		player.Queue.title = 'queue'
		player.pos = 0
	queue = True

	if isinstance(title, basestring):

		if not (title.startswith('T') or title.startswith('AL') or title.startswith('AR')):
			name, title = title.split()
			queue = False

		if title.startswith('T'):	
			track = user.library_get('id', ['streamid', 'location'], 'id', [], str(recent_Tra[int(title[1:])]), True)
			if queue:
				player.add(track[0], track[1].encode("utf-8"), track[2].encode("utf-8"))
			else:
				user.get_playlist(name).add(track[0], track[1].encode("utf-8"), track[2].encode("utf-8"))

		elif title.startswith('AL'):
			track = user.library_get('id', ['streamid', 'location'], 'album', ['tracknum'], str(recent_Alb[int(title[2:])]))
			if queue:
				add(track)
			else:
				for tracks in track:
					user.get_playlist(name).add(tracks[0], tracks[1].encode("utf-8"), tracks[2].encode("utf-8"))

		elif title.startswith('AR'):
			track = user.library_get('id', ['streamid', 'location'], 'artist', ['artist','album','tracknum'], str(recent_Art[int(title[2:])]))
			if queue:
				add(track)
			else:
				for tracks in track:
					user.get_playlist(name).add(tracks[0], tracks[1].encode("utf-8"), tracks[2].encode("utf-8"))
		else:
			print "Cannot Find: " + title
	
	else:
		for track in title:
			player.add(track[0], track[1].encode("utf-8"), track[2].encode("utf-8"))

def add_track(title):
	pass

def print_queue(title):
	for playlist in user.playlists:
		if playlist.title == "playlist_"+title:
			user.print_playlist(title)
			return
	if title == "playlists":
		user.print_playlists()
	elif len(title) == 0:
		player.print_queue(user.cursor)
	else:
		print "Cannot find playlist <" + title + ">"

def pause(title):
	player.pause()
def next(title):
	player.play_next()
def prev(title):
	player.play_prev()
def start(title):
	if title == 'stream':
		player.Queue.clear()
		player.Queue.title = "stream"
		player.pos = 0
		user.sync_stream(client,player)
	else:
		if len(title) > 0:
			player.Queue = user.get_playlist(title)
			player.Queue.title = "queue"
			player.Queue.save()
	player.play_queue()

def clear_queue(title):
	player.clear_queue()
def sync(title):
	user.sync(client)

def watch(title):
	if len(title) > 0:
		user.add_watched(title)
	else:
		for path in user.watched:
			print path

def make_playlist(title):
	user.add_playlist(title)

def view(title,recent_Art, recent_Alb, recent_Tra):

	if title[:2] == 'AR'and int(title[2:]) <= len(recent_Art):
		all_rows_TR = user.library_get('id', ['artist','album','title','tracknum'], 'artist', ['artist','album','tracknum'], recent_Art[int(title[2:])])
		all_rows_AL = user.library_get('album', [], 'artist', ['album'], recent_Art[int(title[2:])])
		recent_Art, recent_Alb, recent_Tra = Print_Results([], all_rows_AL, all_rows_TR)
	elif title[:2] == 'AL' and int(title[2:]) <= len(recent_Alb):
		all_rows = user.library_get('id', ['artist','album','title','tracknum'], 'album', ['artist','album','tracknum'], recent_Alb[int(title[2:])])
		recent_Art, recent_Alb, recent_Tra = Print_Results([], [], all_rows)
	else:
		print "Cannot find: " + title

	return [recent_Art, recent_Alb, recent_Tra]

def like(title):
	if player.Queue.title == 'stream':
		client.S_client.put('/me/favorites/%d' % int(player.Queue.items[player.pos].streamid[2:]))
	else:
		print "The stream is not curretly playing"

def now(title):
	if player.Queue.title == 'queue' and len(player.Queue.items) > 0:
		track = user.library_get('id', ['title', 'artist', 'location'], 'id', [], str(player.Queue.items[player.pos].id), True)
	elif player.Queue.title == 'stream' and len(player.Queue.items) > 0:
		track = user.stream_get('id', ['title', 'artist', 'location'], 'id', [], str(player.Queue.items[player.pos].id), True)
	else:
		print "Nothing is playing"
		return

	print "Now Playing:\t" + track[1] + "\t by \t" + track[2] + "\t from \t",

	if track[3] == 'S':
		print "Soundcloud"
	elif track[3] == 'G':
		print "Google Play"
	elif track[3] == 'L':
		print "Local Music"
	else:
		print "Unknown"
	

Print_Banner()

user = User()
client = Client_Handler(user)
player = Player(user)
player.client = client

print ""

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
	'sync' : sync,
	'watch': watch,
	'make' : make_playlist,
	'view' : view,
	'like' : like,
	'now' : now
}

def intersect(res, inp):
	if(len(res) == 0):
		for row in inp:
	    		 res.add(row)
	else:
		temp = set()
		for row in inp:
	    		 temp.add(row)
		res = res.intersection(temp)
	return res

while(True):
	USI = raw_input("$> ")

	if len(USI.split(' ', 1)) > 1:
		command, tail = USI.split(' ', 1)
	else:
		command = USI
		tail = ''

	if command == 'quit':
		user.cursor.execute('''DROP TABLE IF EXISTS stream''')
		user.db.commit()
		user.db.close()
		break

	if command == 'search':
		Art_res = set()
		Alb_res = set()
		Tra_res = set()
		for word in tail.split():
			all_rows = user.library_get('artist', [], 'artist', ['artist'], word)
			Art_res = intersect(Art_res, all_rows)
			
			all_rows = user.library_get('album', ['artist'], 'album', ['album'], word)
			Alb_res = intersect(Alb_res, all_rows)

			all_rows = user.library_get('id', ['artist','album','title','tracknum'], 'title', ['artist','album','tracknum'], word)
			Tra_res = intersect(Tra_res, all_rows)

		recent_Art, recent_Alb, recent_Tra = Print_Results(Art_res, Alb_res, Tra_res)

	elif command in func_dict.keys():
		if command == 'view':
			recent_Art, recent_Alb, recent_Tra = func_dict[command](tail,recent_Art, recent_Alb, recent_Tra)
		else:
			func_dict[command](tail)
	else:
		print "Command <" + command + "> not found"

