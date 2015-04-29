from Theme import *

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *

form_class = uic.loadUiType("prefs.ui")[0]                 # Load the UI

class PrefsDialog(QDialog, form_class):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(True)
        self.buttonColorButton.clicked.connect(self.buttonColorPicker)
        self.exec_()

    def buttonColorPicker(self):
        print "Launch color picker"
        colorDialog = QColorDialog(self)
        colorDialog.exec_()

        if colorDialog.result() != 1: # dialog rejected
        	return

        color = colorDialog.selectedColor()
        theme = Theme()
        theme.changeButtonColor(color.red(), color.green(), color.blue())
