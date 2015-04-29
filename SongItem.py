
from PyQt4 import QtCore, QtGui, uic

class SongItem(QtGui.QListWidgetItem):

	def __init__(self, other, parent = None):
		super(SongItem, self).__init__(parent)
		self.id = other[0]
		self.artist = str(other[1].encode("utf-8"))
		self.album = str(other[2].encode("utf-8"))
		self.title = str(other[3].encode("utf-8"))
		self.art = str(other[5].encode("utf-8"))
		self.setText(self.title+"\non: "+self.album+"\nby: "+self.artist)

	@classmethod
	def copyCtor(this, copy):
		newSong = SongItem(['','','','','',''])
		newSong.id = copy.id
		newSong.artist = copy.artist
		newSong.album = copy.album
		newSong.title = copy.title
		newSong.art = copy.art
		newSong.setText(newSong.title+"\non: "+newSong.album+"\nby: "+newSong.artist)
		return newSong

class ArtistItem(QtGui.QListWidgetItem):

	def __init__(self, other, parent = None):
		super(ArtistItem, self).__init__(parent)
		self.artist = str(other[0].encode("utf-8"))
		self.setText(self.artist)

	@classmethod
	def copyCtor(this, copy):
		newArtist = ArtistItem([''])
		newArtist.artist = copy.artist
		newArtist.setText(newArtist.artist)
		return newArtist

class AlbumItem(QtGui.QListWidgetItem):

	def __init__(self, other, parent = None):
		super(AlbumItem, self).__init__(parent)
		self.artist = str(other[1].encode("utf-8"))
		self.album = str(other[0].encode("utf-8"))
		self.setText(self.album+"   -   "+self.artist)

	@classmethod
	def copyCtor(this, copy):
		newAlbum = AlbumItem(['',''])
		newAlbum.artist = copy.artist
		newAlbum.album = copy.album
		self.setText(newAlbum.album+"\nby: "+newAlbum.artist)
		return newAlbum



class TableSongItem(QtGui.QTableWidgetItem):

	def __init__(self, other, parent = None):
		super(SongItem, self).__init__(parent)
		self.id = other[0]
		self.setText(str(other[1])+"  -  "+str(other[2])+"  -  "+str(other[3]))
