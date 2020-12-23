import numpy as np
from PIL import Image, ImageDraw

class Solutions():
	def __init__(self, kernel):
		self.kernel = kernel

	def dilation(self, image, kernel):
		dilation_image = Image.new(image.mode, image.size, color = 0)
		h, w = image.size
		pixels = image.load()
		new_pixels = dilation_image.load()
		for i in range(h):
			for j in range(w):
				max_value = 0
				for point in kernel:
					new_i = i + point[0]
					new_j = j + point[1]
					if new_i >= 0 and new_i < h and new_j >= 0 and new_j < w:
						if pixels[new_i, new_j] > max_value:
							max_value = pixels[new_i, new_j]
				new_pixels[i, j] = max_value
		return dilation_image

	def erosion(self, image, kernel):
		erosion_image = Image.new(image.mode, image.size, color = 255)
		h, w = image.size
		pixels = image.load()
		new_pixels = erosion_image.load()
		for i in range(h):
			for j in range(w):
				min_value = 255
				for point in kernel:
					new_i = i + point[0]
					new_j = j + point[1]
					if new_i >= 0 and new_i < h and new_j >= 0 and new_j < w:
						if pixels[new_i, new_j] < min_value:
							min_value =  pixels[new_i, new_j]
				new_pixels[i, j] = min_value
							
		return erosion_image

	def opening(self, image):
		erosion_image = self.erosion(image, self.kernel)
		opening_image = self.dilation(erosion_image, self.kernel)
		return opening_image

	def closing(self, image):
		dilation_image = self.dilation(image, self.kernel)
		closing_image = self.erosion(dilation_image, self.kernel)
		return closing_image


	def save_image(self, image, name):
		image.save(name)

	def question1(self, path, save_name):
		# deliation
		image = Image.open(path)
		dilation_image = self.dilation(image, self.kernel)
		self.save_image(dilation_image, save_name)

	def question2(self, path, save_name):
		# Erosion
		image = Image.open(path)
		erosion_image = self.erosion(image, self.kernel)
		self.save_image(erosion_image, save_name)

	def question3(self, path, save_name):
		# Opening
		image = Image.open(path)
		opening_image = self.opening(image)
		self.save_image(opening_image, save_name)

	def question4(self, path, save_name):
		# Closing
		image = Image.open(path)
		closing_image = self.closing(image)
		self.save_image(closing_image, save_name)	




if __name__ == '__main__':
	kernel_35553 = [(1,2), (0,2), (-1,2), (-2,1), (-1,1), (0,1), (1,1), (2,1), (-2,  0), (-1,  0), (0,  0), (1,  0), (2,  0), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (-1, -2), (0, -2), (1, -2)]

	sol = Solutions(kernel_35553)
	sol.question1('lena.bmp', 'dilation_lena.bmp')
	sol.question2('lena.bmp', 'erosion_lena.bmp')
	sol.question3('lena.bmp', 'opening_lena.bmp')
	sol.question4('lena.bmp', 'closing_lena.bmp')


