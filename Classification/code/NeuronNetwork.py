from random import randrange, random

class Neuron(object):

	def __init__(self, level, num):
		self.a = 0
		self.ins = 0
		self.level = level
		if num > 0:
			self.ListofWeight = [0] * num
		else:
			self.ListofWeight = 0

	def initWeights(self):
		for i in xrange(len(self.ListofWeight)):
			self.ListofWeight[i] = random()


class NeuronNetwork(object):

	InputList = []
	HiddenList = []
	OutputList = []

	def __init__(self, k, NumofIL, NumofOL):
		for i in xrange(NumofIL):
			temp = Neuron(0,k)
			temp.initWeights()
			self.InputList.append(temp)
		for i in xrange(k):
			temp = Neuron(1,NumofOL)
			temp.initWeights()
			self.HiddenList.append(temp)
		self.OutputList.append(Neuron(2,0))







