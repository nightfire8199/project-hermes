#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib3

import functools

import vlc

from PyQt4 import QtCore, QtGui, uic
# from PyQt4.QtGui import *
from Hermes import *
from SongItem import *
from PrefsDialog import *
from Interface import *
from LoginDialog import *

import urllib3.contrib.pyopenssl
import requests

requests.packages.urllib3.disable_warnings()
urllib3.contrib.pyopenssl.inject_into_urllib3()

form_class = uic.loadUiType("ui1.ui")[0]  # Load the UI


class MyWindowClass(QtGui.QMainWindow, form_class):

    getArt = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle('Project Hermes')

        self.username = ''

        if len(sys.argv) < 2:
            login = LoginDialog(self)

            login.exec_()

            if login.result() != 1:
                print "Error: no username found"
                print "Usage: python MainWindow.py <username>"
                exit()

        else:
            self.username = str(sys.argv[1])

        self.hermes = Hermes(self.username)

        self.searchResults_Tra.addT = self.addToQueue

        self.initializeLayout()
        self.createActions()
        self.connectActions()
        self.addMenu()
        self.loadPlaylists()

        self.hermes.player.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.autoNext)
        self.hermes.player.events.event_attach(vlc.EventType.MediaPlayerTimeChanged, self.updateTracker)

    def createActions(self):
        self.quitAction = QtGui.QAction('&Quit', self)
        self.quitAction.setShortcut('Ctrl+Q')
        self.quitAction.setStatusTip('Exit application')
        self.syncAction = QtGui.QAction('&Sync', self)
        self.syncAction.setShortcut('Ctrl+S')
        self.syncAction.setStatusTip('Sync Library')
        self.prefsAction = QtGui.QAction('&Preferences', self)
        self.prefsAction.setShortcut('Ctrl+P')
        self.prefsAction.setStatusTip('Customize Hermes')
        self.playlistAction = QtGui.QAction('&New Playlist', self)
        self.playlistAction.setShortcut('Ctrl+N')
        self.playlistAction.setStatusTip('Create a new playlist')

        self.statusBar()

    def initializeLayout(self):
        self.toNP.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.toLIB.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.toPLY.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.settingsButton.setStyleSheet("background-color: rgba(0,0,0,0)")

        self.streamButton.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.likeButton.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.clearQueueButton.setStyleSheet("background-color: rgba(0,0,0,0)")

        self.theme = Theme("theme", self.hermes.user)
        self.buttonColor = QColor()
        self.prefDialog = PrefsDialog(self.theme, self)
        self.refreshUI()

        for path in self.hermes.user.watched:
            self.prefDialog.watchedList.addItem(path)

        self.likeButton.hide()

        self.playpauseButton.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.prevButton.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.nextButton.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.playingLabel.setStyleSheet("background-color: rgba(80,80,80,80); color: rgb(200,200,200)")
        self.playingLabel.setText('')
        self.nowPlaying.setIconSize(QtCore.QSize(75, 75))

        self.searchResults_Alb.setIconSize(QtCore.QSize(75, 75))
        self.searchResults_Art.setIconSize(QtCore.QSize(75, 75))

        image = QtGui.QPixmap(QtCore.QString('assets/buttons/record.png'))
        self.artView.setScaledContents(True)
        self.artView.setPixmap(image.scaled(75, 75))

    def connectActions(self):
        self.quitAction.triggered.connect(self.quitApp)
        self.searchButton.clicked.connect(self.search)
        self.searchBox.returnPressed.connect(self.search)
        self.playpauseButton.clicked.connect(self.playpause)
        self.nextButton.clicked.connect(self.playNext)
        self.prevButton.clicked.connect(self.playPrev)
        self.searchResults_Alb.itemDoubleClicked.connect(self.viewAlbum)
        self.searchResults_Art.itemDoubleClicked.connect(self.viewArtist)
        self.searchResults_Tra.itemDoubleClicked.connect(self.addToQueueAndPlay)
        self.nowPlaying.itemDoubleClicked.connect(self.playCurrent)
        self.syncAction.triggered.connect(self.sync)
        self.trackSlider.sliderReleased.connect(self.setTime)
        self.clearQueueButton.clicked.connect(self.clearQueue)
        self.streamButton.clicked.connect(self.getStream)
        self.likeButton.clicked.connect(self.like)
        self.getArt.connect(self.setAlbumArt)
        self.prefsAction.triggered.connect(self.launchPrefs)
        self.settingsButton.clicked.connect(self.launchPrefs)
        self.toNP.clicked.connect(self.showNP)
        self.toLIB.clicked.connect(self.showLIB)
        self.toPLY.clicked.connect(self.showPLY)
        self.playlistAction.triggered.connect(self.createPlaylist)
        self.playlistView.itemDoubleClicked.connect(self.addFromsPlaylistToQueue)

    def addMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.playlistAction)
        fileMenu.addAction(self.quitAction)
        toolMenu = menubar.addMenu('&Tools')
        toolMenu.addAction(self.syncAction)
        toolMenu.addAction(self.prefsAction)

        # self.searchResults_Tra.Rmenu = QtGui.QMenu(self)
        self.R_click_Tra()
        self.R_click_NP()

    def R_click_Tra(self):
        self.searchResults_Tra.Rmenu = QtGui.QMenu(self.searchResults_Tra)
        addQueue = QtGui.QAction('Add to Queue', self)
        addQueue.triggered.connect(self.addToQueue)
        addQueue.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/addtoqueue.png")))
        self.searchResults_Tra.Rmenu.addAction(addQueue)
        playmenu = self.searchResults_Tra.Rmenu.addMenu('Add to Playlist')
        for playlist in self.hermes.user.playlists:
            playAdd = QtGui.QAction(playlist.title[9:], self)
            playAdd.triggered.connect(functools.partial(self.playlistAddFromTra, playlist.title))
            playAdd.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/addtoplaylist.png")))
            playmenu.addAction(playAdd)
        newPlay = QtGui.QAction("Create New Playlist", self)
        newPlay.triggered.connect(self.createPlaylist)
        newPlay.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/playlist.png")))
        playmenu.addAction(newPlay)

    def R_click_NP(self):
        self.nowPlaying.Rmenu = QtGui.QMenu(self.nowPlaying)
        # addQueue = QtGui.QAction('Add to Queue', self)
        # addQueue.triggered.connect(self.addToQueue)
        # self.searchResults_Tra.Rmenu.addAction(addQueue)
        playmenu = self.nowPlaying.Rmenu.addMenu('Add to Playlist')
        for playlist in self.hermes.user.playlists:
            playAdd = QtGui.QAction(playlist.title[9:], self)
            playAdd.triggered.connect(functools.partial(self.playlistAddFromQueue, playlist.title))
            playAdd.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/addtoplaylist.png")))
            playmenu.addAction(playAdd)
        newPlay = QtGui.QAction("Create New Playlist", self)
        newPlay.triggered.connect(self.createPlaylist)
        newPlay.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/playlist.png")))
        playmenu.addAction(newPlay)

    def loadPlaylists(self):
        self.playlistView.clear()
        for playlist in self.hermes.user.playlists:
            newItem = QtGui.QTreeWidgetItem()
            newItem.setText(0, QtCore.QString(playlist.title[9:]))
            for track in playlist.items:
                song = TreePlaylistItem.copyCtor(track)
                song.setIcon(1, QtGui.QIcon(song.art))
                newItem.addChild(song)
            self.playlistView.addTopLevelItem(newItem)
        self.R_click_Tra()
        self.R_click_NP()

    def quitApp(self):
        self.hermes.quit()
        QtGui.qApp.quit()

    def sync(self):
        self.hermes.sync()

    def createPlaylist(self):
        dialog = QtGui.QInputDialog(self)
        dialog.setWindowTitle("Create Playlist")
        dialog.setLabelText("Enter playlist name:")
        dialog.exec_()

        if dialog.result() != 1: # dialog rejected
            return

        title = 'playlist_'+str(dialog.textValue())
        playlist = Playlist(title, self.hermes.user)
        self.hermes.user.playlists.append(playlist)
        self.loadPlaylists()

    def getStream(self):
        tracks = self.hermes.syncStream()
        self.addTrackToQueue(SongItem(tracks[0]))
        self.nowPlaying.setCurrentRow(len(self.nowPlaying) - 1)
        self.playCurrent()
        QtGui.QApplication.processEvents()
        for song in tracks[1:]:
            self.addTrackToQueue(SongItem(song))
            QtGui.QApplication.processEvents()

    def addTrackToQueue(self, song):
        song.setIcon(QtGui.QIcon(song.art))
        self.nowPlaying.addItem(song)

    def addToQueue(self, args):
        track = SongItem.copyCtor(self.searchResults_Tra.currentItem())
        track.setIcon(QtGui.QIcon(track.art))
        self.nowPlaying.addItem(track)

    def setTime(self):
        position = float(self.trackSlider.sliderPosition()) / float(self.trackSlider.maximum())
        self.hermes.player.vlc.set_position(position)

    def clearQueue(self):
        self.hermes.player.vlc.stop()
        self.likeButton.hide()
        self.playingLabel.setText('')
        image = QtGui.QPixmap(QtCore.QString('assets/buttons/record.png'))
        self.artView.setScaledContents(True)
        self.artView.setPixmap(image.scaled(75, 75))
        self.trackSlider.setValue(0)
        self.nowPlaying.clear()
        self.setToPlay()
        # self.playpause()

    def updateSearch(self, artists, albums, tracks):
        self.searchResults_Tra.clear()
        self.searchResults_Alb.clear()
        self.searchResults_Art.clear()

        if len(albums) == 0:
            self.label_3.hide()
            self.searchResults_Alb.hide()
        else:
            self.label_3.show()
            self.searchResults_Alb.show()

        if len(artists) == 0:
            self.label_4.hide()
            self.searchResults_Art.hide()
        else:
            self.label_4.show()
            self.searchResults_Art.show()

        if len(tracks) == 0:
            self.addButton.hide()
        else:
            self.addButton.show()

        for album in albums:
            newAlbum = AlbumItem(album)
            newAlbum.setIcon(QtGui.QIcon(newAlbum.art))
            self.searchResults_Alb.addItem(newAlbum)
            QtGui.QApplication.processEvents()
        for artist in artists:
            newArtist = ArtistItem(artist)
            newArtist.setIcon(QtGui.QIcon(newArtist.art))
            self.searchResults_Art.addItem(newArtist)
            QtGui.QApplication.processEvents()
        for song in tracks:
            newItem = SearchSongItem(song)
            newItem.setText(newItem.title + " - " + newItem.album + " - " + newItem.artist)
            self.searchResults_Tra.addItem(newItem)
            QtGui.QApplication.processEvents()

    def search(self):
        self.stack.setCurrentIndex(1)
        searchText = self.searchBox.text()
        [artists, albums, tracks] = self.hermes.search(searchText)
        self.updateSearch(artists, albums, tracks)

    def setAlbumArt(self):
        self.artView.setScaledContents(True)
        self.artView.setPixmap(self.nowPlaying.currentItem().art.scaled(75, 75))

    def playTrack(self, track):
        self.hermes.player.play_track(self.hermes.client.get_stream_URL(track.id, track.id[0]))

        self.getArt.emit()

        self.playingLabel.setText(QtCore.QString(track.title + ' by ' + track.artist + ' on ' + track.album))

        if track.location == 's':
            self.likeButton.show()
        else:
            self.likeButton.hide()

        self.setToPause()

    def playCurrent(self):
        self.playTrack(self.nowPlaying.currentItem())

    def setToPause(self):
        self.playpauseButton.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/pause_nofill.png")))
        self.playpauseButton.setStyleSheet("background-color: rgba(0,0,0,0)")

    def setToPlay(self):
        self.playpauseButton.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/play_fill.png")))
        self.playpauseButton.setStyleSheet("background-color: rgba(0,0,0,0)")

    def playpause(self):
        if len(self.nowPlaying) > 0:
            if self.hermes.player.vlc.is_playing():
                self.setToPlay()
                self.hermes.player.vlc.pause()
            else:
                self.setToPause()
                if self.hermes.player.vlc.get_media() is None:
                    self.playTrack(self.nowPlaying.currentItem())
                else:
                    self.hermes.player.vlc.play()
        else:
            self.setToPlay()
            self.playingLabel.setText('')
            image = QtGui.QPixmap(QtCore.QString('assets/buttons/record.png'))
            self.artView.setScaledContents(True)
            self.artView.setPixmap(image.scaled(75, 75))

    def playNext(self):
        if self.nowPlaying.currentRow() < len(self.nowPlaying):
            self.nowPlaying.setCurrentRow(self.nowPlaying.currentRow() + 1)
            self.playTrack(self.nowPlaying.currentItem())

    def playPrev(self):
        if self.nowPlaying.currentRow() > 0:
            self.nowPlaying.setCurrentRow(self.nowPlaying.currentRow() - 1)
            self.playTrack(self.nowPlaying.currentItem())

    def addToQueueAndPlay(self):
        track = SongItem.copyCtor(self.searchResults_Tra.currentItem())
        track.setIcon(QtGui.QIcon(track.art))
        self.nowPlaying.addItem(track)
        self.nowPlaying.setCurrentRow(len(self.nowPlaying) - 1)
        self.playTrack(self.nowPlaying.currentItem())

    def viewAlbum(self):
        searchText = self.searchResults_Alb.currentItem().album
        [artists, albums, tracks] = self.hermes.search_album(searchText)

        tList = []
        for song in tracks:
            tList.append(song)
        tList.sort(key=lambda x: x[4], reverse=False)

        self.updateSearch(artists, albums, tList)

    def viewArtist(self):
        searchText = self.searchResults_Art.currentItem().artist
        [artists, albums, tracks] = self.hermes.search_artist(searchText)

        tList = []
        for song in tracks:
            tList.append(song)
        tList.sort(key=lambda x: x[4], reverse=False)

        self.updateSearch(artists, albums, tList)

    def like(self):
        track = self.nowPlaying.currentItem
        if track.location == 's':
            self.hermes.client.S_client.put('/me/favorites/%d' % int(track.id[2:]))

    def updateTracker(self, args):
        self.trackSlider.setValue(int(self.hermes.player.vlc.get_position() * self.trackSlider.maximum()))

    def autoNext(self, args):
        self.hermes.player.vlc = vlc.MediaPlayer()
        self.hermes.player.events = self.hermes.player.vlc.event_manager()
        self.hermes.player.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.autoNext)
        self.hermes.player.events.event_attach(vlc.EventType.MediaPlayerTimeChanged, self.updateTracker)
        self.playNext()

    def launchPrefs(self, tab = 0):
        self.prefDialog.tabWidget.setCurrentIndex(tab)
        self.prefDialog.launch()

    def refreshUI(self):
        self.toNP.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/addtoqueue.png")))
        self.toLIB.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/search.png")))
        self.toPLY.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/playlist.png")))
        self.settingsButton.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/settings.png")))

        self.streamButton.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/soundcloud.png")))
        self.likeButton.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/like_nofill.png")))
        self.clearQueueButton.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/delete.png")))

        self.R_click_Tra()
        self.R_click_NP()

        if self.hermes.player.vlc.is_playing():
            self.playpauseButton.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/pause_nofill.png")))
        else:
            self.playpauseButton.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/play_fill.png")))
            image = QtGui.QPixmap(QtCore.QString('assets/buttons/record.png'))
            self.artView.setScaledContents(True)
            self.artView.setPixmap(image.scaled(75,75))

        self.nextButton.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/next.png")))
        self.prevButton.setIcon(QtGui.QIcon(QtCore.QString("assets/buttons/prev.png")))

        red, green, blue = self.theme.get_buttonColor()
        #print "Changing text color to: ", red, green, blue
        self.playingLabel.setStyleSheet("background-color: rgba(80,80,80,80); color: rgb("+str(red)+","+str(green)+","+str(blue)+")")

    def showNP(self):
        self.stack.setCurrentIndex(0)

    def showLIB(self):
        self.stack.setCurrentIndex(1)

    def showPLY(self):
        self.stack.setCurrentIndex(2)

    def playlistAddFromTra(self, title):
        track = self.searchResults_Tra.currentItem()
        self.hermes.playlist_add(title, track)
        self.loadPlaylists()

    def playlistAddFromQueue(self, title):
        track = self.nowPlaying.currentItem()
        self.hermes.playlist_add(title, track.searchRevert())
        self.loadPlaylists()

    def addFromsPlaylistToQueue(self, item, col):
        if col == 1:
            self.addTrackToQueue(item.Listver())
        elif col == 0:
            for indx in range(0, item.childCount()):
                self.addTrackToQueue(item.child(indx).Listver())

    def removeFromQueue(self):
        self.nowPlaying.takeItem(self.nowPlaying.currentRow)

# Main script
app = QtGui.QApplication(sys.argv)
app.setStyleSheet('QMainWindow{background-color: darkgray;}')
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
