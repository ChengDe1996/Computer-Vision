from PIL import Image
import numpy as np
import random 
import math

class Solution:
	def __init__(self, filter3, filter5, kernel):
		self.filter3 = filter3
		self.filter5 = filter5
		self.kernel = kernel

	def gaussian_noise(self, image, amplitude):
		pixels = image.load()
		noise_image = image.copy()
		noise_pixels = noise_image.load()
		h,w  = image.size
		for i in range(w):
			for j in range(h):
				gaussian = random.gauss(0, 1)
				noise_pixels[j, i] = int(pixels[j, i] + amplitude * gaussian)
		return noise_image

	def salt_n_pepper(self, image, prob):
		noise_image = image.copy()
		pixels = image.load()
		noise_pixels = noise_image.load()
		h, w = image.size

		for i in range(w):
			for j in range(h):
				norm = random.uniform(0, 1)
				if norm < prob:
					noise_pixels[j, i] = 0
				elif norm > (1-prob):
					noise_pixels[j,i] = 255
		return noise_image

	def box_filter(self, image, filterr):
		pixels = image.load()
		filt_image = Image.new(image.mode, image.size)
		filt_pixels = filt_image.load()
		h, w = image.size
		for i in range(w):
			for j in range(h):
				summation, count = 0, 0
				for point in filterr:
					new_i = i + point[1]
					new_j = j + point[0]
					if new_i >= 0 and new_i < w and new_j >= 0  and new_j < h:
						summation += pixels[new_j, new_i]
						count += 1
				filt_pixels[j, i] = int(summation / count)
		return filt_image

	def median_filter(self, image, filterr):
		pixels = image.load()
		filt_image = Image.new(image.mode, image.size)
		filt_pixels = filt_image.load()
		h, w = image.size
		for i in range(w):
			for j in range(h):
				tmp = []
				for point in filterr:
					new_i = i + point[1]
					new_j = j + point[0]
					if new_i >= 0 and new_i < w and new_j >= 0  and new_j < h:
						tmp.append(pixels[new_j, new_i])
				filt_pixels[j, i] = int(np.median(tmp))
		return filt_image

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

	def opening(self, image, kernel): return self.dilation(self.erosion(image, kernel), kernel)

	def closing(self, image, kernel): return self.erosion(self.dilation(image, kernel), kernel)

	def SNR(self, image, noise):
		pixels = image.load()
		noise_pixels = noise.load()
		h,w  = image.size
		ni, nn = 0, 0

		for i in range(w):
			for j in range(h):
				ni += pixels[j, i] / 255
				nn += (noise_pixels[j, i] - pixels[j, i ]) / 255
		ni /= h * w
		nn /= h * w
		vs, vn = 0, 0
		for i in range(w):
			for j in range(h):
				vs += ((pixels[j, i] / 255) - ni) ** 2
				vn += (((noise_pixels[j, i] - pixels[j, i]) / 255) - nn) ** 2
		vs /= h * w
		vn /= h * w
		snr = 20 * math.log10(math.sqrt(vs) / math.sqrt(vn))
		return snr

	def image_process(self, image, noise, name):
		noise.save(name + '.bmp')
		print(name, self.SNR(image, noise))

		box_filter3 = self.box_filter(noise, self.filter3)
		box_filter3.save(name + 'box filter 3*3.bmp')
		print(name + ' box filter 3*3:', self.SNR(image, box_filter3))

		box_filter5 = self.box_filter(noise, self.filter5)
		box_filter5.save(name + 'box filter 5*5.bmp')
		print(name + ' box filter 5*5:', self.SNR(image, box_filter5))

		median_filter3 = self.median_filter(noise, self.filter3)
		median_filter3.save(name + 'median filter 3*3.bmp')
		print(name + ' median filter 3*3:', self.SNR(image, median_filter3))

		median_filter5 = self.median_filter(noise, self.filter5)
		median_filter5.save(name + 'median filter 5*5.bmp')
		print(name + ' median filter 5*5: ', self.SNR(image, median_filter5))

		open_close = self.closing(self.opening(noise, self.kernel), self.kernel)
		open_close.save(name + 'open_close.bmp')
		print(name + ' open close: ', self.SNR(image, open_close))

		close_open = self.opening(self.closing(noise, self.kernel), self.kernel)
		close_open.save(name + 'close_open.bmp')
		print(name + ' close_open: ', self.SNR(image, close_open))

		print(' ')

def hw8(filter_3, filter_5, kernel, lena_path):
	sol = Solution(filter_3, filter_5, kernel)
	lena = Image.open(lena_path)
	guassian_noise_10 = sol.gaussian_noise(lena, 10)
	guassian_noise_30 = sol.gaussian_noise(lena, 30)

	salt_n_pepper_01 = sol.salt_n_pepper(lena, 0.1)
	salt_n_pepper_005 = sol.salt_n_pepper(lena, 0.05)

	sol.image_process(lena, guassian_noise_10, 'guassian_noise_10')
	sol.image_process(lena, guassian_noise_30, 'guassian_noise_30')
	sol.image_process(lena, salt_n_pepper_01, 'salt_n_pepper_01')
	sol.image_process(lena, salt_n_pepper_005, 'salt_n_pepper_005')

if __name__ == '__main__':
	
	path = 'lena.bmp'

	filter_3 = [(-1, -1), (0, -1), (1, -1),
				 (-1,  0), (0,  0), (1,  0),
				 (-1,  1), (0,  1), (1,  1)]

	filter_5 = [(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
				 (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
				 (-2,  0), (-1,  0), (0,  0), (1,  0), (2,  0),
				 (-2,  1), (-1,  1), (0,  1), (1,  1), (2,  1),
				 (-2,  2), (-1,  2), (0,  2), (1,  2), (2,  2)]

	kernel = [(-1, -2), (0, -2), (1, -2),
			  (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
			  (-2,  0), (-1,  0), (0,  0), (1,  0), (2,  0),
			  (-2,  1), (-1,  1), (0,  1), (1,  1), (2,  1),
			  (-1,  2), (0,  2), (1,  2)]

	hw8(filter_3, filter_5, kernel, path)