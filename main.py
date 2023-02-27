import math
import os
import time
from queue import PriorityQueue
from collections import deque, defaultdict
from rich.table import Table
from rich.console import Console

c = Console()


def readMazeFile(name):
	with open(name) as f:
		return f.read().strip().split("\n")

def returnNeighbours(maze, x, y):
	# Initialize an empty list to hold the neighbors of the given cell
	neighbours = []
	# Check the cell above the given cell
	if y - 1 >= 0 and maze[y - 1][x] == "-":
		# If the above cell is within the boundaries of the maze and is a valid path, add it to the list of neighbors
		neighbours.append((x, y - 1))
	
	# Check the cell below the given cell
	if not (y + 1) == len(maze) and maze[y + 1][x] == "-":
		# If the below cell is within the boundaries of the maze and is a valid path, add it to the list of neighbors
		neighbours.append((x, y + 1))
	
	# Check the cell to the right of the given cell
	if maze[y][x + 2] == "-":
		# If the cell to the right is a valid path, add it to the list of neighbors
		neighbours.append((x + 2, y))

	# Check the cell to the left of the given cell
	if maze[y][x - 2] == "-":
		# If the cell to the left is a valid path, add it to the list of neighbors
		neighbours.append((x - 2, y))

	# Return the list of neighbors
	return neighbours


def buildAdjacencyList(maze):
	bounds = (0, len(maze), 0, len(maze[0]))
	adjacencyList = defaultdict(list)

	for y in range(bounds[1]):
		for x in range(0, bounds[3], 2):
			if maze[y][x] == "-":
				adjacencyList[(x, y)] = returnNeighbours(maze, x, y)
	
	return adjacencyList

def backtrackSolution(solutionMap, root, goal):
	# Set the current node to be the goal
	current = goal
	# Initialize a list to hold the path from the goal to the root
	path = [goal]

	# While the current node is not the root
	while not current == root:
		# Append the current node to the path
		path.append(current)
		# Set the current node to be the node that leads to it in the solution map
		current = solutionMap[current]

	# Append the root node to the path
	path.append(root)

	# Return the path from the goal to the root
	return path


def depthFirstSearch(adjacencyList, root, goal):
	# Initialize an empty set to keep track of discovered nodes.
	discovered = set()
	
	# Initialize a double-ended queue to store nodes to visit.
	S = deque()
	
	# Add the starting node to the queue.
	S.append(root)
	
	# Initialize an empty dictionary to keep track of the path from each visited node to its parent.
	cameFrom = {}
	
	# Initialize a counter to keep track of the number of nodes explored during the traversal.
	nodesExplored = 0
	
	# While there are nodes in the queue:
	while S:
		
		# Pop the last node from the queue.
		v = S.pop()
		
		# Increment the node counter.
		nodesExplored += 1
	
		# If the current node is the goal, return the dictionary map and the number of nodes explored.
		if v == goal:
			return cameFrom, nodesExplored
	
		# If the current node has not been discovered yet:
		if v not in discovered:
			
			# Mark it as discovered.
			discovered.add(v)
	
			# For each adjacent node w:
			for w in adjacencyList[v]:
				
				# If w has already been discovered, skip it.
				if w in discovered:
					continue
				
				# Otherwise, add w to the queue and record the path from v to w.
				S.append(w)

				# Set the parent of the neighbour to the current node
				cameFrom[w] = v
	
	# If the goal was not reached, return None for the path and the number of nodes explored.
	return None, nodesExplored



def saveSolution(mazeFileName, maze, solution, algorithm):
	# Initialize an empty string to hold the output
	outputString = ''

	# For each node in the solution path
	for node in solution:
		# Get the x and y coordinates of the node
		x, y = node
		# Replace the character at that position in the maze with an 'X'
		maze[y] = maze[y][:x] + "X" + maze[y][x + 1:]

	# For each line in the modified maze
	for line in maze:
		# Append the line to the output string with a newline character
		outputString += line + "\n"

	# Open a file with a name that includes the original maze file name, the name of the algorithm used, and the string "-Solution" 
	with open(f"{mazeFileName.split('.')[0]}-{algorithm}-Solution.txt", "w") as file:
		# Write the output string to the file
		file.write(outputString)

