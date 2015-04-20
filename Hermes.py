from User import *
from Library import *
from ClientHandler import *
from Player import *

from collections import defaultdict

print "   ___           _           _                        "                    
print "  / _ \\_ __ ___ (_) ___  ___| |_       /\\  /\\___ _ __ _ __ ___   ___  ___" 
print " / /_)/ '__/ _ \\| |/ _ \\/ __| __|____ / /_/ / _ \\ '__| '_ ` _ \\ / _ \\/ __|"
print "/ ___/| | | (_) | |  __/ (__| ||_____/ __  /  __/ |  | | | | | |  __/\__ \\"
print "\\/    |_|  \\___// |\\___|\\___|\\__|    \\/ /_/ \\___|_|  |_| |_| |_|\\___||___/"
print "              |__/   \n"                                                     


user = User()
client = Client_Handler(user)

Fav_Size = 0
S_list = client.S_client.get('/me/favorites', limit=300)
while Fav_Size != len(S_list):
	Fav_Size = len(S_list)
	S_list += client.S_client.get('/me/favorites', limit=300, offset=len(S_list))

G_list = client.G_client.get_all_songs()

for track in G_list:
	new_track = G_Track(track['id'])
	new_track.id = len(user.library)
	if len(track['title']) > 0:
		new_track.title = track['title']
	if len(track['album']) > 0:
		new_track.album = track['album']
	if len(track['artist']) > 0:
		new_track.artist = track['artist']
	new_track.location = 'G'
	user.library.append(new_track)

for track in S_list:
	new_track = S_Track(track.id)
	new_track.id = len(user.library)
	new_track.title = track.title
	new_track.artist = track.user['username']
	new_track.location = 'S'
	user.library.append(new_track)
	
print ""

Search_lib = defaultdict(set)

## Build Database

for track in user.library:
	for word in track.title.split():	
		Search_lib[word.upper()].add(track)
	for word in track.artist.split():
		Search_lib[word.upper()].add(track)
	for word in track.album.split():
		Search_lib[word.upper()].add(track)

### Allow User Search

player = Player()
player.client = client

while(True):
	USI = raw_input("$> ")
	if USI[:4] == 'play' and len(USI) > 5:
		player.play_track(client.get_stream_URL(user.library[int(USI[5:])]))
	elif USI[:4] == 'stop':
		player.stop()
	elif USI[:3] == 'add':
		player.add(user.library[int(USI[4:])])
	elif USI[:5] == 'print':
		player.print_queue()
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
		break
	else:
		newList = sorted(Search_lib[USI.upper()], key=lambda x: x.album)
		for track in newList:
			print track.id, "\t# " ,track.artist.encode("utf-8"), " - ", track.album.encode("utf-8"), " - ", track.title.encode("utf-8")
