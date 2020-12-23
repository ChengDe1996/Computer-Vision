from PIL import Image
import numpy as np

class Solution:
	def __init__(self, corners, neighbors):
		self.corners = corners
		self.neighbors = neighbors

	def down_sampling(self, image, target_size):
		pixels = image.load()
		new_image = Image.new(image.mode, (target_size, target_size))
		new_pixels = new_image.load()
		for i in range(target_size):
			for j in range(target_size):
				new_pixels[i, j] = pixels[i * int(image.size[0]/target_size), j * int(image.size[0]/target_size)]
		return new_image

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

	def h_yokoi(self, b, c, d, e):
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

	def Yokoi(self, image):
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
					for cor in self.corners:
						b = pixels[x, y]
						c, d, e = 0, 0, 0
						c = self.check(image, cor[0], x, y)
						d = self.check(image, cor[1], x, y)
						e = self.check(image, cor[2], x, y)
						temp.append(self.h_yokoi(b,c,d,e))
					if temp.count('r') == 4:
						row.append('5')
					else:
						if temp.count('q') == 0:
							row.append(' ')
						else:
							row.append(str(temp.count('q')))
			res.append(row)
		return np.array(res)


	def pair_relationship(self, yokoi, image):
		marked = Image.new('1', image.size)
		marked_pixels = marked.load()
		h, w  = image.size
		for y in range(h):
			for x in range(w):
				if yokoi[y][x] == '1':
					booling = False
					for neighbor in self.neighbors:
						new_x, new_y = x + neighbor[0], y + neighbor[1]
						if self.valid(new_x, new_y, h, w):
							if yokoi[new_y][new_x] == '1':
								booling = True
								break
					if booling:
						marked_pixels[x,y] = 1
		return marked

	def h_shrink(self, b, c, d, e):
		if (b != d or b !=e) and b == c:
			return 1
		return 0

	def connected_shrink(self, image, marked):
		pixels = image.load()
		marked_pixels = marked.load()
		res = image.copy()
		res_pixels = res.load()
		h, w = image.size
		for y in range(w):
			for x in range(h):
				if marked_pixels[x, y] == 1:
					temp = []
					for cor in self.corners:
						b = res_pixels[x, y]
						c, d, e = 0, 0, 0
						c = self.check(res, cor[0], x, y)
						d = self.check(res, cor[1], x, y)
						e = self.check(res, cor[2], x, y)
						temp.append(self.h_shrink(b, c, d, e))
					if temp.count(1) == 1:
						res_pixels[x, y] = 0
		return res

	def thinning(self, image):
		while True:
			yokoi = self.Yokoi(image)
			marked = self.pair_relationship(yokoi, image)
			thinning = self.connected_shrink(image, marked)
			if image != thinning:
				image = thinning
			else:
				break
		return thinning

	def problem1(self, path, outfile):
		image = Image.open(path)
		down_sampled = self.down_sampling(image, 64)
		bin_image = self.binarization(down_sampled)
		thined = self.thinning(bin_image)
		print(thined)
		thined.save(outfile)




if __name__ == '__main__':
	corners = [ [( 1,  0), ( 1, -1), ( 0, -1)], 
				[( 0, -1), (-1, -1), (-1,  0)], 
				[(-1,  0), (-1,  1), ( 0,  1)], 
				[( 0,  1), ( 1,  1), ( 1,  0)] ]
	neighbors = [(1, 0), (0, -1), (-1, 0), (0, 1)]
	sol = Solution(corners, neighbors)
	path = 'lena.bmp'
	out_file = 'lena_thinning.bmp'
	sol.problem1(path, out_file)
