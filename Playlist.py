from Shelver import *
from PyQt4 import QtGui, QtCore
import urllib3
from SongItem import *


class Playlist(Shelver):
    def __init__(self, title, user):
        super(Playlist, self).__init__(title, user)
        self.load()

    def add(self, item):
        self.items.append(item)
        self.save()

    def clear(self):
        self.items = []
        self.save()

    #def printItems(self):
    #    for item in self.items:
    #        item.printItem()


class PlaylistItem:

    def __init__(self, other):
        self.id = other[0]
        self.artist = str(other[1].encode("utf-8"))
        self.album = str(other[2].encode("utf-8"))
        self.title = str(other[3].encode("utf-8"))
        self.tracknum = other[4]
        self.art = other[5].encode("utf-8")
        self.location = str(other[6].encode("utf-8"))
        self.text = self.title + "\ton: " + self.album + "\tby: " + self.artist

    @classmethod
    def copySong(this, copy):
        newSong = PlaylistItem(['', '', '', '', '', '','',''])
        newSong.id = copy.id
        newSong.artist = copy.artist
        newSong.album = copy.album
        newSong.title = copy.title
        newSong.art = copy.art
        newSong.tracknum = copy.tracknum
        newSong.location = copy.location
        newSong.text = newSong.title + "\ton: " + newSong.album + "\tby: " + newSong.artist
        return newSong

class TreePlaylistItem(QtGui.QTreeWidgetItem):
    def __init__(self, other, parent=None):
        super(TreePlaylistItem, self).__init__(parent)
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
        self.setText(1, self.title + "\ton: " + self.album + "\tby: " + self.artist)

    @classmethod
    def copyCtor(this, copy):
        newSong = TreePlaylistItem(['', '', '', '', '', '','',''])
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
        newSong.setText(1, newSong.title + "\ton: " + newSong.album + "\tby: " + newSong.artist)
        return newSong

    def Listver(self):
        newSong = SongItem(['', '', '', '', '', '', '' ,''])
        newSong.id = self.id
        newSong.artist = self.artist
        newSong.album = self.album
        newSong.title = self.title
        newSong.art = self.art
        newSong.tracknum = self.tracknum
        newSong.location = self.location
        newSong.setText(newSong.title + "\non: " + newSong.album + "\nby: " + newSong.artist)
        return newSong