import vlc

class Player:

	def __init__(self):
		self.vlc = vlc.MediaPlayer()

	def play_track(self,track):
		self.vlc.set_mrl(track)
		self.vlc.play()

	def play(self):
		self.vlc.play()

	def pause(self):
		self.vlc.pause()

	def stop(self):
		self.vlc.stop()

	
