from rich.console import Console

c = Console()
def readMazeFile(name):
	return open(name).read().split("\n")


def returnNeighbours(maze, currentX, currentY):
	neighbours = []



	#check above
	if currentY - 1 >= 0 and maze[currentY - 1][currentX] == "-":
		neighbours.append((currentX, currentY - 1))

	#check right
	try:
		if maze[currentY][currentX + 2] == "-":
			neighbours.append((currentX + 2, currentY))
	except IndexError:
		c.print("right")
		c.print(currentY , currentX+2)

	#check left
	try:
		if maze[currentY][currentX - 2] == "-":
			neighbours.append((currentX - 2, currentY))
	except IndexError:
		c.print("left")
		c.print(currentY, currentX - 2)


	#check below
	if (currentY + 1) < (len(maze) - 1) and maze[currentY + 1][currentX] == "-":
			neighbours.append((currentX, currentY + 1))


	# c.print(len(maze))

	return neighbours





def buildAdjacencyList(maze):
	adjacencyList = {}

	for y in range(len(maze)):
		for x in range(len(maze[y])):
			if maze[y][x] == "-":
				# Check if the current point is a node and if so check neighbours

				adjacencyList[(x, y)] = returnNeighbours(maze, x, y)

	return adjacencyList


def printMazeFromAdjacencyList(al, currentV):
	outputString = ''


def depthFirstSearch(adjacencyList, root, goal):

	discovered = []
	S = []

	cameFrom = {}

	S.append(root)

	while len(S) > 0:
		if len(discovered) % 1000 == 0:
			c.print(f"[*] Percentage of maze explored: {(int((len(discovered)/len(adjacencyList))*100))}%")
		v = S.pop()

		if v == goal:
			c.print("[*] [green]Goal reached")
			return cameFrom

		if v not in discovered:
			discovered.append(v)

			for w in adjacencyList[v]:

				if w in discovered:
					continue

				S.append(w)
				cameFrom[w] = v

	c.print("[*] [red]No solution possible")
	return 0


def backtrackSolution(solutionMap, root, goal):
	current = goal
	path = [goal]

	while not current == root:
		path.append(current)
		current = solutionMap[current]

	path.append(root)
	path.reverse()

	return path



def saveSolution(mazeFileName, maze, solution):
	outputString = ''

	# with open(f"{mazeFileName.split('.')[0]}-Solution.txt", "w") as file:
	for y in range(len(maze)):
		for x in range(len(maze[y])):
			if maze[y][x] == "-":
				if (x, y) in solution:
					# file.write("X")
					outputString += "X"
				else:
					# file.write("-")
					outputString += "-"
			else:
				# file.write(maze[y][x])
				outputString += maze[y][x]
		# file.write("\n")
		outputString += "\n"

	with open(f"{mazeFileName.split('.')[0]}-Solution.txt", "w") as file:
		file.write(outputString)


	c.print("[*] File saved")

c.clear()

mazeFileName = 'maze-Large.txt'

mazeFile = readMazeFile(mazeFileName)
c.print("[*] File read into memory")

adjacencyList = buildAdjacencyList(mazeFile)
c.print("[*] Adjacency list built")

start = list(adjacencyList.keys())[0]
end = list(adjacencyList.keys())[-1]

c.print("[*] Solving started...")
solutionMap = depthFirstSearch(adjacencyList, start, end)

if solutionMap != 0:
	c.print("[*] Constructing solution...")
	saveSolution(mazeFileName, mazeFile, backtrackSolution(solutionMap, start, end))


