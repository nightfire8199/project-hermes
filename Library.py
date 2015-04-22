
import shelve
from os import path

class Playlist:

	def __init__(self, title, user=None):
		self.title = title
		self.items = []
		self.shelve = path.join(user.userdata_path, 'playlist_'+self.title)

	def save(self):
		shelf = shelve.open(self.shelve, 'c')
		shelf[self.title] = self.items
		shelf.close()

	def load(self):
		if not path.exists(self.shelve):
			self.save()
			return

		shelf = shelve.open(self.shelve, 'r')
		self.items = shelf[self.title]
		shelf.close()

	def add(self, id, streamid, location):
		self.items.append(PlaylistItem(id, streamid, location))
		self.save()

	def clear(self):
		self.items = []
		self.save()

	def printItems(self):
		for item in self.items:
			item.printItem()


class PlaylistItem:

	def __init__(self, id, streamid, location):
		self.id = id
		self.streamid = streamid
		self.location = location

	def printItem(self):
		print self.id, self.streamid, self.location