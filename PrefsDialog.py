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
        self.setFixedSize(self.width(), self.height())
        self.connectActions()

        if self.theme.cssTheme == CssTheme.DARK:
            self.setThemeDark()
            self.darkTheme.toggle()
        elif self.theme.cssTheme == CssTheme.LIGHT:
            self.setThemeLight()
            self.lightTheme.toggle()
        elif self.theme.cssTheme == CssTheme.CUSTOM:
            self.setThemeCustom(True)
            self.customTheme.toggle()

        self.load()

    def connectActions(self):
        self.buttonColorLabel.setText('')
        self.buttonColorButton.clicked.connect(self.buttonColorPicker)
        self.addPath.clicked.connect(self.addWatched)
        self.removePath.clicked.connect(self.removeWatched)
        self.darkTheme.clicked.connect(self.setThemeDark)
        self.lightTheme.clicked.connect(self.setThemeLight)
        self.customTheme.clicked.connect(self.setNewCustomTheme)

    def setThemeDark(self):
        print "Theme: dark"
        self.theme.cssTheme = CssTheme.DARK
        self.setTheme('dark.css')

    def setThemeLight(self):
        print "Theme: light"
        self.theme.cssTheme = CssTheme.LIGHT
        self.setTheme('light.css')

    def setNewCustomTheme(self):
        self.setThemeCustom(False)

    def setThemeCustom(self, load_file):
        print "Theme: custom"

        old_theme = self.theme.cssTheme
        self.theme.cssTheme = CssTheme.CUSTOM

        if load_file and len(self.theme.customCssPath) > 0:
            self.setTheme(self.theme.customCssPath)
            return

        dialog = QFileDialog(self, "Select a PyQt4 CSS File to Use", "./", "*.css")
        dialog.exec_()

        # dialog rejected
        if dialog.result() != 1:
            if old_theme == CssTheme.DARK:
                self.darkTheme.toggle()
            elif old_theme == CssTheme.LIGHT:
                self.lightTheme.toggle()
            return

        print "Selected file:", str(dialog.selectedFiles()[0])
        self.theme.customCssPath = str(dialog.selectedFiles()[0])
        self.setTheme(self.theme.customCssPath)

    def setTheme(self, themeName):
        with open(themeName, 'r') as content_file:
            appStyle = content_file.read()
        self.parent.setStyleSheet(appStyle)
        self.theme.save()

    def load(self):
        # self.theme.load() # done in ctor in Theme.py
        pass

    def addWatched(self):
        dialog = QFileDialog(self, "Select a Directory to Watch", "./", "*.css")
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
        colorDialog = QColorDialog(self)
        colorDialog.exec_()

        if colorDialog.result() != 1:  # dialog rejected
            return

        color = colorDialog.selectedColor()
        self.theme.changeButtonColor(color.red(), color.green(), color.blue())
        self.parent.refreshUI()
        self.refreshUI()
