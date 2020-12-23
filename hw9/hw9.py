import numpy as np 
import cv2

class Solution:
	def gradient(self, v1, v2, threshold):
		val = (v1**2 + v2**2)**0.5
		if val <= threshold: return 255
		return 0

	def Roberts(self, image, threshold):
		res = np.ones((512, 512), dtype = np.uint8)
		h, w = image.shape
		for i in range(1, h-1):
			for j in range(1, w-1):
				v1 = int(image[i+1, j+1]) - int(image[i, j])
				v2 = int(image[i+1, j]) - int(image[i, j+1])
				res[i-1][j-1] = self.gradient(v1, v2, threshold)

		return res

	def Prewitt(self, image, threshold):
		res = np.ones((512, 512), dtype = np.uint8)
		h, w = image.shape
		for i in range(1, h-1):
			for j in range(1, w-1):
				v1 = sum(image[i+1, j-1:j+2]) - sum(image[i-1, j-1:j+2])
				v2 = sum(image[i-1:i+2, j+1]) - sum(image[i-1:i+2, j-1])
				res[i-1][j-1] = self.gradient(v1, v2, threshold)
		return res

	def Sobel(self, image, threshold):
		res = np.zeros((512, 512), dtype = np.uint8)
		h, w = image.shape
		for i in range(1, h-1):
			for j in range(1, w-1):
				v1 = (image[i+1][j-1] + 2*image[i+1][j] + image[i+1][j+1]) - (image[i-1][j-1] + 2*image[i-1][j] + image[i-1][j+1])
				v2 = (image[i-1][j+1] + 2*image[i][j+1] + image[i+1][j+1]) - (image[i-1][j-1] + 2*image[i][j-1] + image[i+1][j-1])
				res[i-1][j-1] = self.gradient(v1, v2, threshold)
		return res

	def FreiAndChen(self, image, threshold):
		res = np.ones((512, 512), dtype = np.uint8)
		h, w = image.shape
		for i in range(1, h-1):
			for j in range(1, w-1):
				v1 = (image[i+1][j-1] + 2**0.5 * image[i+1][j] + image[i+1][j+1]) - (image[i-1][j-1] + 2**0.5 * image[i-1][j] + image[i-1][j+1])
				v2 = (image[i-1][j+1] + 2**0.5 * image[i][j+1] + image[i+1][j+1]) - (image[i-1][j-1] + 2**0.5 * image[i][j-1] + image[i+1][j-1])
				res[i-1][j-1] = self.gradient(v1, v2, threshold)
		return res

	def gradient_max(self, values, threshold):
		value = np.max(values)
		if value <= threshold: return 255
		return 0

	def Kirsch(self, image, threshold, filters):
		res = np.ones((512, 512), dtype = np.uint8)
		h, w = image.shape
		for i in range(1, h-1):
			for j in range(1, w-1):
				can = []
				temp = image[i-1:i+2, j-1:j+2]
				for f in filters:
					can.append(np.sum(temp*f))
				res[i-1][j-1] = self.gradient_max(can, threshold)
		return res

	def Robinson(self, image, threshold, filters):
		res = np.ones((512, 512), dtype = np.uint8)
		h, w = image.shape
		for i in range(1, h-1):
			for j in range(1, w-1):
				can = []
				for f in filters:
					can.append(np.sum(image[i-1:i+2, j-1:j+2] * f ))
				res[i-1][j-1] = self.gradient_max(can, threshold)
		return res

	def NevatiaBabu(self, image, threshold, filters):
		res = np.ones((512, 512), dtype = np.uint8)
		h, w = image.shape
		for i in range(2, h-2):
			for j in range(2, w-2):
				can = []
				for f in filters:
					can.append(np.sum(image[i-2:i+3, j-2:j+3] * f))
				res[i-2][j-2] = self.gradient_max(can, threshold)
		return res

	def read_image(self, lena_path):
		image = cv2.imread(lena_path, cv2.IMREAD_GRAYSCALE).astype(int)
		border1 = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
		border2 = cv2.copyMakeBorder(image, 2, 2, 2, 2, cv2.BORDER_REPLICATE)

		return image, border1, border2


	def save_image(self, image, path):
		cv2.imwrite(path, image)



