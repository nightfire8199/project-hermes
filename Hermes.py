from User import *
from ClientHandler import *
from Player import *
from IO import *

def play(title, cursor):
	if len(title) > 0:
		track = user.library_get('id', ['streamid', 'location'], 'id', [], title, True)
		player.play_track(client.get_stream_URL(track[1].encode("utf-8"), track[2].encode("utf-8")))
	else:
		player.play()

def stop(title, cursor):
	player.stop()

def add(title, cursor):
	track = user.library_get('id', ['streamid', 'location'], 'id', [], title, True)
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
	user.sync(client)

Print_Banner()

user = User()
client = Client_Handler(user)
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
		user.db.close()
		break
	elif command in func_dict.keys():
		func_dict[command](tail, user.cursor)
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
