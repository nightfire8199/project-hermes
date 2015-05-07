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
        self.buttonColorButton.clicked.connect(self.buttonColorPicker)
        self.load()

    def load(self):
        # self.theme.load() # done in ctor in Theme.py
        pass

    def refreshUI(self):
        self.buttonColorLabel.setText('')
        print self.buttonColorLabel.text()
        red, green, blue = self.theme.get_buttonColor()
        # self.buttonColorLabel.setStyleSheet("background-color: rgb("+str(red)+","+str(green)+","+str(blue)+")")
        print "Refreshing Prefs UI:", red, green, blue
        self.buttonColorLabel.setStyleSheet("background-color: rgb(150, 0, 0, 80)")
        # self.buttonColorLabel.setStyleSheet("background-color: rgba(200,200,200,200); color: rgb("+str(red)+","+str(green)+","+str(blue)+")")

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
        print "ref>>>>>>"
        self.refreshUI()


