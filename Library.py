from Shelver import *
from PyQt4 import QtGui, QtCore


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
