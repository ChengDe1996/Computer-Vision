import numpy as np
import cv2

class Solution:
	def __init__(self, l_mask1, l_mask2, mvl_mask, log_mask, dog_mask):
		self.l_mask1 = l_mask1
		self.l_mask2 = l_mask2
		self.mvl_mask = mvl_mask
		self.log_mask = log_mask
		self.dog_mask = dog_mask

	def Laplacian(self, image, threshold, mask):
		res = np.zeros((512, 512), dtype = int)
		h, w = image.shape
		for i in range(1, h-1):
			for j in range(1, w-1):
				temp = np.sum(image[i-1:i+2, j-1:j+2] * mask)
				if temp >= threshold:
					res[i-1][j-1] = 1
				elif temp <= -threshold:
					res[i-1][j-1] = -1
				else:
					res[i-1][j-1] = 0
		res_border = cv2.copyMakeBorder(res, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
		zero_cross = np.zeros((512, 512), dtype = np.uint8)
		h2, w2 = res_border.shape
		for i in range(1, h2-1):
			for j in range(1, w2-1):
				if res_border[i][j] == 1:
					temp = res_border[i-1:i+2, j-1:j+2]
					if -1 in temp:
						zero_cross[i-1][j-1] = 0
					else:
						zero_cross[i-1][j-1] = 255
				else:
					zero_cross[i-1][j-1] = 255
		return zero_cross

	def Minimum_Variance_Laplacian(self, image, threshold, mask):
		res = np.zeros((512, 512), dtype = int)
		h, w = image.shape
		for i in range(1, h-1):
			for j in range(1, w-1):
				temp = np.sum(image[i-1:i+2, j-1:j+2] * mask)
				if temp >= threshold:
					res[i-1][j-1] = 1
				elif temp <= -threshold:
					res[i-1][j-1] = -1
				else:
					res[i-1][j-1] = 0
		res_border = cv2.copyMakeBorder(res, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
		zero_cross = np.zeros((512, 512), dtype = np.uint8)
		h2, w2 = res_border.shape
		for i in range(1, h2-1):
			for j in range(1, w2-1):
				if res_border[i][j] == 1:
					temp = res_border[i-1:i+2, j-1:j+2]
					if -1 in temp:
						zero_cross[i-1][j-1] = 0
					else:
						zero_cross[i-1][j-1] = 255
				else:
					zero_cross[i-1][j-1] = 255
		return zero_cross


	def Laplacian_of_Gaussian(self, image, threshold, mask):
		res = np.zeros((512, 512), dtype = int)
		h, w = image.shape
		for i in range(5, h-5):
			for j in range(5, w-5):
				temp = np.sum(image[i-5:i+6, j-5:j+6] * mask)
				if temp >= threshold:
					res[i-5][j-5] = 1
				elif temp <= -threshold:
					res[i-5][j-5] = -1
				else:
					res[i-5][j-5] = 0
		res_border = cv2.copyMakeBorder(res, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
		zero_cross = np.zeros((512, 512), dtype = np.uint8)
		h2, w2 = res_border.shape
		for i in range(1, h2-1):
			for j in range(1, w2-1):
				if res_border[i][j] == 1:
					temp = res_border[i-1:i+2, j-1:j+2]
					if -1 in temp:
						zero_cross[i-1][j-1] = 0
					else:
						zero_cross[i-1][j-1] = 255
				else:
					zero_cross[i-1][j-1] = 255
		return zero_cross

	def Differece_of_Guassian(self, image, threshold, mask):
		res = np.zeros((512, 512), dtype = int)
		h, w = image.shape
		for i in range(5, h-5):
			for j in range(5, w-5):
				temp = np.sum(image[i-5:i+6, j-5:j+6] * mask)
				if temp >= threshold:
					res[i-5][j-5] = 1
				elif temp <= -threshold:
					res[i-5][j-5] = -1
				else:
					res[i-5][j-5] = 0
		res_border = cv2.copyMakeBorder(res, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
		zero_cross = np.zeros((512, 512), dtype = np.uint8)
		h2, w2 = res_border.shape
		for i in range(1, res_border.shape[0]-1):
			for j in range(1, res_border.shape[1]-1):
				if res_border[i][j] == 1:
					temp = res_border[i-1:i+2, j-1:j+2]
					if -1 in temp:
						zero_cross[i-1][j-1] = 0
					else:
						zero_cross[i-1][j-1] = 255
				else:
					zero_cross[i-1][j-1] = 255
		return zero_cross

	def solve(self, input_path):
		image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE).astype(int)
		border1 = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
		border5 = cv2.copyMakeBorder(image, 5, 5, 5, 5, cv2.BORDER_REPLICATE)
		lena_laplacian_mask1 = self.Laplacian(border1, 15, self.l_mask1)
		lena_laplacian_mask2 = self.Laplacian(border1, 15, self.l_mask2)
		lena_minimum_variance_laplacian = self.Minimum_Variance_Laplacian(border1, 20, self.mvl_mask)
		lena_laplacian_of_guassian = self.Laplacian_of_Gaussian(border5, 3000, self.log_mask)
		lena_difference_of_guassian = self.Differece_of_Guassian(border5, 1, self.dog_mask)
		cv2.imwrite("lena_laplacian_mask1.bmp", lena_laplacian_mask1)
		cv2.imwrite("lena_laplacian_mask2.bmp", lena_laplacian_mask2)
		cv2.imwrite("lena_minimum_variance_laplacian.bmp", lena_minimum_variance_laplacian)
		cv2.imwrite("lena_laplacian_of_guassian.bmp", lena_laplacian_of_guassian)
		cv2.imwrite("lena_difference_of_guassian.bmp", lena_difference_of_guassian)



if __name__ == '__main__':
	# Laplacian_mask1
	l_mask1 = np.array([[0, 1, 0],
						[1, -4, 1],
						[0, 1, 0]])
	# Laplacian_mask2
	l_mask2 = (1/3) * np.array([[1, 1, 1],
								[1, -8, 1],
								[1, 1, 1]])
	# minimum varience laplacian mask
	mvl_mask = (1/3) * np.array([[2, -1, 2],
								 [-1, -4, -1],
								 [2, -1, 2]])
	# laplacian of guassian mask
	log_mask = np.array([[0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0],
						 [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
						 [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
						 [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
						 [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
						 [-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],
						 [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
						 [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
						 [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
						 [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
						 [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]])
	# difference of guassian mask
	dog_mask = np.array([[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
						 [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
						 [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
						 [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
						 [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
						 [-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],
						 [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
						 [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
						 [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
						 [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
						 [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1]])

	sol = Solution(l_mask1, l_mask2, mvl_mask, log_mask, dog_mask)

	sol.solve("lena.bmp")







