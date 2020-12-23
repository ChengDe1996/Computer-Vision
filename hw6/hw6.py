from PIL import Image
import numpy as np

class Solution:
	def __init__(self):
		pass

	def binarization(self, image):
		pixels = image.load()
		bin_image = Image.new('1', image.size)
		bin_pixels = bin_image.load()
		h, w = image.size
		for i in range(h):
			for j in range(w):
				if pixels[i, j] >= 128:
					bin_pixels[i, j] = 1
				else:
					bin_pixels[i, j] = 0

		return bin_image

	def down_sampling(self, image, origin_size, target_size):
		pixels = image.load()
		new_image = Image.new(image.mode, (target_size, target_size))
		new_pixels = new_image.load()
		for i in range(target_size):
			for j in range(target_size):
				new_pixels[i, j] = pixels[i * int(origin_size/target_size), j * int(origin_size/target_size)]
		return new_image


	def h(self, b, c, d, e):
		if b != c: return 's'
		if b == d and b == e: return 'r'
		return 'q'

	def valid(self, new_x, new_y, h, w):
		return new_x >= 0 and new_x < h and new_y >= 0 and new_y < w

	def check(self, image, cor, x, y):
		h, w = image.size
		pixels = image.load()
		new_x, new_y = x + cor[0], y + cor[1]
		if self.valid(new_x, new_y, h, w): return pixels[new_x, new_y]
		return 0

	def Yokoi_num(self, image, corners):
		pixels = image.load()
		res = []
		h, w = image.size
		for y in range(w):
			row = []
			for x in range(h):
				if pixels[x, y] == 0:
					row.append(' ')
					continue
				else:
					temp = []
					for cor in corners:
						b = pixels[x, y]
						c, d, e = 0, 0, 0
						c = self.check(image, cor[0], x, y)
						d = self.check(image, cor[1], x, y)
						e = self.check(image, cor[2], x, y)
						temp.append(self.h(b,c,d,e))
					if temp.count('r') == 4:
						row.append('5')
					else:
						if temp.count('q') == 0:
							row.append(' ')
						else:
							row.append(str(temp.count('q')))
			res.append(row)
		return np.array(res)

	def save(self, save_name, res):
		file = open(save_name, "w")
		with open(save_name, "w") as file:
			for i in range(res.shape[0]):
				for j in range(res.shape[1]):
					file.write(res[i, j])
				file.write('\n')


	def problem1(self, path, out_file, corners):
		image = Image.open(path)
		down_sampleing_image = self.down_sampling(image, 512, 64)
		# down_sampleing_image.save('down_sampling.bmp')
		bin_image = self.binarization(down_sampleing_image)
		# bin_image.save('bin_image.bmp')
		yokoi = self.Yokoi_num(bin_image, corners)
		self.save(out_file, yokoi)



if __name__ == '__main__':
	corners = [ [( 1,  0), ( 1, -1), ( 0, -1)], 
				[( 0, -1), (-1, -1), (-1,  0)], 
				[(-1,  0), (-1,  1), ( 0,  1)], 
				[( 0,  1), ( 1,  1), ( 1,  0)] ]
	path = 'lena.bmp'
	out_file = 'lena_yokoi.txt'
	Solution().problem1(path, out_file, corners)







