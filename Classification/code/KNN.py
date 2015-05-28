from math import sqrt

class KNN(object):

	examples = 0
	test_examples = 0
	network = 0
	k = 0
	NumofIL = 0
	NumofOL = 0
	new_num = 0

	def __init__(self, filepath,k):
		self.initExamples(filepath)
		self.k = k
		self.NumofIL = len(self.examples[0])-1
		self.NumofOL = 1

	def initExamples(self, filepath):
		self.examples = [[0 for x in xrange(3)] for x in xrange(200)]
		self.test_examples = [[0 for x in xrange(3)] for x in xrange(200)]
		with open(filepath) as f:
			for i in xrange(200):
				content = f.readline()
				arr = content.strip().split(' ')
				for j in xrange(len(arr)):
					self.examples[i][j] = float(arr[j])

	def run(self):
		correct = 0
		for i in range(int(len(self.examples) * 0.8), len(self.examples)):
			value = self.test(self.examples[i])
			if value == int(self.examples[i][2]):
				correct += 1
			self.new_num += 1
			self.examples[i][2] = value
		print 1 - correct*1.0/40

	def test(self, example):
		dic = {}
		for i in xrange(int(len(self.examples) * 0.8) + self.new_num):
			dic[self.getDistance(example, self.examples[i])] = self.examples[i][2]
		dict = sorted(dic.iteritems(), key=lambda d:d[0])
		zero = 0
		one = 0
		for i in xrange(self.k):
			if int(dict[i][1]) == 0:
				zero += 1
			else:
				one += 1
		if zero == one:
			return int(dict[0][1])
		elif zero > one:
			return 0
		else:
			return 1

	def getDistance(self, example1, example2):
		return sqrt((example1[0] - example2[0])**2 + (example1[1] - example2[1])**2)




