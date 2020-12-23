import os
from scipy import misc
import numpy as np
from PIL import Image

path = 'lena.bmp'
image = Image.open(path)
image2 = image.copy()
image3 = image.copy()

w = image.size[0]
h = image.size[1]

def UpsideDown(image,w,h):
	for x in range(w):
		for y in range(h//2):
			upper = image.getpixel((x,y))
			lower = image.getpixel((x,h-1-y))
			image.putpixel((x,h-1-y),upper)
			image.putpixel((x,y),lower)
	return image

def RightSideLeft(image,w,h):
	for y in range(h):
		for x in range(w//2):
			left = image.getpixel((x,y))
			right = image.getpixel((w-1-x,y))
			image.putpixel((w-1-x,y),left)
			image.putpixel((x,y),right)
	return image


def Diagonally(image,w,h):
	for y in range(h):
		for x in range(w):
			if(x<y):
				leftdown = image.getpixel((x,y))
				rightup = image.getpixel((y,x))
				image.putpixel((y,x),leftdown)
				image.putpixel((x,y),rightup)
	return image


image.show()

imageUD = UpsideDown(image,w,h)
imageUD.show()
imageRL = RightSideLeft(image2,w,h)
imageRL.show()
imageDia = Diagonally(image3,w,h)
imageDia.show()
