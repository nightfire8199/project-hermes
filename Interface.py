from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *

class AlbumViewer(QtGui.QListWidget):

	def __init__(self, _MW, parent=None):
        	super(QtGui.QListWidget, self).__init__(parent)
		self.MW = _MW

	def contextMenuEvent(self, event):
		if self.currentRow() != -1:
			self.menu = QtGui.QMenu(self)
			renameAction = QtGui.QAction('Add to Queue', self)
			renameAction.triggered.connect(self.additem)
			self.menu.addAction(renameAction)

			self.menu.popup(QtGui.QCursor.pos())

	def additem(self,arg):
		tracks = self.MW.hermes.user.library_get_exact('id', ['artist','album','title','tracknum','art'], 'album', ['tracknum'], self.currentItem().album)
		for track in tracks:
			self.MW.addToQueue(track)

class TrackViewer(QtGui.QListWidget):

	def __init__(self, _MW, parent=None):
        	super(QtGui.QListWidget, self).__init__(parent)
		self.MW = _MW

	def contextMenuEvent(self, event):
		if self.currentRow() != -1:
			self.menu = QtGui.QMenu(self)
			renameAction = QtGui.QAction('Add to Queue', self)
			renameAction.triggered.connect(self.additem)
			self.menu.addAction(renameAction)

			self.menu.popup(QtGui.QCursor.pos())

	def additem(self,arg):
		self.MW.addToQueue()
