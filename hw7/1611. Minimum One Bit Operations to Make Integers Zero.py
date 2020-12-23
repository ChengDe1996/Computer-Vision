class Solution:
	def minimumOneBitOperations(self, n):
		if n <= 1: return n
		bin_res = str(bin(n))[2:]

		def h(n):
			b = str(bin(n))[2:]
			return 2**len(b) - 1

		def msb(n):
			msb = 1
			while n//2 > 0:
				msb*=2
				n/=2
			return msb
		return h(msb(n)) - self.minimumOneBitOperations(n-msb(n))



if __name__ == '__main__':
	n = 333
	print(Solution().minimumOneBitOperations(n))