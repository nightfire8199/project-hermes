from gmusicapi import Webclient
from Library import *

import eyeD3

import sys
import os
import sqlite3
from os import path
import getpass
import base64
import pickle

class User:
	
	def __init__(self):
		self.library = []
		self.G_username = ""
		self.G_password = ""
		self.S_username = ""
		self.S_password = ""
		self.GOOGLE_DEVICE_ID = ""
		self.SOUNDCLOUD_CLIENT_ID = ""
		self.SOUNDCLOUD_CLIENT_SECRET_ID = ""
		self.enc_key = "private_key"

		self.playlists = []

		if(len(sys.argv) >= 2):
			try:
				File = open(self.get_filename(str(sys.argv[1])))
			except IOError:
				print 'Cannot find user: ' + str(sys.argv[1])
				print 'Creating new user...'
				self.authenticate(self.get_filename())
			else:
				self.login(self.get_filename(str(sys.argv[1])))
		else:
			self.authenticate(self.get_filename())

		if not path.exists(self.userdata_path):
			os.mkdir(self.userdata_path)

		self.db_path = path.join(self.userdata_path, self.profile_name+'_db')
		self.db = sqlite3.connect(self.db_path)
		self.cursor = self.db.cursor()

		self.watched_file = path.join(self.userdata_path, self.profile_name+"_watched")

		self.watched = []
		if not path.exists(self.watched_file):
			#print "no watched file"
			open(self.watched_file, 'w').close()

		if os.stat(self.watched_file).st_size > 0:
			file = open(self.watched_file, 'r')
			self.watched = pickle.load(file)
			file.close()

		for file in os.listdir(self.userdata_path):
			if file.startswith("playlist_"):
				#print "Adding playlist " , file
				playlist = Playlist(file, self)
				self.playlists.append(playlist)

	def add_watched(self, path):
		self.watched.append(path)
		file = open(self.watched_file, 'w')
		pickle.dump(self.watched, file)
		file.close()

	def encode(self, key, clear):
	    enc = []
	    for i in range(len(clear)):
	        key_c = key[i % len(key)]
	        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
	        enc.append(enc_c)
	    return base64.urlsafe_b64encode("".join(enc))

	def decode(self, key, enc):
	    dec = []
	    enc = base64.urlsafe_b64decode(enc)
	    for i in range(len(enc)):
	        key_c = key[i % len(key)]
	        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
	        dec.append(dec_c)
	    return "".join(dec)

	def get_filename(self, arg=None):
		if arg is None:
			arg = raw_input('Choose a user profile filename: ')
		self.profile_name = arg
		self.userdata_path = path.join('..', 'hermes-userdata', arg)
		if not path.exists(self.userdata_path):
			os.mkdir(self.userdata_path)

		return path.join(self.userdata_path, arg)

	def add_playlist(self, name):
		self.playlists.append(Playlist("playlist_"+name, self))

	def get_playlist(self, name):
		for item in self.playlists:
			if item.title == "playlist_"+name:
				return item

	def print_playlists(self):
		print "\n...Playlists..............."
		for playlist in self.playlists:
			print "    ", playlist.title[9:]

	# def remove_playlist(self, name):
	# 	self.playlists.append(Playlist(name, self))

	def sync(self, client):

		L_list = []
		for path in self.watched:
			filelist = []
			for (dirpath, dirnames, filenames) in os.walk(path):
    				filelist.extend(dirpath + '/' + filename for filename in filenames)
			L_list += filelist	

		for File in L_list:
			if not (File.endswith('mp3') or File.endswith('wav')):
				L_list.remove(File)

		G_list = client.G_client.get_all_songs()	

		Fav_Size = 0
		S_list = client.S_client.get('/me/favorites', limit=300)
		while Fav_Size != len(S_list):
			Fav_Size = len(S_list)
			S_list += client.S_client.get('/me/favorites', limit=300, offset=len(S_list))

		# cursor.execute('''DROP TABLE tracks''')
		self.cursor.execute('''
		    CREATE TABLE IF NOT EXISTS tracks(id INTEGER PRIMARY KEY, title TEXT, album TEXT, artist TEXT, location TEXT, streamid TEXT)
		''')
		iden = 0
		for track in G_list:
			self.cursor.execute('''
				INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?)
				''', (iden, track['title'], track['album'], track['artist'], 'G', track['id']))
			iden+=1

		for track in S_list:
			self.cursor.execute('''
				INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?)
				''', (iden, track.title, "Unknown Album", track.user['username'], 'S', track.id))
			iden+=1

		for track in L_list:
			tag = eyeD3.Tag()
			tag.link(track)
			if len(tag.getArtist()) and len(tag.getAlbum()) and len(tag.getTitle()) > 0:
				self.cursor.execute('''
					INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?)
					''', (iden, tag.getTitle(), tag.getAlbum(), tag.getArtist(), 'L', track))
				iden+=1
			else:
				print "Could not resolve track metadata for: " + track

		self.db.commit()

	def login(self,USER_DATA_FILENAME):
		File = open(USER_DATA_FILENAME,'r')
		self.G_username = self.decode(self.enc_key, File.readline().rstrip('\n'))
		self.G_password = self.decode(self.enc_key, File.readline().rstrip('\n'))
		self.S_username = self.decode(self.enc_key, File.readline().rstrip('\n'))
		self.S_password = self.decode(self.enc_key, File.readline().rstrip('\n'))
		self.GOOGLE_DEVICE_ID = File.readline().rstrip('\n')
		self.SOUNDCLOUD_CLIENT_ID = File.readline().rstrip('\n')
		self.SOUNDCLOUD_CLIENT_SECRET_ID = File.readline().rstrip('\n')
		File.close()

	def library_get(self, distinct, get_others, where_like, ordered_return, USI, single = False):
		query = 'SELECT DISTINCT(' + distinct + ')'
		for item in get_others:
			query += ', ' + item
		query += ' FROM tracks WHERE ' + where_like + ' LIKE ? OR ' + where_like +' LIKE ?'
		if len(ordered_return) > 0:		
			query += ' ORDER BY '
			for item in ordered_return:
				query += item + ', '
			query = query[:len(query)-2]
		self.cursor.execute(query, (USI+'%', '% '+USI+'%',))
		if single == False:
			return self.cursor.fetchall()
		else:
			return self.cursor.fetchone()

	def authenticate(self,USER_DATA_FILENAME):
		self.G_username = raw_input("Google Play Account Email: ")
		self.G_password = getpass.getpass("Google Play Account Pass: ")

		Deviceclient = Webclient()
		Deviceclient.login(self.G_username,self.G_password)

		DList = Deviceclient.get_registered_devices()	

		for device in DList:	
			if device['type'] == "PHONE":
				self.GOOGLE_DEVICE_ID = device["id"]
				if self.GOOGLE_DEVICE_ID[:2] == '0x':
					self.GOOGLE_DEVICE_ID = self.GOOGLE_DEVICE_ID[2:]
				break

		self.S_username = raw_input("Soundcloud Account Username: ")
		self.S_password = getpass.getpass("Soundcloud Account Password: ")
		self.SOUNDCLOUD_CLIENT_ID = raw_input("Soundcloud Client ID: ")
		self.SOUNDCLOUD_CLIENT_SECRET_ID = raw_input("Soundcloud Secret Client ID: ")

		File = open(USER_DATA_FILENAME,'w+')
		File.write(self.encode(self.enc_key, self.G_username) + '\n')
		File.write(self.encode(self.enc_key, self.G_password) + '\n')
		File.write(self.encode(self.enc_key, self.S_username) + '\n')
		File.write(self.encode(self.enc_key, self.S_password) + '\n')
		File.write(self.GOOGLE_DEVICE_ID + '\n')
		File.write(self.SOUNDCLOUD_CLIENT_ID + '\n')
		File.write(self.SOUNDCLOUD_CLIENT_SECRET_ID + '\n')
		File.close()

	def get_command(self,_command):
		pass
