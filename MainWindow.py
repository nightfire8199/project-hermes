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
        self.hermes = Hermes(self.trackSlider,self.nowPlaying)

	currQueue = self.hermes.player.get_queue(self.hermes.user.cursor)
	for track in currQueue:
		newItem = SongItem(track)
        	self.nowPlaying.addItem(newItem)

	self.likeButton.hide()
		

    def createActions(self):
        self.quitAction = QtGui.QAction('&Quit', self)        
        self.quitAction.setShortcut('Ctrl+Q')
        self.quitAction.setStatusTip('Exit application')
        self.syncAction = QtGui.QAction('&Sync', self)        
        self.syncAction.setShortcut('Ctrl+S')
        self.syncAction.setStatusTip('Sync Library')

        self.statusBar()

    def connectActions(self):
        self.quitAction.triggered.connect(self.quitApp)
        self.searchButton.clicked.connect(self.search)  # Bind the event handlers
        self.searchBox.returnPressed.connect(self.search)
        self.startButton.clicked.connect(self.playSelected)
	self.playpauseButton.clicked.connect(self.playpause)
	self.nextButton.clicked.connect(self.playnext)
	self.prevButton.clicked.connect(self.playprev)
     	self.searchResults_Alb.itemDoubleClicked.connect(self.viewAlbum)
	self.searchResults_Art.itemDoubleClicked.connect(self.viewArtist)
        self.searchResults_Tra.itemDoubleClicked.connect(self.addToQueueAndPlay)
	self.syncAction.triggered.connect(self.sync)
        self.addButton.clicked.connect(self.addToQueue)
	self.trackSlider.sliderReleased.connect(self.setTime)
        self.clearQueueButton.clicked.connect(self.clearQueue)
	self.streamButton.clicked.connect(self.getStream)
	self.likeButton.clicked.connect(self.like)

    def addMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.quitAction)
        toolMenu = menubar.addMenu('&Tools')
        toolMenu.addAction(self.syncAction)

    def quitApp(self):
        self.hermes.quit()
        QtGui.qApp.quit()

    def search(self): # button event handler
        searchText = self.searchBox.text()
        [artists,albums,tracks] = self.hermes.search(searchText, self)

        self.searchResults_Tra.clear()
 	self.searchResults_Alb.clear()
	self.searchResults_Art.clear()
        for song in tracks:
            self.searchResults_Tra.addItem(SongItem(song))
	for album in albums:
	    self.searchResults_Alb.addItem(AlbumItem(album))
	for artist in artists:
	    self.searchResults_Art.addItem(ArtistItem(artist))

    def addToQueueAndPlay(self):
        newItem = self.addToQueue()
        print "selecting new item"
        self.nowPlaying.setItemSelected(newItem, True)
        print "playing selected"
        self.playSelected()
        print "now playing"


    def playSelected(self):
	print self.nowPlaying.currentRow()
        selected = self.nowPlaying.selectedItems()
        if len(selected) == 0:
            return
        self.current = selected[0].id
	self.playpauseButton.setText(QtCore.QString('Pause'))
        self.hermes.play(self.current)

    def addToQueue(self):
        selected = self.searchResults_Tra.selectedItems()
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

    def setTime(self):
	position = float(self.trackSlider.sliderPosition())/float(self.trackSlider.maximum())
	self.hermes.player.vlc.set_position(position)

    def viewArtist(self):
	selected = self.searchResults_Art.selectedItems()
	[artists,albums,tracks] = self.hermes.view_Ar(selected[0])

        self.searchResults_Tra.clear()
 	self.searchResults_Alb.clear()
	self.searchResults_Art.clear()
        for song in tracks:
            self.searchResults_Tra.addItem(SongItem(song))
	for album in albums:
	    self.searchResults_Alb.addItem(AlbumItem(album))
	self.searchResults_Art.addItem(ArtistItem([selected[0].artist]))

    def viewAlbum(self):
	selected = self.searchResults_Alb.selectedItems()
	[artists,albums,tracks] = self.hermes.view_Al(selected[0])

        self.searchResults_Tra.clear()
 	self.searchResults_Alb.clear()
	self.searchResults_Art.clear()
        for song in tracks:
            self.searchResults_Tra.addItem(SongItem(song))
	self.searchResults_Alb.addItem(AlbumItem([selected[0].album,selected[0].artist]))
	self.searchResults_Art.addItem(ArtistItem([selected[0].artist]))

    def sync(self):
	print "Syncing Library"
	self.hermes.user.sync(self.hermes.client)
	print "Sync Complete"

    def playpause(self):
	if self.hermes.player.vlc.is_playing():
		self.playpauseButton.setText(QtCore.QString('Play'))
		self.hermes.player.vlc.pause()
	else:
		self.playpauseButton.setText(QtCore.QString('Pause'))
		self.hermes.player.vlc.play()

    def playnext(self):
	self.hermes.next()

    def playprev(self):
	self.hermes.prev()

    def getStream(self):
	self.clearQueue()
	self.hermes.start('stream')
	currQueue = self.hermes.player.get_queue(self.hermes.user.cursor)
	for track in currQueue:
		newItem = SongItem(track)
        	self.nowPlaying.addItem(newItem)
	self.likeButton.show()

    def like(self):
	self.hermes.like()


# Main script
app = QtGui.QApplication(sys.argv)
app.setStyleSheet('QMainWindow{background-color: darkgray;}')
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
