from Library import *

import vlc

class Player:

	def __init__(self, user):
		self.vlc = vlc.MediaPlayer()
		self.events = self.vlc.event_manager()
		self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.auto_next_queue)
		self.Queue = Playlist("queue", user)
		self.Queue.load()
		self.pos = 0

	def auto_next_queue(self, arg):
		self.vlc = vlc.MediaPlayer()
		self.events = self.vlc.event_manager()
		self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.auto_next_queue)
		self.play_next()

	def play_track(self,track):
		self.vlc.set_mrl(track)
		self.vlc.play()

	def play_next(self):
		if self.pos < len(self.Queue.items):
			self.vlc.set_mrl(self.client.get_stream_URL(self.Queue.items[self.pos+1].streamid,self.Queue.items[self.pos+1].location))
			self.vlc.play()
			self.pos+=1
		else:
			print "No next track has been queued"

	def play_prev(self):
		if self.pos > 0:
			self.vlc.set_mrl(self.client.get_stream_URL(self.Queue.items[self.pos-1].streamid,self.Queue.items[self.pos-1].location))
			self.vlc.play()
			self.pos-=1
		else:
			print "No previous track exists"

	def add(self,ident,sid,location):
		self.Queue.add(ident, sid, location)

	def clear_queue(self):
		self.Queue.clear()

	def print_queue(self, cursor):
		for track in self.Queue.items:
			if track is self.Queue.items[self.pos]:
				print ">> ",
			cursor.execute("SELECT artist, title FROM tracks WHERE id LIKE ?", (track.id,))
			result = cursor.fetchone()
			print result[0].encode("utf-8"), " - ", result[1].encode("utf-8")

	def play_queue(self):
		self.pos = 0
		self.vlc.set_mrl(self.client.get_stream_URL(self.Queue.items[self.pos].streamid,self.Queue.items[self.pos].location))
		self.vlc.play()

	def play(self):
		self.vlc.play()

	def pause(self):
		self.vlc.pause()

	def stop(self):
		self.vlc.stop()

	
