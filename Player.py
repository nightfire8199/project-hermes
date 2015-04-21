import vlc

class Player:

	def __init__(self):
		self.vlc = vlc.MediaPlayer()
		self.events = self.vlc.event_manager()
		self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.auto_next_queue)
		self.Queue = []
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
		if self.pos < len(self.Queue):
			self.vlc.set_mrl(self.client.get_stream_URL(self.Queue[self.pos+1][0],self.Queue[self.pos+1][1]))
			self.vlc.play()
			self.pos+=1
		else:
			print "No next track has been queued"

	def play_prev(self):
		if self.pos > 0:
			self.vlc.set_mrl(self.client.get_stream_URL(self.Queue[self.pos-1][0],self.Queue[self.pos-1][1]))
			self.vlc.play()
			self.pos-=1
		else:
			print "No previous track exists"

	def add(self,sid,location,ident):
		self.Queue.append([sid,location,ident])

	def clear_queue(self):
		del self.Queue[:]

	def print_queue(self, cursor):
		for track in self.Queue:
			if track is self.Queue[self.pos]:
				print ">> ",
			cursor.execute("SELECT artist, title FROM tracks WHERE id LIKE ?", (track[2],))
			result = cursor.fetchone()
			print result[0].encode("utf-8"), " - ", result[1].encode("utf-8")

	def play_queue(self):
		self.vlc.set_mrl(self.client.get_stream_URL(self.Queue[self.pos][0],self.Queue[self.pos][1]))
		self.vlc.play()

	def play(self):
		self.vlc.play()

	def pause(self):
		self.vlc.pause()

	def stop(self):
		self.vlc.stop()

	
