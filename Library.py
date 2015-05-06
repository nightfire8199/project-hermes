
from Shelver import *

import shelve
from os import path


class Playlist(Shelver):

    def __init__(self, title, user):
        # Shelver.__init__(title, user)
        super(Playlist, self).__init__(title, user)
        self.load()

    def add(self, sid, streamid, location):
        self.items.append(PlaylistItem(sid, streamid, location))
        self.save()

    def clear(self):
        self.items = []
        self.save()

    def printItems(self):
        for item in self.items:
            item.printItem()


class PlaylistItem:

    def __init__(self, sid, streamid, location):
        self.id = sid
        self.streamid = streamid
        self.location = location

    def printItem(self):
        print self.id, self.streamid, self.location
