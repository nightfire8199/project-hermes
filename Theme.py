from Shelver import *

import os
from os import path
from PIL import Image
import numpy as np


class Theme(Shelver):
    def __init__(self, title, user):
        super(Theme, self).__init__(title, user)
        self.buttonColor = []
        self.buttonColor_id = 0
        self.load()

    def save(self):
        self.items = [
            self.buttonColor
        ]
        super(Theme, self).save()

    def load(self):
        super(Theme, self).load()
        if len(self.items[0]) == 0:
            self.buttonColor = [255, 255, 255]
            return

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

        r1, g1, b1 = data[:,:,0], data[:,:,1], data[:,:,2] # Original value

        red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
        mask = (red == r1) & (green == g1) & (blue == b1)
        data[:, :, :3][mask] = [red2, green2, blue2]

        self.buttonColor = [red2, green2, blue2]

        im = Image.fromarray(data)
        im.save(image)

