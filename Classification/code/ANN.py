from NeuronNetwork import NeuronNetwork
from math import exp


class ANN(object):
	

	examples = 0
	network = 0
	k = 0
	NumofIL = 0
	NumofOL = 0

	def __init__(self, filepath,k):
		self.initExamples(filepath)
		self.k = k
		self.NumofIL = len(self.examples[0])-1
		self.NumofOL = 1
		self.network = NeuronNetwork(self.k, self.NumofIL, self.NumofOL)

	def initExamples(self, filepath):
		self.examples = [[0 for x in xrange(3)] for x in xrange(200)]
		with open(filepath) as f:
			for i in xrange(200):
				content = f.readline()
				arr = content.strip().split(' ')
				for j in xrange(len(arr)):
					self.examples[i][j] = float(arr[j])

	def run(self):
		for i in xrange(int(len(self.examples) * 0.8)):
			self.forward(self.examples[i])
			# Propagate deltas backward from output layer to input layer
			self.backward(self.examples[i][2])
		self.test()

	def forward(self, example):
		for j in xrange(self.NumofIL):
			self.network.InputList[j].a = example[j]
		for j in xrange(self.k):
			sum = 0
			for m in xrange(self.NumofIL):
				sum += self.network.InputList[m].a * self.network.InputList[m].ListofWeight[j]
				# sum += self.network.InputList[m].a * 1
			self.network.HiddenList[j].ins = sum
			self.network.HiddenList[j].a = self.funcG(sum)
		sum = 0
		for m in xrange(self.k):
			sum += self.network.HiddenList[m].a * self.network.HiddenList[m].ListofWeight[0]
		self.network.OutputList[0].ins = sum
		self.network.OutputList[0].a = self.funcG(sum)
		return self.network.OutputList[0].a

	def backward(self, rst):
		deltaj = self.funcG1(self.network.OutputList[0].ins) * (rst - self.network.OutputList[0].a)
		# print deltaj
		for m in xrange(self.k):
			# print "old:",self.network.HiddenList[m].ListofWeight[0]
			self.network.HiddenList[m].ListofWeight[0] += 1 * self.network.HiddenList[m].a * deltaj
			# print "new:",self.network.HiddenList[m].ListofWeight[0]
		delta = [0]*self.k
		for j in xrange(self.k):
			delta[j] = self.funcG1(self.network.HiddenList[j].ins) * self.network.HiddenList[j].ListofWeight[0] * deltaj
		for m in xrange(self.NumofIL):
			for n in xrange(self.k):	
				self.network.InputList[m].ListofWeight[n] += 1 * self.network.InputList[m].a * delta[n]

	def funcG(self, ins):
		return 1/(exp(ins*(-1))+1)

	def funcG1(self, ins):
		return self.funcG(ins) * (1-self.funcG(ins))

	def test(self):
		correct = 0
		for i in range(int(len(self.examples) * 0.8), len(self.examples)):
			print "Expected:",self.examples[i][2],"Got:",round(self.forward(self.examples[i]))
			if self.examples[i][2] - round(self.forward(self.examples[i])) == 0:
				correct += 1
		print "target rate:",1 - correct*1.0/40
