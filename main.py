import math
import os
import time
from rich.table import Table
from rich.console import Console
from rich.pretty import pprint
from rich.progress import track
from time import sleep

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
	try:
		if maze[currentY + 1][currentX] == "-":
				neighbours.append((currentX, currentY + 1))
	except IndexError as e:
		c.print(f"[*] Below Error: [red]{e}")

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

	nodesExplored = 0

	while len(S) > 0:
		v = S.pop()
		nodesExplored += 1

		if v == goal:
			c.print("[*] [green]Goal reached")
			return cameFrom, nodesExplored

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

	return path



def saveSolution(mazeFileName, maze, solution, algorithm):
	outputString = ''

	for vertex in solution:
		x, y = vertex
		maze[y] = maze[y][:x] + "X" + maze[y][x + 1:]

	for line in maze:
		outputString += line + "\n"

	with open(f"{mazeFileName.split('.')[0]}-{algorithm}-Solution.txt", "w") as file:
		file.write(outputString)


class BinaryHeapPriorityQueue:
    def __init__(self):
        self.heap = []
        self.size = 0

    def cameFrom(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def extractMin(self):
        if self.size <= 0:
            return None
        if self.size == 1:
            self.size -= 1
            return self.heap.pop()
    
        root = self.heap[0]
        last_element = self.heap.pop()
        self.size -= 1
        if self.size > 0:
            self.heap[0] = last_element
            self._minHeapify(0)
        return root


    def enqueue(self, priority, value):
        self.heap.append((priority, value))
        self.size += 1
        i = self.size - 1
        while i != 0 and self.heap[self.cameFrom(i)][0] > self.heap[i][0]:
            self.heap[i], self.heap[self.cameFrom(i)] = self.heap[self.cameFrom(i)], self.heap[i]
            i = self.cameFrom(i)

    def _minHeapify(self, i):
        l = self.left_child(i)
        r = self.right_child(i)
        smallest = i
        if l < self.size and self.heap[l][0] < self.heap[i][0]:
            smallest = l
        if r < self.size and self.heap[r][0] < self.heap[smallest][0]:
            smallest = r
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._minHeapify(smallest)

    def getSize(self):
        return self.size

    def contains(self, value):
        for _, v in self.heap:
            if v == value:
                return True
        return False

    def toString(self):
        return str(self.heap)


def aStar(adjacencyList, root, goal):
	multiplier = 10

	distance = {root: heuristic(root, goal, multiplier)}
	cameFrom = {root: None}

	heap = BinaryHeapPriorityQueue()
	heap.enqueue(0, root)

	nodesExplored = 0

	while heap.getSize() > 0:
		current = heap.extractMin()[1]
		nodesExplored += 1
	
		if current == goal:
			c.print("[*] [green]Goal reached")
			return cameFrom, nodesExplored

		for neighbor in adjacencyList[current]:
			tentative_distance = distance[current] + heuristic(neighbor, current)

			if neighbor not in distance or tentative_distance < distance[neighbor]:
				distance[neighbor] = tentative_distance
				priority = tentative_distance + heuristic(neighbor, goal, multiplier)
				heap.enqueue(priority, neighbor)

				cameFrom[neighbor] = current

	return 0

def heuristic(current, goal, m=1):
	return (abs(current[0] - goal[0]) + abs(current[1] - goal[1])) * m

availableMazeFiles = [x for x in os.listdir() if ("maze" in x and "Solution" not in x)]


c.print("[*] Available files:")
for i, availableMaze in enumerate(availableMazeFiles):
	c.print(f"[{i+1}] {availableMaze}")

mazeFileName = availableMazeFiles[int(c.input("\n[*] Maze: ")) - 1]

c.print("\n[*] Reading file into memory...")
mazeFile = readMazeFile(mazeFileName)
c.print("[*] File read into memory\n")

c.print("[*] Constructing adjacency list...")
adjacencyList = buildAdjacencyList(mazeFile)
c.print("[*] Adjacency list built\n")

root = list(adjacencyList.keys())[0]
goal = list(adjacencyList.keys())[-1]


def statsTable(algorithm, explored, adjacencyList, path, start, end):
	table = Table(title=f"Statistics for {algorithm}")

	table.add_column("[bold]Statistic")
	table.add_column("[bold]Value")

	table.add_row("Vertices visited", str(explored))
	table.add_row("Percentage of maze explored", f"{int((explored/len(adjacencyList)) * 100)}%")
	table.add_row("Solution length", str(len(path)))
	table.add_row("Time taken to solve the maze", f"{round(end-start, 5)} seconds")
	table.add_row("Solution percentage", f"[green]{int(len(path)/len(adjacencyList) * 100)}%")

	return table

c.print("\n[*] DFS Solving started...")

DFS_start = time.time()
DFS_solutionMap, DFS_explored = depthFirstSearch(adjacencyList, root, goal)

c.print("[*] Constructing solution from map...")
DFS_path = backtrackSolution(DFS_solutionMap, root, goal)
c.print("[*] Solution constructed\n")
DFS_end = time.time()
c.print(statsTable(f"DFS on {mazeFileName}", DFS_explored, adjacencyList, DFS_path, DFS_start, DFS_end))


c.print("\n[*] A* Solving started...")

ASTAR_start = time.time()
ASTAR_solutionMap, ASTAR_explored = aStar(adjacencyList, root, goal)

c.print("[*] Constructing solution from map...")
ASTAR_path = backtrackSolution(ASTAR_solutionMap, root, goal)
c.print("[*] Solution constructed\n")
ASTAR_end = time.time()

c.print(statsTable(f"A* on {mazeFileName}", ASTAR_explored, adjacencyList, ASTAR_path, ASTAR_start, ASTAR_end))



c.print("\n[*] Saving files...")
saveSolution(mazeFileName, mazeFile.copy(), ASTAR_path, "ASTAR")
saveSolution(mazeFileName, mazeFile.copy(), DFS_path, "DFS")
c.print("[*] File saved")

