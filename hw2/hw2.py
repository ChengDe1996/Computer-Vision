import numpy as np
import argparse
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--lena', default= 'lena.bmp')
	args = parser.parse_args()

	return args

class Question1():
	def run(self, threshold, path):
		image = Image.open(path)
		h, w = image.size
		for i in range(h):
			for j in range(w):
				value = image.getpixel((i, j))
				value = 255 if value >= threshold else 0
				image.putpixel((i,j), value)
		image.save('binary.bmp')

class Question2():
	def run(self, path, dim):
		his = np.zeros(dim)
		image = Image.open(path)
		h, w = image.size
		for i in range(h):
			for j in range(w):
				val = image.getpixel((i, j))
				his[val] += 1
		np.savetxt("histogram.csv", his, delimiter=",")
		plt.bar(range(dim), his)
		plt.savefig('histogram.png')
		plt.show()

class Question3():
	def run(self, path, threshold):
		def connected_components(h, w, bin_image):
			vis = np.zeros((h, w))
			label = np.zeros((h, w))
			region_id = 1
			n_labels = np.zeros(h * w)
			for row in range(h):
				for col in range(w):
					if bin_image.getpixel((row, col)) == 0:
						vis[row, col] = 1
					elif vis[row, col] == 0:
						stack = []
						stack.append((row, col))
						while len(stack) > 0:
							r, c = stack.pop()
							if vis[r, c] == 1:
								continue
							vis[r, c] = 1
							label[r, c] = region_id
							n_labels[region_id] += 1
							for y in [r - 1, r, r + 1]:
								for x in [c - 1, c, c + 1]:
									if (0 <= y < h) and (0 <= x < w):
										if (bin_image.getpixel((y, x)) != 0) and (vis[y, x] == 0):
											stack.append((y, x))
						region_id += 1
			return label, n_labels

		def rectangle(label, n_labels, thres,  h, w):
			recs = []
			for region, n in enumerate(n_labels):
				if (n >= thres):
					left = w
					right = 0
					top = h
					bot = 0
					for y in range(w):
						for x in range(h):
							if (label[y, x] == region):
								if (y < left):
									left = y
								if (y > right):
									right = y
								if (x < top):
									top = x
								if (x > bot):
									bot = x
					recs.append((left, right, top, bot))
			return recs

		def draws(recs, rec_img):
			while recs:
				left, right, top, bot = recs.pop()
				draw = ImageDraw.Draw(rec_img)
				draw.rectangle(((left, top), (right, bot)), outline = 'yellow')
				centroid_x = (left + right) / 2
				centroid_y = (top + bot) / 2
				draw.line(((centroid_x - 10, centroid_y), (centroid_x + 10, centroid_y)), fill = 'green', width = 3)
				draw.line(((centroid_x, centroid_y - 10), (centroid_x, centroid_y + 10)), fill = 'green', width = 3)
			rec_img.save('connect_components.bmp')

		hreshold = 500
		bin_img = Image.open('binary.bmp')
		h, w = bin_img.size
		label,n_labels = connect_components(h, w, bin_img)
		recs = rectangle(label, n_labels, threshold, w, h)
		rec_img = Image.open('binary.bmp').convert('RGB')

		draws(recs, rec_img)

if __name__ == '__main__':
	args = parse_args()
	Question1().run(128, args.lena)
	Question2().run(args.lena, 256)
	Question3().run(args.lena, 500)