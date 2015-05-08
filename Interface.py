from PyQt4 import QtGui, QtCore


class TrackViewer(QtGui.QListWidget):
    def __init__(self, parent=None):
        super(QtGui.QListWidget, self).__init__(parent)
        self.addT = ''
        self.Rmenu = QtGui.QMenu(self)

    def contextMenuEvent(self, event):
        if self.currentRow() != -1:
            self.Rmenu.popup(QtGui.QCursor.pos())