class BinaryHeapPriorityQueue:
	# Init method which is called when an object of the class is instantiated
	def __init__(self):
		# Initialize an empty list to store the heap and a variable to store the size of the heap
		self.heap = []
		self.size = 0

	# Method called cameFrom that takes an index as input and returns the index of its parent node
	def cameFrom(self, i):
		return (i - 1) // 2

	# Method called left_child that takes an index as input and returns the index of its left child
	def left_child(self, i):
		return 2 * i + 1

	# Method called right_child that takes an index as input and returns the index of its right child
	def right_child(self, i):
		return 2 * i + 2

	# Removes and returns the element with the lowest priority from the heap
	def extractMin(self):
		# If the size of the heap is 0, return None
		if self.size <= 0:
			return None
		# If the size of the heap is 1, remove the element and decrease the size by 1
		if self.size == 1:
			self.size -= 1
			return self.heap.pop()
		# Otherwise, remove the root element from the heap, replace it with the last element in the heap, and decrease the size by 1
		root = self.heap[0]
		last_element = self.heap.pop()
		self.size -= 1
		# If the heap is not empty, call _minHeapify to maintain the min-heap property
		if self.size > 0:
			self.heap[0] = last_element
			self._minHeapify(0)
		# Return the root element that was removed
		return root

	# Adds an element to the heap with a given priority and value
	def enqueue(self, priority, value):
		# Append the element to the end of the heap and increase the size by 1
		self.heap.append((priority, value))
		self.size += 1
		# Bubble up the element to its correct position in the heap
		i = self.size - 1
		while i != 0 and self.heap[self.cameFrom(i)][0] > self.heap[i][0]:
			self.heap[i], self.heap[self.cameFrom(i)] = self.heap[self.cameFrom(i)], self.heap[i]
			i = self.cameFrom(i)

	# Maintains the min-heap property for a given node in the heap
	def _minHeapify(self, i):
		l = self.left_child(i)
		r = self.right_child(i)
		smallest = i
		# If the left child has a lower priority than the current node, set it as the smallest
		if l < self.size and self.heap[l][0] < self.heap[i][0]:
			smallest = l
		# If the right child has a lower priority than the current node, set it as the smallest
		if r < self.size and self.heap[r][0] < self.heap[smallest][0]:
			smallest = r
		# If the smallest is not the current node, swap the elements and recursively call _minHeapify on the smallest node
		if smallest != i:
			self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
			self._minHeapify(smallest)

	# Method to return the size of the queue
	def getSize(self):
		return self.size

	# Method to return true if an item is in the queue
	def contains(self, value):
		# Iterate over the items in the queue and check if its equal
		for _, v in self.heap:
			if v == value:
				return True
		return False

	# Method to return the contents of the queue
	def toString(self):
		return str(self.heap)


def bestFirstSearch(adjacencyList, root, goal):
	# Initialize an empty set to keep track of discovered nodes.
	discovered = set()
	
	# Initialize a priority queue to store nodes to visit.
	S = PriorityQueue()
	
	# Add the starting node to the queue.
	S.put((heuristic(root, goal), root))
	
	# Initialize an empty dictionary to keep track of the path from each visited node to its predecessor.
	cameFrom = {}
	
	# Initialize a counter to keep track of the number of nodes explored during the traversal.
	nodesExplored = 0
	
	# While there are nodes in the queue:
	while not S.empty():
		
		# Pop the node with the highest priority from the queue.
		_, v = S.get()
		
		# Increment the node counter.
		nodesExplored += 1
	
		# If the current node is the goal, return the path to it and the number of nodes explored.
		if v == goal:
			return cameFrom, nodesExplored
	
		# If the current node has not been discovered yet:
		if v not in discovered:
			
			# Mark it as discovered.
			discovered.add(v)

			# For each adjacent node w:
			for w in adjacencyList[v]:
				
				# If w has already been discovered, skip it.
				if w in discovered:
					continue
				
				# Otherwise, add w to the queue with a priority based on the heuristic value and record the path from v to w.
				priority = heuristic(w, goal)
				S.put((priority, w))
				cameFrom[w] = v

	# If the goal was not reached, return 0 for the path and the number of nodes explored.
	return None, nodesExplored


def aStar(adjacencyList, root, goal):
	# Set the heuristic multiplier.
	multiplier = .8

	# Create a dictionary to hold the distances from the root to each node.
	# Initialize the distance to the root to be the heuristic distance.
	distance = defaultdict(lambda: float('inf'))
	distance[root] = heuristic(root, goal, multiplier)

	# Create a dictionary to hold the parent of each node in the shortest path from the root to that node.
	cameFrom = {root: None}

	# Create a binary heap priority queue to store the nodes.
	# Create a priority queue to store the nodes.
	# heap = heapdict()
	prioQueue = PriorityQueue()

	# Enqueue the root with a priority of 0.
	prioQueue.put((0, root))
	# heap[root] = 0

	# Keep track of the number of nodes explored.
	nodesExplored = 0

	# Create a cache for the heuristic values.
	heuristicCache = defaultdict()


	# While there are nodes in the heap.
	while not prioQueue.empty():
		# Extract the node with the lowest priority.
		# current, priority = heap.popitem()
		_, current = prioQueue.get()
		nodesExplored += 1
	
		# If the current node is the goal, return the shortest path.
		if current == goal:
			return cameFrom, nodesExplored

		# For each neighbor of the current node.
		for neighbor in adjacencyList[current]:
			# Calculate the tentative distance from the root to the neighbor through the current node.
			tentative_distance = distance[current] + 1 #heuristic(neighbor, current)

			# If the tentative distance is less than the current distance to the neighbor, update the distance.
			if tentative_distance < distance[neighbor]:
				distance[neighbor] = tentative_distance

				# Check if the heuristic value for the neighbor is already cached.
				if neighbor in heuristicCache:
					# Use the cached value.
					heuristic_value = heuristicCache[neighbor]
				else:
					# Calculate the heuristic value and cache it.
					heuristic_value = heuristic(neighbor, goal, multiplier)
					heuristicCache[neighbor] = heuristic_value

				# Calculate the priority of the neighbor as the sum of the tentative distance and the heuristic distance to the goal.
				priority = tentative_distance + heuristic_value
				# Enqueue the neighbor with the calculated priority.
				# heap[neighbor] = priority
				prioQueue.put((priority, neighbor))
				# Set the parent of the neighbor to the current node.
				cameFrom[neighbor] = current

	# If there is no path from the root to the goal, return None for the path and the number of nodes explored.
	return None, nodesExplored


