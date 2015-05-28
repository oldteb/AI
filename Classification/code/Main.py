from ANN import ANN
from Maze import AStarMaze
from KNN import KNN


def main():
	# ann = ANN("hw5data.txt",10)
	# ann.run()

	# maze = AStarMaze("Maze.txt",10)
	# maze.ASSolver()

	knn = KNN("hw5data.txt",15)
	knn.run()


if __name__ == '__main__':
    main()
