
from PyQt4 import QtCore, QtGui, uic

class SongItem(QtGui.QListWidgetItem):

	def __init__(self, other, parent = None):
		super(SongItem, self).__init__(parent)
		self.id = other[0]
		self.artist = str(other[1])
		self.album = str(other[2])
		self.title = str(other[3])
		self.setText(self.artist+"   -   "+self.album+"   -   "+self.title)

	@classmethod
	def copyCtor(this, copy):
		newSong = SongItem(['','','',''])
		newSong.id = copy.id
		newSong.artist = copy.artist
		newSong.album = copy.album
		newSong.title = copy.title
		newSong.setText(newSong.artist+"   -   "+newSong.album+"   -   "+newSong.title)
		return newSong

class TableSongItem(QtGui.QTableWidgetItem):

	def __init__(self, other, parent = None):
		super(SongItem, self).__init__(parent)
		self.id = other[0]
		self.setText(str(other[1])+"  -  "+str(other[2])+"  -  "+str(other[3]))