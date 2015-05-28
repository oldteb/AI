from BayesianNetwork import BayesianNetwork
from random import randrange, random




class RejectionSampling(object):

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
			sample = self.prior_sample(self.BN)
			if self.sample_compare(self.BN.obsrvList, sample):
				self.statistic[sample[self.BN.queryV]] += 1
		rst = self.Normalize(self.statistic)
		return rst


	def prior_sample(self, BN):
		rst = [0]*(len(BN.obsrvList))
		for i in xrange(0, len(rst)):
			p = self.getPossibility(i, rst, BN)
			if random() < p:
				rst[i] = 1
		return rst


	def getPossibility(self, index, rst, BN):
		if(index == 0):
			return BN.nodes[0].CPT[0]
		elif(index == 3):
			return BN.nodes[3].CPT[rst[1]*2 + rst[2]]
		else:
			return BN.nodes[index].CPT[rst[0]]


	def sample_compare(self, obsrvList, sample):
		for i in xrange(0, len(obsrvList)):
			if obsrvList[i] == 't' and sample[i] == 0:
				return False
			if obsrvList[i] == 'f' and sample[i] == 1:
				return False
		return True


	def Normalize(self, statistic):
		sum = statistic[0] + statistic[1]
		if sum == 0:
			return [0,0]
		return [statistic[0]*1.0/sum, statistic[1]*1.0/sum]



