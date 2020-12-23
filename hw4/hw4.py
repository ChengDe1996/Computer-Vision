import numpy as np
from PIL import Image, ImageDraw
# import matplotlib.pyplot as plt

class Solutions():
	def __init__(self, kernel, ker_j, ker_k):
		self.kernel = kernel
		self.ker_j = ker_j
		self.ker_k = ker_k

	def binarization(self, path):
		img = Image.open("lena.bmp")
		img_pixel = img.load()
		binary_img = Image.new('1', img.size)
		binary_img_pixel = binary_img.load()

		for x in range(img.size[0]):
			for y in range(img.size[1]):
				if img_pixel[x,y] >= 128:
					binary_img_pixel[x,y] = 1
				else:
					binary_img_pixel[x,y] = 0
		return binary_img

	def dilation(self, bin_image, kernel):
		dilation_image = Image.new('1', bin_image.size)
		h, w = bin_image.size
		pixels = bin_image.load()
		new_pixels = dilation_image.load()
		for i in range(h):
			for j in range(w):
				for point in kernel:
					new_i = i + point[0]
					new_j = j + point[1]
					if new_i >= 0 and new_i < h and new_j >= 0 and new_j < w:
						if pixels[new_i, new_j] == 1:
							new_pixels[i, j] = 1
							break
		return dilation_image

	def erosion(self, bin_image, kernel):
		erosion_image = Image.new('1', bin_image.size, color = 1)
		h, w = bin_image.size
		pixels = bin_image.load()
		new_pixels = erosion_image.load()
		for i in range(h):
			for j in range(w):
				for point in kernel:
					new_i = i + point[0]
					new_j = j + point[1]
					if new_i >= 0 and new_i < h and new_j >= 0 and new_j < w:
						if pixels[new_i, new_j] != 1:
							new_pixels[i, j] = 0
							break
		return erosion_image

	def opening(self, bin_image):
		erosion_image = self.erosion(bin_image, self.kernel)
		opening_image = self.dilation(erosion_image, self.kernel)
		return opening_image

	def closing(self, bin_image):
		dilation_image = self.dilation(bin_image, self.kernel)
		closing_image = self.erosion(dilation_image, self.kernel)
		return closing_image

	def complement(sefl, bin_image):
		complement_image = Image.new('1', bin_image.size)
		complement_pixels = complement_image.load()
		binary_pixels = bin_image.load()
		h, w = bin_image.size
		for i in range(h):
			for j in range(w):
				complement_pixels[i,j] = 1 - binary_pixels[i,j]
		return complement_image

	def intersection(self, image1, image2):
		pixels1 = image1.load()
		pixels2 = image2.load()
		intersect_image = Image.new('1', image1.size)
		intersect_pixels = intersect_image.load()
		h, w = intersect_image.size
		for i in range(h):
			for j in range(w):
				intersect_pixels[i, j] = pixels1[i, j] & pixels2[i, j]
		return intersect_image

	def hitandmiss(self, bin_image):
		complement_image = self.complement(bin_image)
		pixels = bin_image.load()
		hit = self.erosion(bin_image, self.ker_j)
		miss = self.erosion(complement_image, self.ker_k)
		return self.intersection(hit, miss)

	def save_image(self, image, name):
		image.save(name)

	def question1(self, path, save_name):
		# deliation
		bin_image = self.binarization(path)
		dilation_image = self.dilation(bin_image, self.kernel)
		self.save_image(dilation_image, save_name)

	def question2(self, path, save_name):
		# Erosion
		bin_image = self.binarization(path)
		erosion_image = self.erosion(bin_image, self.kernel)
		self.save_image(erosion_image, save_name)

	def question3(self, path, save_name):
		# Opening
		bin_image = self.binarization(path)
		opening_image = self.opening(bin_image)
		self.save_image(opening_image, save_name)

	def question4(self, path, save_name):
		# Closing
		bin_image = self.binarization(path)
		closing_image = self.closing(bin_image)
		self.save_image(closing_image, save_name)	

	def question5(self, path, save_name):
		# hit and miss
		bin_image = self.binarization(path)
		hit_and_miss_image = self.hitandmiss(bin_image)
		self.save_image(hit_and_miss_image, save_name)



if __name__ == '__main__':
	kernel_35553 = [(1,2), (0,2), (-1,2), (-2,1), (-1,1), (0,1), (1,1), (2,1), (-2,  0), (-1,  0), (0,  0), (1,  0), (2,  0), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (-1, -2), (0, -2), (1, -2)]
	# ker_j = [(0,-1), (0,0), (-1, 0)]
	# ker_k = [(0,1), (1,0), (1,1)]
	ker_j = [(-1, 0), (0, 0), (0, 1)]
	ker_k = [(0, -1), (1, -1), (1, 0)]
	sol = Solutions(kernel_35553, ker_j, ker_k)
	sol.question1('lena.bmp', 'dilation_lena.bmp')
	sol.question2('lena.bmp', 'erosion_lena.bmp')
	sol.question3('lena.bmp', 'opening_lena.bmp')
	sol.question4('lena.bmp', 'closing_lena.bmp')
	sol.question5('lena.bmp', 'hit&miss_lena.bmp')