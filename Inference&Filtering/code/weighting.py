from BayesianNetwork import BayesianNetwork
from random import randrange, random




class LikelyhoodWeighting(object):

	num = 0
	statistic = []
	BN = 0

	def __init__(self, filepath):

		with open(filepath) as f:
			content = f.readline()
			arr = content.strip().split(',')
			content = f.readline()
			self.num = int(content.strip())

		self.BN = BayesianNetwork(arr)
		self.statistic = [0]*2


	def run(self):
		for i in xrange(0, self.num):
			sample = self.weighted_sample(self.BN)
			self.statistic[sample[0][self.BN.queryV]] += sample[1]
		rst = self.Normalize(self.statistic)
		return rst


	def weighted_sample(self, BN):
		rst = [0]*(len(BN.obsrvList))
		weight = 1.0
		for i in xrange(0, len(rst)):
			if cmp(BN.nodes[i].NodeType, "Evidence") == 0:
				if BN.obsrvList[i] == 't':
					rst[i] = 1
				if rst[i] == 0:
					weight *= (1.0 - self.getPossibility(i, rst, BN))
				else:
					weight *= self.getPossibility(i, rst, BN)
			else:
				p = self.getPossibility(i, rst, BN)
				if random() < p:
					rst[i] = 1

		return [rst, weight]

	def getPossibility(self, index, rst, BN):
		if(index == 0):
			return BN.nodes[0].CPT[0]
		elif(index == 3):
			return BN.nodes[3].CPT[rst[1]*2 + rst[2]]
		else:
			return BN.nodes[index].CPT[rst[0]]


	def Normalize(self, statistic):
		sum = statistic[0] + statistic[1]
		return [statistic[0]/sum, statistic[1]/sum]
