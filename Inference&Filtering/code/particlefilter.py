from random import randrange, random



class DynamicBayesianNetwork(object):
	prior = []
	transitionM = []
	sensorM = []

	def __init__(self, prior, transitionM, sensorM):
		self.prior = prior
		self.transitionM = transitionM
		self.sensorM = sensorM
		



class ParticleFiltering(object):

	num_sample = 0
	evidList = []
	DBN = 0
	sampleList = []

	def __init__(self, filepath):

		with open(filepath) as f:
			content = f.readline()
			self.evidList = content.strip().split(',')
			content = f.readline()
			self.num_sample = int(content.strip())

		self.DBN = DynamicBayesianNetwork([0.3,0.7],[0.3,0.7],[0.2,0.9])
		self.sampleList = [0] * self.num_sample


	def run(self):
		self.prior_sample(self.sampleList, self.DBN)
		for i in xrange(0, len(self.evidList)):
			self.particle_filtering(self.evidList[i], self.sampleList, self.DBN)
		rst = self.Normalize(self.sampleList)
		return rst

	def prior_sample(self, sampleList, DBN):
		for i in xrange(0, len(sampleList)):
			if random() < DBN.prior[1]:
				sampleList[i] = 1


	def particle_filtering(self, evidence, sampleList, DBN):
		statistic = [0] * 2
		weight = self.getWeight(evidence)
		for i in xrange(0, len(sampleList)):
			if random() < DBN.transitionM[sampleList[i]]:
				sampleList[i] = 1
			else:
				sampleList[i] = 0
			statistic[sampleList[i]] += 1
		self.resampling(weight, statistic, sampleList)


	def resampling(self, weight, statistic, sampleList):
		probability = weight[1] * statistic[1] / (weight[0] * statistic[0] + weight[1] * statistic[1])
		for i in xrange(0, len(sampleList)):
			if random() < probability:
				sampleList[i] = 1
			else:
				sampleList[i] = 0


	def getWeight(self, evidence):
		if evidence == 't':
			return [self.DBN.sensorM[0], self.DBN.sensorM[1]]
		else:
			return [1.0 - self.DBN.sensorM[0], 1.0 - self.DBN.sensorM[1]]


	def Normalize(self, sampleList):
		statistic = [0] * 2
		for i in xrange(len(sampleList)):
			statistic[sampleList[i]] += 1
		sum = statistic[0] + statistic[1]
		return [statistic[0]*1.0/sum, statistic[1]*1.0/sum]