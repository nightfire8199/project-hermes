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
			self.vlc.set_mrl(self.client.get_stream_URL(self.Queue[self.pos+1]))
			self.vlc.play()
			self.pos+=1
		else:
			print "No next track has been queued"

	def play_prev(self):
		if self.pos > 0:
			self.vlc.set_mrl(self.client.get_stream_URL(self.Queue[self.pos-1]))
			self.vlc.play()
			self.pos-=1
		else:
			print "No previous track exists"

	def add(self,track):
		self.Queue.append(track)

	def print_queue(self):
		for track in self.Queue:
			if track is self.Queue[self.pos]:
				print ">> ",
			print track.artist, " - ", track.title

	def play_queue(self):
		self.vlc.set_mrl(self.client.get_stream_URL(self.Queue[self.pos]))
		self.vlc.play()

	def play(self):
		self.vlc.play()

	def pause(self):
		self.vlc.pause()

	def stop(self):
		self.vlc.stop()

	
