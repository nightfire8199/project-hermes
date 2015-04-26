from User import *
from ClientHandler import *
from Player import *
from IO import *
from PyQt4 import QtCore, QtGui, uic

class Hermes:

	def __init__(self, QT_trackBar,QT_nowPlaying):
		Print_Banner()

		self.user = User()
		self.client = Client_Handler(self.user)
		self.player = Player(self.user, QT_trackBar,QT_nowPlaying)
		self.player.client = self.client

		print ""

		self.func_dict = {
			'play' : self.play,
			'stop' : self.stop,
			'add'  : self.add,
			'print': self.print_queue,
			'pause': self.pause,
			'next' : self.next,
			'prev' : self.prev,
			'start': self.start,
			'clear': self.clear_queue,
			'sync' : self.sync,
			'watch': self.watch,
			'make' : self.make_playlist,
			'view' : self.view
		}
		# self.sync("sync")

	def play(self, title):
		if self.player.paused():
			self.player.play()
		elif self.player.Queue.title == 'stream':
			track = self.user.stream_get('id', ['streamid', 'location'], 'id', [], str(title), True)
			self.player.play_track(self.client.get_stream_URL(track[1].encode("utf-8"), track[2].encode("utf-8")))
		else:
			track = self.user.library_get('id', ['streamid', 'location'], 'id', [], str(title), True)
			self.player.play_track(self.client.get_stream_URL(track[1].encode("utf-8"), track[2].encode("utf-8")))
		return

		if self.player.Queue.title == 'stream':
			self.player.stop()
			self.player.Queue.clear()
			self.player.Queue.title = 'queue'
			self.player.pos = 0
		if title.startswith('T'):	
			track = self.user.library_get('id', ['streamid', 'location'], 'id', [], str(recent_Tra[int(title[1:])]), True)
			self.player.play_track(self.client.get_stream_URL(track[1].encode("utf-8"), track[2].encode("utf-8")))
		elif title.startswith('AL'):
			clear_queue('')
			track = self.user.library_get('id', ['streamid', 'location'], 'album', ['tracknum'], str(recent_Alb[int(title[2:])]))
			add(track)
			start('')
		elif title.startswith('AR'):
			clear_queue('')
			track = self.user.library_get('id', ['streamid', 'location'], 'artist', ['artist','album','tracknum'], str(recent_Art[int(title[2:])]))
			add(track)
			start('')
		else:
			self.player.play()

	def stop(self, title):
		self.player.stop()

	def add(self, title):
		track = self.user.library_get('id', ['streamid', 'location'], 'id', [], str(title), True)
		self.player.add(track[0], track[1].encode("utf-8"), track[2].encode("utf-8"))
		return

		if self.player.Queue.title == 'stream':
			self.player.stop()
			self.player.Queue.clear()
			self.player.Queue.title = 'queue'
			self.player.pos = 0
		queue = True

		if isinstance(title, basestring):

			if not (title.startswith('T') or title.startswith('AL') or title.startswith('AR')):
				name, title = title.split()
				queue = False

			if title.startswith('T'):	
				track = self.user.library_get('id', ['streamid', 'location'], 'id', [], str(recent_Tra[int(title[1:])]), True)
				if queue:
					self.player.add(track[0], track[1].encode("utf-8"), track[2].encode("utf-8"))
				else:
					self.user.get_playlist(name).add(track[0], track[1].encode("utf-8"), track[2].encode("utf-8"))

			elif title.startswith('AL'):
				track = self.user.library_get('id', ['streamid', 'location'], 'album', ['tracknum'], str(recent_Alb[int(title[2:])]))
				if queue:
					add(track)
				else:
					for tracks in track:
						self.user.get_playlist(name).add(tracks[0], tracks[1].encode("utf-8"), tracks[2].encode("utf-8"))

			elif title.startswith('AR'):
				track = self.user.library_get('id', ['streamid', 'location'], 'artist', ['artist','album','tracknum'], str(recent_Art[int(title[2:])]))
				if queue:
					add(track)
				else:
					for tracks in track:
						self.user.get_playlist(name).add(tracks[0], tracks[1].encode("utf-8"), tracks[2].encode("utf-8"))
			else:
				print "Cannot Find: " + title
		
		else:
			for track in title:
				self.player.add(track[0], track[1].encode("utf-8"), track[2].encode("utf-8"))

	def add_track(self, title):
		pass

	def print_queue(self, title):
		for playlist in self.user.playlists:
			if playlist.title == "playlist_"+title:
				self.user.print_playlist(title)
				return
		if title == "playlists":
			self.user.print_playlists()
		elif len(title) == 0:
			self.player.print_queue(self.user.cursor)
		else:
			print "Cannot find playlist <" + title + ">"

	def pause(self):
		self.player.pause()
	def next(self):
		self.player.play_next()
	def prev(self):
		self.player.play_prev()
	def start(self, title):
		if title == 'stream':
			self.player.Queue.clear()
			self.player.Queue.title = "stream"
			self.user.sync_stream(self.client,self.player)
		else:
			if len(title) > 0:
				self.player.Queue = self.user.get_playlist(title)
				self.player.Queue.title = "queue"
				self.player.Queue.save()
		#self.player.play_queue()

	def clear_queue(self):
		self.player.clear_queue()
	def sync(self, title):
		self.user.sync(self.client)

	def watch(self, title):
		if len(title) > 0:
			self.user.add_watched(title)
		else:
			for path in self.user.watched:
				print path

	def make_playlist(self, title):
		self.user.add_playlist(title)

	def view(self, title,recent_Art, recent_Alb, recent_Tra):

		if title[:2] == 'AR'and int(title[2:]) <= len(recent_Art):
			all_rows_TR = self.user.library_get_exact('id', ['artist','album','title','tracknum'], 'artist', ['artist','album','tracknum'], recent_Art[int(title[2:])])
			all_rows_AL = self.user.library_get_exact('album', ['artist'], 'artist', ['album'], recent_Art[int(title[2:])])
			recent_Art, recent_Alb, recent_Tra = Print_Results([], all_rows_AL, all_rows_TR)
		elif title[:2] == 'AL' and int(title[2:]) <= len(recent_Alb):
			all_rows = self.user.library_get_exact('id', ['artist','album','title','tracknum'], 'album', ['artist','album','tracknum'], recent_Alb[int(title[2:])])
			recent_Art, recent_Alb, recent_Tra = Print_Results([], [], all_rows)
		else:
			print "Cannot find: " + title

		return [recent_Art, recent_Alb, recent_Tra]

	def view_Al(self, album):
		all_rows = self.user.library_get_exact('id', ['artist','album','title','tracknum'], 'album', ['artist','album','tracknum'], album.album)
		recent_Art, recent_Alb, recent_Tra = Print_Results([], [], all_rows)
		return [[], [], all_rows]

	def view_Ar(self,artist):
		all_rows_TR = self.user.library_get_exact('id', ['artist','album','title','tracknum'], 'artist', ['artist','album','tracknum'], artist.artist)
		all_rows_AL = self.user.library_get_exact('album', ['artist'], 'artist', ['album'], artist.artist)
		recent_Art, recent_Alb, recent_Tra = Print_Results([], all_rows_AL, all_rows_TR)
		return [[], all_rows_AL, all_rows_TR]

	def intersect(self, res, inp):
		if(len(res) == 0):
			for row in inp:
		    		 res.add(row)
		else:
			temp = set()
			for row in inp:
		    		 temp.add(row)
			res = res.intersection(temp)
		return res

	def like(self):
		if self.player.Queue.title == 'stream':
			self.client.S_client.put('/me/favorites/%d' % int(self.player.Queue.items[self.player.pos].streamid[2:]))
		else:
			print "The stream is not curretly playing"

	# while(True):
	# 	USI = raw_input("$> ")

	# 	if len(USI.split(' ', 1)) > 1:
	# 		command, tail = USI.split(' ', 1)
	# 	else:
	# 		command = USI
	# 		tail = ''

	# 	if command == 'quit':
	# 		user.cursor.execute('''DROP TABLE IF EXISTS stream''')
	# 		user.db.close()
	# 		break

	# 	if command == 'search':
	# 		Art_res = set()
	# 		Alb_res = set()
	# 		Tra_res = set()
	# 		for word in tail.split():
	# 			all_rows = user.library_get('artist', [], 'artist', ['artist'], word)
	# 			Art_res = intersect(Art_res, all_rows)
				
	# 			all_rows = user.library_get('album', [], 'album', ['album'], word)
	# 			Alb_res = intersect(Alb_res, all_rows)

	# 			all_rows = user.library_get('id', ['artist','album','title','tracknum'], 'title', ['artist','album','tracknum'], word)
	# 			Tra_res = intersect(Tra_res, all_rows)

	# 		recent_Art, recent_Alb, recent_Tra = Print_Results(Art_res, Alb_res, Tra_res)

	# 	elif command in func_dict.keys():
	# 		if command == 'view':
	# 			recent_Art, recent_Alb, recent_Tra = func_dict[command](tail,recent_Art, recent_Alb, recent_Tra)
	# 		else:
	# 			func_dict[command](tail)
	# 	else:
	# 		print "Command <" + command + "> not found"

	def search(self, tail, parent):
		Art_res = set()
		Alb_res = set()
		Tra_res = set()
		tail = str(tail)
		for word in tail.split():
			all_rows = self.user.library_get('artist', [], 'artist', ['artist'], word)
			Art_res = intersect(Art_res, all_rows)
			
			all_rows = self.user.library_get('album', ['artist'], 'album', ['album'], word)
			Alb_res = intersect(Alb_res, all_rows)

			all_rows = self.user.library_get('id', ['artist','album','title','tracknum'], 'title', ['artist','album','tracknum'], word)
			Tra_res = intersect(Tra_res, all_rows)

		recent_Art, recent_Alb, recent_Tra = Print_Results(Art_res, Alb_res, Tra_res)

		return [Art_res, Alb_res, Tra_res]

	def quit(self):
		self.user.cursor.execute('''DROP TABLE IF EXISTS stream''')
		self.user.db.close()
		
