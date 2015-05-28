from copy import deepcopy


class Node:

	index = 0;
	parentsList = []
	NodeType = "";
	CPT = []


	def __init__(self, index, parentsList, NodeType, CPT):
		self.index = index
		self.parentsList = parentsList
		self.CPT = CPT

		if NodeType == 't' or NodeType == 'f':
			self.NodeType = "Evidence"
		else:
			self.NodeType = "Variable"




class BayesianNetwork:

	queryV = 0
	nodes = []
	obsrvList = []


	def __init__(self, obsrvList):
		self.obsrvList = obsrvList

		for i in xrange(0, len(obsrvList)):
			if obsrvList[i] == 'q':
				self.queryV = i
				break


		nodes = [0]*(len(obsrvList))
		nodes[0] = Node(0, [], obsrvList[0], [0.5,0.5])
		nodes[1] = Node(1, [0], obsrvList[1], [0.5,0.1])
		nodes[2] = Node(2, [0], obsrvList[2], [0.2,0.8])
		nodes[3] = Node(3, [1,2], obsrvList[3], [0,0.9,0.9,0.99])
		self.nodes = nodes
		


		
