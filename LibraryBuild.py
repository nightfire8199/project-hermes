from Library import *

import soundcloud
from gmusicapi import Mobileclient
from gmusicapi import Webclient
import urllib3.contrib.pyopenssl

import webbrowser

urllib3.contrib.pyopenssl.inject_into_urllib3()

### Create Google Play client

G_username = raw_input("Google Play Account Email:")
G_password = raw_input("Google Play Account Pass:")
GOOGLE_DEVICE_ID = ""

G_client = Mobileclient()
logged_in = G_client.login(G_username,G_password)

if(logged_in == True):
	print "\nGoogle Play Account Login Succesful\n"

Deviceclient = Webclient()
Deviceclient.login(G_username,G_password)

DList = Deviceclient.get_registered_devices()	

for device in DList:	
	if device['type'] == "PHONE":
		GOOGLE_DEVICE_ID = device["id"]
		if GOOGLE_DEVICE_ID[:2] == '0x':
			GOOGLE_DEVICE_ID = GOOGLE_DEVICE_ID[2:]
		break

### Create Soundcloud client

S_username = raw_input("Soundcloud Account Username: ")
S_password = raw_input("Soundcloud Account Password: ")
SOUNDCLOUD_CLIENT_ID = raw_input("Soundcloud Client ID: ")
SOUNDCLOUD_CLIENT_SECRET_ID = raw_input("Soundcloud Secret Client ID: ")

S_client = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_ID,
                           client_secret=SOUNDCLOUD_CLIENT_SECRET_ID,
                           username=S_username,
                           password=S_password)

print "\nSoundcloud Account Login Succesful\n"

### Build Library

print "Building Library..."
 
G_lib = []
S_lib = []

S_list = S_client.get('/me/favorites', limit=500)

G_list = G_client.get_all_songs()

for track in G_list:
	new_track = G_Track(track['id'])
	new_track.title = track['title']
	new_track.album = track['album']
	new_track.artist = track['artist']
	new_track.location = 'G'
	G_lib.append(new_track)

for track in S_list:
	new_track = S_Track(track.id)
	new_track.title = track.title
	new_track.artist = track.user['username']
	new_track.location = 'S'
	S_lib.append(new_track)


print ""

Master_lib = S_lib + G_lib

### Sort Master Library

Master_lib.sort(key=lambda x: x.title.upper())

### Allow User Search

print "Type a character to return all songs whose title begins with that character\n"

while(True):
	USI = raw_input("$> ")
	for track in Master_lib:
		if track.title[0].upper() == USI.upper():
			print track.artist, " - ", track.album, " - ", track.title

	
