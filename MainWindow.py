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
        self.setWindowTitle('Project Hermes')

        self.createActions()
        self.connectActions()
        self.addMenu()
        self.hermes = Hermes()

    def createActions(self):
        self.quitAction = QtGui.QAction('&Quit', self)        
        self.quitAction.setShortcut('Ctrl+Q')
        self.quitAction.setStatusTip('Exit application')

        self.statusBar()

    def connectActions(self):
        self.quitAction.triggered.connect(self.quitApp)
        self.searchButton.clicked.connect(self.search)  # Bind the event handlers
        self.searchBox.returnPressed.connect(self.search)
        self.playButton.clicked.connect(self.playSelected)
        self.pauseButton.clicked.connect(self.pauseCurrent)
        self.searchResults.itemDoubleClicked.connect(self.playSelected)
        self.searchResults.itemDoubleClicked.connect(self.addToQueueAndPlay)
        self.addButton.clicked.connect(self.addToQueue)
        self.clearQueueButton.clicked.connect(self.clearQueue)

    def addMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.quitAction)

    def quitApp(self):
        self.hermes.quit()
        QtGui.qApp.quit()

    def search(self): # button event handler
        searchText = self.searchBox.text()
        result = self.hermes.search(searchText, self)

        self.searchResults.clear()
        for song in result:
            self.searchResults.addItem(SongItem(song))

    def addToQueueAndPlay(self):
        newItem = self.addToQueue()
        print "selecting new item"
        self.nowPlaying.setItemSelected(newItem, True)
        print "playing selected"
        self.playSelected()
        print "now playing"


    def playSelected(self):
        selected = self.nowPlaying.selectedItems()
        if len(selected) == 0:
            return
        self.current = selected[0].id
        self.hermes.play(self.current)

    def pauseCurrent(self):
        self.hermes.pause()

    def addToQueue(self):
        selected = self.searchResults.selectedItems()
        if len(selected) == 0:
            return
        toAdd = selected[0]
        self.hermes.add(toAdd.id)
        newItem = SongItem.copyCtor(toAdd)
        self.nowPlaying.addItem(newItem)
        return newItem

    def clearQueue(self):
        self.hermes.clear_queue()
        self.nowPlaying.clear()



# Main script
app = QtGui.QApplication(sys.argv)
app.setStyleSheet('QMainWindow{background-color: darkgray;}')
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()