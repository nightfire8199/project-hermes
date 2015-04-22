from User import *
from ClientHandler import *
from Player import *
from IO import *

def play(title):
	if len(title) > 0:
		track = user.library_get('id', ['streamid', 'location'], 'id', [], title, True)
		player.play_track(client.get_stream_URL(track[1].encode("utf-8"), track[2].encode("utf-8")))
	else:
		player.play()

def stop(title):
	player.stop()

def add(title):
	queue = True
	if not title[0].isdigit():
		name, title = title.split()
		queue = False

	track = user.library_get('id', ['streamid', 'location'], 'id', [], title, True)

	if queue:
		player.add(track[0], track[1].encode("utf-8"), track[2].encode("utf-8"))
	else:
		user.get_playlist(name).add(track[0], track[1].encode("utf-8"), track[2].encode("utf-8"))

def add_track(title):
	pass

def print_queue(title):
	if title == "playlists":
		user.print_playlists()
	else:
		player.print_queue(user.cursor)
def pause(title):
	player.pause()
def next(title):
	player.play_next()
def prev(title):
	player.play_prev()
def start(title):
	if len(title) > 0:
		player.Queue = user.get_playlist(title)
		player.Queue.title = "queue"
		player.Queue.save()
	player.play_queue()

def clear_queue(title):
	player.clear_queue()
def sync(title):
	user.sync(client)

def watch(title, cursor):
	if len(title) > 0:
		user.watched.append(title)
	else:
		for path in user.watched:
			print path

def make_playlist(title):
	user.add_playlist(title)

Print_Banner()

user = User()
client = Client_Handler(user)
player = Player(user)
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
	'sync' : sync,
	'watch': watch,
	'make' : make_playlist
}

while(True):
	USI = raw_input("$> ")

	if len(USI.split(' ', 1)) > 1:
		command, tail = USI.split(' ', 1)
	else:
		command = USI
		tail = ''

	if command == 'quit':
		user.db.close()
		break
	elif command in func_dict.keys():
		func_dict[command](tail)
	else:
		Art_res = set()
		Alb_res = set()
		Tra_res = set()
		for word in USI.split():
			all_rows = user.library_get('artist', [], 'artist', ['artist'], word)
			Art_res = intersect(Art_res, all_rows)
			
			all_rows = user.library_get('album', [], 'album', ['album'], word)
			Alb_res = intersect(Alb_res, all_rows)

			all_rows = user.library_get('id', ['artist','album','title'], 'title', ['artist','album'], word)
			Tra_res = intersect(Tra_res, all_rows)

		Print_Results(Art_res, Alb_res, Tra_res)
