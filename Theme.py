from Shelver import *

import os
from os import path
from PIL import Image
import numpy as np
from enum import Enum


class CssTheme(Enum):
    DARK = 0
    LIGHT = 1
    CUSTOM = 2


class Theme(Shelver):

    def __init__(self, title, user):
        super(Theme, self).__init__(title, user)
        self.cssTheme_id = 0
        self.cssTheme = CssTheme.DARK
        self.customCssPath_id = 1
        self.customCssPath = ''
        self.buttonColor_id = 2
        self.buttonColor = [255, 255, 255]
        self.load()

    def save(self):
        self.items = [
            self.cssTheme,
            self.customCssPath,
            self.buttonColor
        ]
        super(Theme, self).save()

    def load(self):
        super(Theme, self).load()
        print self.items
        if len(self.items[self.buttonColor_id]) == 0:
            self.cssTheme = CssTheme.DARK
            self.buttonColor = [255, 255, 255]
            return

        self.cssTheme = self.items[self.cssTheme_id]
        self.customCssPath = self.items[self.customCssPath_id]
        self.buttonColor = self.items[self.buttonColor_id]

    def get_buttonColor(self):
        return self.buttonColor[0], self.buttonColor[1], self.buttonColor[2]

    def changeButtonColor(self, red, green, blue):
        print "New color:", red, green, blue
        buttonDir = path.join("assets", "buttons")
        for image in os.listdir(buttonDir):
            image_path = path.join(buttonDir, image)
            self.changeColor(image_path, red, green, blue)
        self.save()

    def changeColor(self, image, red2, green2, blue2):
        im = Image.open(image)
        im = im.convert('RGBA')
        data = np.array(im)

        r1, g1, b1 = data[:, :, 0], data[:, :, 1], data[:, :, 2]  # Original value

        red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
        mask = (red == r1) & (green == g1) & (blue == b1)
        data[:, :, :3][mask] = [red2, green2, blue2]

        self.buttonColor = [red2, green2, blue2]

        im = Image.fromarray(data)
        im.save(image)


