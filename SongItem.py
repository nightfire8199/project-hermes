from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import QUrl
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
import urllib3
import types

import urllib3.contrib.pyopenssl
import requests

requests.packages.urllib3.disable_warnings()
urllib3.contrib.pyopenssl.inject_into_urllib3()


class SearchSongItem(QtGui.QListWidgetItem):
    def __init__(self, other, parent=None):
        super(SearchSongItem, self).__init__(parent)
        self.id = other[0]
        self.artist = str(other[1].encode("utf-8"))
        self.album = str(other[2].encode("utf-8"))
        self.title = str(other[3].encode("utf-8"))
        self.tracknum = other[4]
        self.art = other[5].encode("utf-8")
        self.location = str(other[6].encode("utf-8"))
        self.setText(self.title + "\non: " + self.album + "\nby: " + self.artist)

    @classmethod
    def copyCtor(this, copy):
        newSong = SearchSongItem(['', '', '', '', '', '','',''])
        newSong.id = copy.id
        newSong.artist = copy.artist
        newSong.album = copy.album
        newSong.title = copy.title
        newSong.art = copy.art
        newSong.tracknum = copy.tracknum
        newSong.location = copy.location
        newSong.setText(newSong.title + "\non: " + newSong.album + "\nby: " + newSong.artist)
        return newSong


class SongItem(QtGui.QListWidgetItem):
    def __init__(self, other, parent=None):
        super(SongItem, self).__init__(parent)
        self.id = other[0]
        self.artist = str(other[1].encode("utf-8"))
        self.album = str(other[2].encode("utf-8"))
        self.title = str(other[3].encode("utf-8"))
        self.tracknum = other[4]
        self.art = QtGui.QPixmap(QtCore.QString('assets/record.png'))
        if not (other[5] == '' or isinstance(other[5], types.NoneType)):
            data = urllib3.PoolManager().request("GET", str(other[5].encode("utf-8")))
            self.art = QtGui.QPixmap()
            self.art.loadFromData(data.data)
        self.location = str(other[6].encode("utf-8"))
        self.setText(self.title + "\non: " + self.album + "\nby: " + self.artist)

    @classmethod
    def copyCtor(this, copy):
        newSong = SongItem(['', '', '', '', '', '','',''])
        newSong.id = copy.id
        newSong.artist = copy.artist
        newSong.album = copy.album
        newSong.title = copy.title
        newSong.art = QtGui.QPixmap(QtCore.QString('assets/record.png'))
        if copy.art != '':
            data = urllib3.PoolManager().request("GET", copy.art)
            newSong.art = QtGui.QPixmap()
            newSong.art.loadFromData(data.data)
        newSong.tracknum = copy.tracknum
        newSong.location = copy.location
        newSong.setText(newSong.title + "\non: " + newSong.album + "\nby: " + newSong.artist)
        return newSong


class ArtistItem(QtGui.QListWidgetItem):
    def __init__(self, other, parent=None):
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
    def __init__(self, other, parent=None):
        super(AlbumItem, self).__init__(parent)
        self.artist = str(other[1].encode("utf-8"))
        self.album = str(other[0].encode("utf-8"))
        self.setText(self.album + "   -   " + self.artist)

    @classmethod
    def copyCtor(this, copy):
        newAlbum = AlbumItem(['', ''])
        newAlbum.artist = copy.artist
        newAlbum.album = copy.album
        newAlbum.setText(newAlbum.album + "\nby: " + newAlbum.artist)
        return newAlbum


class TableSongItem(QtGui.QTableWidgetItem):
    def __init__(self, other, parent=None):
        super(SongItem, self).__init__(parent)
        self.id = other[0]
        self.setText(str(other[1]) + "  -  " + str(other[2]) + "  -  " + str(other[3]))
