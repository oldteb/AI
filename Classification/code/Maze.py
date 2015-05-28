import math
import sys 	


class MazeNode(object):
	def __init__(self):
		self.shift = []
		self.fn_value = 0
		self.gn_value = 0
		self.hn_value = 0
		self.status = 0

	def setValue(self, shift, gn, hn, status):
		self.shift = shift
		self.gn_value = gn
		self.hn_value = hn
		self.fn_value = gn+hn
		self.status = status
		

class Maze(object):
	def __init__(self, filepath, dimension):
		self.dimension = dimension
		self.matrix = [[0 for x in xrange(self.dimension)] for x in xrange(self.dimension)]
		self.initFromFile(filepath)
		self.printMaze()

	def initFromFile(self, filepath):
		with open(filepath) as f:
			for i in xrange(self.dimension):
				content = f.readline()
				arr = content.strip().split(' ')
				for j in xrange(len(arr)):
					if arr[j] == 'S':
						self.matrix[i][j] = 3
						self.start = [i,j]
					elif arr[j] == 'G':
						self.matrix[i][j] = 4
						self.goal = [i,j]
					else:
						self.matrix[i][j] = int(arr[j])
	def printMaze(self):
		for i in xrange(self.dimension):
			for j in xrange(self.dimension):
				if self.matrix[i][j] == 0:
					print '-',
				elif self.matrix[i][j] == 1:
					print '*',
				elif self.matrix[i][j] == 2:
					print '#',
				elif self.matrix[i][j] == 3:
					print 'S',
				else:
					print 'G',
			print " "

class AStarMaze(object):

	def __init__(self, filepath, dimension):
		self.maze = Maze(filepath, dimension)
		self.info = [[MazeNode() for x in xrange(dimension)] for x in xrange(dimension)]


	def ASSolver(self):
		while True:
			cur = self.getNext()
			if cur == 0:
				cur = self.info[self.maze.start[0]][self.maze.start[1]]
				cur.setValue([],0,self.getDistence(self.maze.start[0], self.maze.start[1]),-1)
				cur = [self.maze.start[0], self.maze.start[1]]
			elif cur[0] == self.maze.goal[0] and cur[1] == self.maze.goal[1]:
				break;
			self.extendCur(cur)

		self.pathGen()
		

	def getDistence(self,x,y):
		return abs(x-self.maze.goal[0]) + abs(y-self.maze.goal[1])

	def getNext(self):
		min = sys.maxint
		temp = 0
		for i in xrange(self.maze.dimension):
			for j in xrange(self.maze.dimension):
				if self.info[i][j].status == 1:
					if self.info[i][j].fn_value < min:
						temp = [i,j]
						min = self.info[i][j].fn_value
		if min == sys.maxint:
			return 0
		else:
			self.info[temp[0]][temp[1]].status = -1
			return temp

	def extendCur(self, cur):
		cur_gn = self.info[cur[0]][cur[1]].gn_value
		# extend up direction
		if cur[0]-1 >= 0 and self.maze.matrix[cur[0]-1][cur[1]] != 1 and self.info[cur[0]-1][cur[1]].status != -1:
			temp = self.info[cur[0]-1][cur[1]]
			if temp.status == 0 or (temp.status == 1 and temp.gn_value > cur_gn+1):
				temp.setValue([0,1],cur_gn+1,self.getDistence(cur[0]-1,cur[1]),1)
		# extend down direction
		if cur[0]+1 < self.maze.dimension and self.maze.matrix[cur[0]+1][cur[1]] != 1 and self.info[cur[0]+1][cur[1]].status != -1:
			temp = self.info[cur[0]+1][cur[1]]
			if temp.status == 0 or (temp.status == 1 and temp.gn_value > cur_gn+1):
				temp.setValue([0,-1],cur_gn+1,self.getDistence(cur[0]+1,cur[1]),1)
		# extend left direction
		if cur[1]-1 >= 0 and self.maze.matrix[cur[0]][cur[1]-1] != 1 and self.info[cur[0]][cur[1]-1].status != -1:
			temp = self.info[cur[0]][cur[1]-1]
			if temp.status == 0 or (temp.status == 1 and temp.gn_value > cur_gn+1):
				temp.setValue([-1,0],cur_gn+1,self.getDistence(cur[0],cur[1]-1),1)
		# extend right direction
		if cur[1]+1 < self.maze.dimension and self.maze.matrix[cur[0]][cur[1]+1] != 1 and self.info[cur[0]][cur[1]+1].status != -1:
			temp = self.info[cur[0]][cur[1]+1]
			if temp.status == 0 or (temp.status == 1 and temp.gn_value > cur_gn+1):
				temp.setValue([1,0],cur_gn+1,self.getDistence(cur[0],cur[1]+1),1)


	def pathGen(self):
		cur = [self.maze.goal[0],self.maze.goal[1]]
		while cur[0] != self.maze.start[0] or cur[1] != self.maze.start[1]:
			self.maze.matrix[cur[0]][cur[1]] = 2
			temp = self.info[cur[0]][cur[1]]
			if temp.shift[0] == 0:
				cur[0] += temp.shift[1]
				cur[1] += temp.shift[0]
			else:
				cur[0] -= temp.shift[1]
				cur[1] -= temp.shift[0]
		self.maze.matrix[self.maze.goal[0]][self.maze.goal[1]] = 4
		print "Path:"
		self.maze.printMaze()
