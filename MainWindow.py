#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *
from Hermes import *
from SongItem import *

form_class = uic.loadUiType("ui1.ui")[0]                 # Load the UI

class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle('Project Hermes')

        self.playpauseButton.setText('')
        self.playpauseButton.setStyleSheet("background-image: url(assets/play_fill_white.png); background-color: rgba(0,0,0,0)")
        self.prevButton.setText('')
        self.prevButton.setStyleSheet("background-image: url(assets/prev_white.png); background-color: rgba(0,0,0,0)")
        self.nextButton.setText('')
        self.nextButton.setStyleSheet("background-image: url(assets/next_white.png); background-color: rgba(0,0,0,0)")
        self.playingLabel.setText('')
        self.playingLabel.setStyleSheet("background-color: rgba(80,80,80,80); color: rgb(200,200,200)")

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
	self.playpauseButton.clicked.connect(self.playpause)
	self.nextButton.clicked.connect(self.playnext)
	self.prevButton.clicked.connect(self.playprev)
     	self.searchResults_Alb.itemDoubleClicked.connect(self.viewAlbum)
	self.searchResults_Art.itemDoubleClicked.connect(self.viewArtist)
        self.searchResults_Tra.itemDoubleClicked.connect(self.addToQueueAndPlay)
	self.nowPlaying.currentRowChanged.connect(self.playSelected)
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
        self.nowPlaying.setCurrentRow(self.nowPlaying.count()-1)

    def playSelected(self):
	if len(self.hermes.player.Queue.items) > 0:
		selected = self.nowPlaying.currentItem()
		self.hermes.play(selected.id)
		self.playingLabel.setText("   "+selected.title+" by "+selected.artist+" on "+selected.album)
		self.playpause() 

    def addToQueue(self):
        selected = self.searchResults_Tra.currentItem()
        self.hermes.add(selected.id)
        newItem = SongItem.copyCtor(selected)

        self.nowPlaying.addItem(newItem)
        return newItem

    def clearQueue(self):
	self.hermes.player.vlc.stop()
	self.likeButton.hide()
	self.playingLabel.setText('')
	self.trackSlider.setValue(0)
        self.hermes.player.clear_queue()
        self.nowPlaying.clear()
	self.playpause()

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
	if len(self.hermes.player.Queue.items) > 0:
		self.hermes.player.pos = self.nowPlaying.currentRow()
		if self.hermes.player.vlc.is_playing():
			self.playpauseButton.setStyleSheet("background-image: url(assets/play_fill_white.png); background-color: rgba(0,0,0,0)")
			self.hermes.player.vlc.pause()
		else:
			self.playpauseButton.setStyleSheet("background-image: url(assets/pause_nofill_white.png); background-color: rgba(0,0,0,0)")
			if self.hermes.player.vlc.get_media() == None:
				self.hermes.player.play_queue(self.nowPlaying.currentRow())
			else:
				self.hermes.player.vlc.play()
	else:
		self.playpauseButton.setStyleSheet("background-image: url(assets/play_fill_white.png); background-color: rgba(0,0,0,0)")
		self.playingLabel.setText('')

    def playnext(self):
	if self.hermes.player.pos + 1 < self.nowPlaying.count():
		self.nowPlaying.setCurrentRow(self.hermes.player.pos + 1)

    def playprev(self):
	if self.hermes.player.pos - 1 >= 0:
		self.nowPlaying.setCurrentRow(self.hermes.player.pos - 1)

    def getStream(self):
	self.clearQueue()
	self.hermes.start('stream')
	currQueue = self.hermes.player.get_queue(self.hermes.user.cursor)
	for track in currQueue:
		newItem = SongItem(track)
        	self.nowPlaying.addItem(newItem)
	self.likeButton.show()
	self.nowPlaying.setCurrentRow(0)

    def like(self):
	self.hermes.like()



# Main script
app = QtGui.QApplication(sys.argv)
app.setStyleSheet('QMainWindow{background-color: darkgray;}')
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