def hw9(kirsch_f, robinson_f, babu_f, lena_path):
	# image = Image.open(lena_path)
	sol = Solution()
	image, border1, border2 = sol.read_image(lena_path)
	
	print('robert')
	roberts = sol.Roberts(border1, 12)
	sol.save_image(roberts, 'roberts.bmp')
	
	print('prewitt')
	prewitt = sol.Prewitt(border1, 24)
	sol.save_image(prewitt, 'prewitt.bmp')

	print('sobel')
	sobel = sol.Sobel(border1, 38)
	sol.save_image(sobel, 'sobel.bmp')

	print('fnc')
	fnc = sol.FreiAndChen(border1, 30)
	sol.save_image(fnc, 'fnc.bmp')

	print('kirsch')
	kirsch = sol.Kirsch(border1, 135, kirsch_f)
	sol.save_image(kirsch, 'kirsch.bmp')

	print('robinson')
	robinson = sol.Robinson(border1, 43, robinson_f)
	sol.save_image(robinson, 'robinson.bmp')

	print('babu')
	nev_babu = sol.NevatiaBabu(border2, 12500, babu_f)
	sol.save_image(nev_babu, 'nevatia_babu.bmp')


if __name__ == '__main__':
	
	path = 'lena.bmp'

	kirsch_f = np.array([[[-3, -3, 5],
				[-3, 0, 5],
				[-3, -3, 5]],
			   [[-3, 5, 5],
				[-3, 0, 5],
				[-3, -3, -3]],
			   [[5, 5, 5],
				[-3, 0, -3],
				[-3, -3, -3]],
			   [[5, 5, -3],
				[5, 0, -3],
				[-3, -3, -3]],
			   [[5, -3, -3],
				[5, 0, -3],
				[5, -3, -3]],
			   [[-3, -3, -3],
				[5, 0, -3],
				[5, 5, -3]],
			   [[-3, -3, -3],
				[-3, 0, -3],
				[5, 5, 5]],
			   [[-3, -3, -3],
				[-3, 0, 5],
				[-3, 5, 5]]])

	robinson_f = np.array([[[-1, 0, 1],
				[-2, 0, 2],
				[-1, 0, 1]],
			   [[0, 1, 2],
				[-1, 0, 1],
				[-2, -1, 0]],
			   [[1, 2, 1],
				[0, 0, 0],
				[-1, -2, -1]],
			   [[2, 1, 0],
				[1, 0, -1],
				[0, -1, -2]],
			   [[1, 0, -1],
				[2, 0, -2],
				[1, 0, -1]],
			   [[0, -1, -2],
				[1, 0, -1],
				[2, 1, 0]],
			   [[-1, -2, -1],
				[0, 0, 0],
				[1, 2, 1]],
			   [[-2, -1, 0],
				[-1, 0, 1],
				[0, 1, 2]]])

	babu_f = np.array([[[100, 100, 100, 100, 100],
									  [100, 100, 100, 100, 100],
									  [0, 0, 0, 0, 0],
									  [-100, -100, -100, -100, -100],
									  [-100, -100, -100, -100, -100]],
									 [[100, 100, 100, 100, 100],
									  [100, 100, 100, 78, -32],
									  [100, 92, 0, -92, -100],
									  [32, -78, -100, -100, -100],
									  [-100, -100, -100, -100, -100]],
									 [[100, 100, 100, 32, -100],
									  [100, 100, 92, -78, -100],
									  [100, 100, 0, -100, -100],
									  [100, 78, -92, -100, -100],
									  [100, -32, -100, -100, -100]],
									 [[-100, -100, 0, 100, 100],
									  [-100, -100, 0, 100, 100],
									  [-100, -100, 0, 100, 100],
									  [-100, -100, 0, 100, 100],
									  [-100, -100, 0, 100, 100]],
									 [[-100, 32, 100, 100, 100],
									  [-100, -78, 92, 100, 100],
									  [-100, -100, 0, 100, 100],
									  [-100, -100, -92, 78, 100],
									  [-100, -100, -100, -32, 100]],
									 [[100, 100, 100, 100, 100],
									  [-32, 78, 100, 100, 100],
									  [-100, -92, 0, 92, 100],
									  [-100, -100, -100, -78, 32],
									  [-100, -100, -100, -100, -100]]])

	hw9(kirsch_f, robinson_f, babu_f, path)
