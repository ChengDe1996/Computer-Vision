import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

class Solutions():
	def __init__(self, dim):
		self.dim = dim

	def gen_his(self, image, divided):
		his = np.zeros(self.dim)
		h, w = image.size
		for i in range(h):
			for j in range(w):
				val = image.getpixel((i, j))//divided
				if divided != 1: image.putpixel((i,j), val)
				his[val] += 1
		return his, image

	def plot_his(self, his, name):
		plt.bar(range(self.dim), his)
		plt.savefig(name)
		# plt.show()
		plt.close()
		
	def question1(self, path, save_name):
		# original image and its histogram
		image = Image.open(path)
		his, _ = self.gen_his(image, 1)
		self.plot_his(his, save_name + '_histogram.png')
		image.save(save_name + '.bmp')

	def question2(self, path, save_name, divided):
		# mage with intensity divided by 3 and its histogram
		image = Image.open(path)
		his, image = self.gen_his(image, divided)
		self.plot_his(his, save_name + '_histogram.png')
		image.save(save_name + '.bmp')

	def cal_sk(self, image, his):
		sk = np.zeros(self.dim)
		h, w = image.size
		n = w * h 
		for i in range(len(sk)):
			accu = []
			for j in range(i+1):
				accu.append(his[j]/n)
			sk[i] = int(255 * sum(accu))
		return sk

	def equalization(self, sk, image):
		h, w = image.size
		for i in range(h):
			for j in range(w):
				val = image.getpixel((i, j))
				image.putpixel((i, j), int(sk[val]))
		return image

	def question3(self, path):
		# image after applying histogram equalization to (b) and its histogram
		image = Image.open(path)
		his, image = self.gen_his(image, 1)
		sk = self.cal_sk(image, his)
		new_image = self.equalization(sk, image)
		his, _ = self.gen_his(new_image, 1)
		self.plot_his(his, 'equalization_histogram.png')
		new_image.save('equalization.bmp')





if __name__ == '__main__':
	sol = Solutions(256)
	sol.question1('lena.bmp', 'origin')
	sol.question2('lena.bmp', 'divided_by_3', 3)
	sol.question3('divided_by_3.bmp')