# Temperature-conversion program using PyQt

import sys
from PyQt4 import QtCore, QtGui, uic
from Hermes import *
from SongItem import *

form_class = uic.loadUiType("ui1.ui")[0]                 # Load the UI

class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.searchButton.clicked.connect(self.search)  # Bind the event handlers
        self.searchBox.returnPressed.connect(self.search)
        self.playButton.clicked.connect(self.playSelected)
        self.pauseButton.clicked.connect(self.pauseCurrent)
        self.createActions()
        self.addMenu()
        self.hermes = Hermes()

    def createActions(self):
        self.quitAction = QtGui.QAction('&Quit', self)        
        self.quitAction.setShortcut('Ctrl+Q')
        self.quitAction.setStatusTip('Exit application')
        self.quitAction.triggered.connect(QtGui.qApp.quit)

        self.statusBar()

    def addMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.quitAction)

    def search(self): # button event handler
        searchText = self.searchBox.text()
        result = self.hermes.search(searchText, self)

        self.list.clear()
        for song in result:
            self.list.addItem(SongItem(song))
            # self.list.addItem(str(song[0])+"  -  "+str(song[1])+"  -  "+str(song[2])+"  -  "+str(song[3]))

    def playSelected(self):
        selected = self.list.selectedItems()
        if len(selected) == 0:
            return
        self.current = selected[0].id
        self.hermes.play(self.current)

    def pauseCurrent(self):
        self.hermes.pause()



# Main script
app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()