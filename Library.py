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

	def get_stream(self, api,GOOGLE_DEVICE_ID):
		return api.get_stream_url(self.stream_id,GOOGLE_DEVICE_ID)

class S_Track(Track):
	
	def __init__(self, sid):
		Track.__init__(self)
		self.stream_id = sid
		self.stream_string = '/tracks/' + str(self.stream_id)

	def get_stream(self, api,SOUNDCLOUD_CLIENT_ID):
		return api.get(self.stream_string).stream_url + "?client_id=" + SOUNDCLOUD_CLIENT_ID


