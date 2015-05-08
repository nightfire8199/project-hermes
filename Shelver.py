from PyQt4 import QtGui, QtCore

import shelve
from os import path


class Shelver(object):
    def __init__(self, title, user):
        self.title = title
        self.user = user
        self.items = []

    def get_shelve(self):
        return path.join(self.user.userdata_path, self.title)

    def save(self):
        shelf = shelve.open(self.get_shelve(), 'c')
        shelf[self.title] = self.items
        shelf.close()

    def load(self):
        if not path.exists(self.get_shelve()):
            self.save()
            return
        shelf = shelve.open(self.get_shelve(), 'r')
        self.items = shelf[self.title]
        shelf.close()

