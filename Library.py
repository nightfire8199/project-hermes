class Track:
	
	def __init__(self):
		self.id = -1
		self.title = "Unkown Title"
		self.artist = "Unknown Arist"
		self.album = "Unknown Album"
		self.location = "None"
		
class G_Track(Track):
	
	def __init__(self,sid):
		Track.__init__(self)
		self.stream_id = sid

class S_Track(Track):
	
	def __init__(self, sid):
		Track.__init__(self)
		self.stream_id = sid
		self.stream_string = '/tracks/' + str(self.stream_id)