# Heuristic function that calculates the manhatten distance between two nodes
def heuristic(current, goal, m=1):
	return (abs(current[0] - goal[0]) + abs(current[1] - goal[1])) * m

# Define a function to create a table of statistics.
def statsTable(algorithm, explored, adjacencyList, path, start, end):
	table = Table(title=f"Statistics for {algorithm}")
	table.add_column("[bold]Statistic")
	table.add_column("[bold]Value")
	table.add_row("Nodes visited", str(explored))
	table.add_row("Percentage of maze explored", f"{int((explored/len(adjacencyList)) * 100)}%")
	table.add_row("Solution length", str(len(path)))
	table.add_row("Time taken to solve the maze", f"{round(end-start, 5)} seconds")
	table.add_row("Solution percentage", f"[green]{int(len(path)/len(adjacencyList) * 100)}%")
	return table

def solveMaze(adjacencyList, root, goal, mazeFileName, algorithmType):
	# Determine which algorithm to use.
	if algorithmType == "DFS":
		solveFunc = depthFirstSearch
	elif algorithmType == "ASTAR":
		solveFunc = aStar
	else:
		raise ValueError(f"Invalid algorithm type '{algorithmType}'")

	# Solve the maze using the specified algorithm.
	c.print(f"\n[*] {algorithmType} Solving started...")
	start = time.time()
	solutionMap, explored = solveFunc(adjacencyList, root, goal)
	if solutionMap is not None:
		c.print(f"[*] [green]Solution found, [white]time taken: [cyan]{round(time.time() - start, 5)}\n")
		backtrackTime = time.time()
		c.print("[*] Constructing solution from map...")
		path = backtrackSolution(solutionMap, root, goal)
		c.print(f"[*] Solution constructed, time taken: {round(time.time() - backtrackTime, 5)}\n")
		end = time.time()
		# Print statistics table for solution.
		c.print(statsTable(f"{algorithmType} on {mazeFileName}", explored, adjacencyList, path, start, end))
		# Save solution to file.
		c.print("[*] Saving solution...")
		saveSolution(mazeFileName, mazeFile.copy(), path, algorithmType)
		c.print(f"[*] {algorithmType} Solution saved")
	else:
		c.print(f"[*] [red]No solution possible[white], {explored} nodes explored, {round(time.time() - start, 5)} seconds taken")


# Create a list of maze files in the current directory, exclude solution files.
availableMazeFiles = [x for x in os.listdir() if ("maze" in x and "Solution" not in x)]

# Print the available files and allow user to select a maze file.
c.print("[*] Available files:")
for i, availableMaze in enumerate(availableMazeFiles):
	c.print(f"[{i+1}] {availableMaze}")
mazeFileName = availableMazeFiles[int(c.input("\n[*] Maze: ")) - 1]


# Read maze file into memory and build adjacency list.
c.print("\n[*] Reading file into memory...")
start = time.time()
mazeFile = readMazeFile(mazeFileName)
c.print(f"[*] File read into memory, time taken: {round(time.time() - start, 5)} seconds\n")
# Make adjacency list
c.print("[*] Constructing adjacency list...")
start = time.time()
adjacencyList = buildAdjacencyList(mazeFile)
c.print(f"[*] Adjacency list built, time taken: {round(time.time() - start, 5)} seconds\n")

# Get the root and goal nodes for the maze (first and last nodes in adjacencyList)
root = list(adjacencyList.keys())[0]
goal = list(adjacencyList.keys())[-1]


# Solve maze using the two algorithms
solveMaze(adjacencyList, root, goal, mazeFileName, "DFS")
solveMaze(adjacencyList, root, goal, mazeFileName, "ASTAR")
