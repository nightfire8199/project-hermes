from Theme import *

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *

form_class = uic.loadUiType("prefs.ui")[0]                 # Load the UI

class PrefsDialog(QDialog, form_class):
    def __init__(self, theme, parent):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.theme = theme
        self.setupUi(self)
        self.setModal(True)
        self.buttonColorLabel.setText('')
        self.buttonColorButton.clicked.connect(self.buttonColorPicker)
        self.addPath.clicked.connect(self.addWatched)
        self.removePath.clicked.connect(self.removeWatched)
        self.load()

    def load(self):
        # self.theme.load() # done in ctor in Theme.py
        pass

    def addWatched(self):
        dialog = QFileDialog(self, "Select a directory to watch", )
        dialog.setFileMode(QFileDialog.Directory)
        dialog.exec_()

        # dialog rejected
        if dialog.result() != 1:
            return

        directory = dialog.directory().absolutePath()
        added = self.parent.hermes.user.add_watched(directory)
        if added:
            self.watchedList.addItem(directory)

    def removeWatched(self):
        selected = self.watchedList.currentRow()
        directory = str(self.watchedList.item(selected).text())
        self.parent.hermes.user.remove_watched(directory)
        self.watchedList.takeItem(selected)

    def refreshUI(self):
        red, green, blue = self.theme.get_buttonColor()
        self.buttonColorLabel.setStyleSheet("background-color: rgb("+str(red)+","+str(green)+","+str(blue)+")")
        print "Refreshing Prefs UI:", red, green, blue

    def launch(self):
        self.refreshUI()
        self.exec_()

    def buttonColorPicker(self):
        print "Launch color picker"
        colorDialog = QColorDialog(self)
        colorDialog.exec_()

        if colorDialog.result() != 1: # dialog rejected
            return

        color = colorDialog.selectedColor()
        self.theme.changeButtonColor(color.red(), color.green(), color.blue())
        self.parent.refreshUI()
        self.refreshUI()


