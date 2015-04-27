from Library import *

import vlc

class Player:

	def __init__(self, user, QT_trackBar,QT_nowPlaying):
		self.vlc = vlc.MediaPlayer()
		self.events = self.vlc.event_manager()
		self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.auto_next_queue)
		self.events.event_attach(vlc.EventType.MediaPlayerTimeChanged, self.change_time)
		self.Queue = Playlist("queue", user)
		self.Queue.load()
		self.pos = 0
		self.QT_track_bar = QT_trackBar
		self.QT_queue = QT_nowPlaying
		self.is_paused = False
		self.QT_queue.setCurrentRow(0)

	def auto_next_queue(self, arg):
		self.vlc = vlc.MediaPlayer()
		self.events = self.vlc.event_manager()
		self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.auto_next_queue)
		self.events.event_attach(vlc.EventType.MediaPlayerTimeChanged, self.change_time)
		self.play_next()

	def play_track(self,track):
		self.vlc.set_mrl(track)
		self.pos = self.QT_queue.currentRow()
		self.play()

	def change_time(self,arg):
		self.QT_track_bar.setValue(int(self.vlc.get_position() * self.QT_track_bar.maximum()))

	def play_next(self):
		if self.pos < len(self.Queue.items)-1:
			self.QT_queue.setCurrentRow(self.pos+1)
			self.vlc.set_mrl(self.client.get_stream_URL(self.Queue.items[self.pos+1].streamid,self.Queue.items[self.pos+1].location))
			self.play()
			self.pos+=1
		else:
			print "No next track has been queued"

	def play_prev(self):
		if self.pos > 0:
			self.QT_queue.setCurrentRow(self.pos-1)
			self.vlc.set_mrl(self.client.get_stream_URL(self.Queue.items[self.pos-1].streamid,self.Queue.items[self.pos-1].location))
			self.play()
			self.pos-=1
		else:
			print "No previous track exists"

	def add(self,ident,sid,location):
		self.Queue.add(ident, sid, location)

	def clear_queue(self):
		self.Queue.clear()
		self.Queue.title = 'queue'
		self.pos = 0

	def print_queue(self, cursor):
		if self.Queue.title == "stream":
			for track in self.Queue.items:
				if track is self.Queue.items[self.pos]:
					print ">> ",
				cursor.execute("SELECT artist, title FROM stream WHERE id LIKE ?", (track.id,))
				result = cursor.fetchone()
				print result[0].encode("utf-8"), " - ", result[1].encode("utf-8")	
		else:
			for track in self.Queue.items:
				if track is self.Queue.items[self.pos]:
					print ">> ",
				cursor.execute("SELECT artist, title FROM tracks WHERE id LIKE ?", (track.id,))
				result = cursor.fetchone()
				print result[0].encode("utf-8"), " - ", result[1].encode("utf-8")

	def get_queue(self,cursor):
		result = []
		if self.Queue.title == "stream":
			for track in self.Queue.items:
				if track is self.Queue.items[self.pos]:
					print ">> ",
				cursor.execute("SELECT id, artist, album, title, tracknum, art FROM stream WHERE id LIKE ?", (track.id,))
				result.append(cursor.fetchone())
				#print result[0].encode("utf-8"), " - ", result[1].encode("utf-8")	
		else:
			for track in self.Queue.items:
				if track is self.Queue.items[self.pos]:
					print ">> ",
				cursor.execute("SELECT id, artist, album, title, tracknum, art FROM tracks WHERE id LIKE ?", (track.id,))
				result.append(cursor.fetchone())
				#print result[0].encode("utf-8"), " - ", result[1].encode("utf-8")
		return result

	def play_queue(self, posit=0):
		self.pos = posit
		self.vlc.set_mrl(self.client.get_stream_URL(self.Queue.items[self.pos].streamid,self.Queue.items[self.pos].location))
		self.play()

	def play(self):
		self.vlc.play()
		self.is_paused = False

	def paused(self):
		return self.is_paused

	def pause(self):
		self.vlc.pause()
		self.is_paused = True

	def stop(self):
		self.vlc.stop()
		self.is_playing = False

	
