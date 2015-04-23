
from PyQt4 import QtCore, QtGui, uic

class SongItem(QtGui.QListWidgetItem):

	def __init__(self, other, parent = None):
		super(SongItem, self).__init__(parent)
		self.id = other[0]
		self.setText(str(other[0])+"  -  "+str(other[1])+"  -  "+str(other[2])+"  -  "+str(other[3]))

