import os
from os import path
from PIL import Image
import numpy as np

class Theme:
	def __init__(self):
		pass

	def changeButtonColor(self, red, green, blue):
		print "New color:", red, green, blue
		buttonDir = path.join("assets", "buttons")
		for image in os.listdir(buttonDir):
			image_path = path.join(buttonDir, image)
			self.changeColor(image_path, red, green, blue)

	staticmethod = staticmethod(changeButtonColor)

	def changeColor(self, image, red2, green2, blue2):
		im = Image.open(image)
		im = im.convert('RGBA')
		data = np.array(im)

		r1, g1, b1 = 0, 0, 0 # Original value
		r1, g1, b1 = data[:,:,0], data[:,:,1], data[:,:,2]

		red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
		mask = (red == r1) & (green == g1) & (blue == b1)
		data[:,:,:3][mask] = [red2, green2, blue2]

		im = Image.fromarray(data)

		im.save(image)
