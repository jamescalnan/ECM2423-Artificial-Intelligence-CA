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
	return open(name).read().strip().split("\n")


def returnNeighbours(maze, x, y):
	# Initialize an empty list to hold the neighbors of the given cell
	neighbours = []


	# Check the cell above the given cell
	if y - 1 >= 0 and maze[y - 1][x] == "-":
		# If the above cell is within the boundaries of the maze and is a valid path, add it to the list of neighbors
		neighbours.append((x, y - 1))

	# Check the cell to the right of the given cell
	if maze[y][x + 2] == "-":
		# If the cell to the right is a valid path, add it to the list of neighbors
		neighbours.append((x + 2, y))

	# Check the cell to the left of the given cell
	if maze[y][x - 2] == "-":
		# If the cell to the left is a valid path, add it to the list of neighbors
		neighbours.append((x - 2, y))

	# Check the cell below the given cell
	if not (y + 1) == len(maze) and maze[y + 1][x] == "-":
		# If the below cell is within the boundaries of the maze and is a valid path, add it to the list of neighbors
		neighbours.append((x, y + 1))

	# Return the list of neighbors
	return neighbours





def buildAdjacencyList(maze):
	adjacencyList = {}

	for y in range(len(maze)):
		for x in range(len(maze[y])):
			# Iterate over each point in the maze
			if maze[y][x] == "-":
				# Check if the current point is a node and if so add the current nodes neighbours to the dictionary
				adjacencyList[(x, y)] = returnNeighbours(maze, x, y)

	# Return the adjacency list
	return adjacencyList



def depthFirstSearch(adjacencyList, root, goal):
	# Initialize an empty list to hold the vertices that have been discovered
	discovered = []
	# Initialize an empty stack to hold the vertices to be explored
	S = []
	# Initialize an empty dictionary to hold the vertices that lead to each discovered vertex
	cameFrom = {}

	# Add the root vertex to the stack
	S.append(root)

	# Initialize a counter to keep track of the number of nodes explored
	nodesExplored = 0

	# While there are still vertices to be explored
	while len(S) > 0:
		# Pop a vertex from the stack
		v = S.pop()
		# Increment the counter
		nodesExplored += 1

		# If the goal has been reached, return the cameFrom dictionary and the number of nodes explored
		if v == goal:
			return cameFrom, nodesExplored

		# If the vertex has not been discovered yet
		if v not in discovered:
			# Add it to the list of discovered vertices
			discovered.append(v)

			# For each neighbor of the current vertex
			for w in adjacencyList[v]:
				# If the neighbor has already been discovered, skip it
				if w in discovered:
					continue

				# Add the neighbor to the stack to be explored
				S.append(w)
				# Record the current vertex as the one that leads to the neighbor
				cameFrom[w] = v

	# If the goal was not found, return 0 for both the cameFrom dictionary and the number of nodes explored
	return 0, nodesExplored



def backtrackSolution(solutionMap, root, goal):
	# Set the current vertex to be the goal
	current = goal
	# Initialize a list to hold the path from the goal to the root
	path = [goal]

	# While the current vertex is not the root
	while not current == root:
		# Append the current vertex to the path
		path.append(current)
		# Set the current vertex to be the vertex that leads to it in the solution map
		current = solutionMap[current]

	# Append the root vertex to the path
	path.append(root)

	# Return the path from the goal to the root
	return path



def saveSolution(mazeFileName, maze, solution, algorithm):
	# Initialize an empty string to hold the output
	outputString = ''

	# For each vertex in the solution path
	for vertex in solution:
		# Get the x and y coordinates of the vertex
		x, y = vertex
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
	# Define an init method which is called when an object of the class is instantiated
    def __init__(self):
    	# Initialize an empty list to store the heap and a variable to store the size of the heap
        self.heap = []
        self.size = 0

    # Define a method called cameFrom that takes an index as input and returns the index of its parent node
    def cameFrom(self, i):
        return (i - 1) // 2

    # Define a method called left_child that takes an index as input and returns the index of its left child
    def left_child(self, i):
        return 2 * i + 1

    # Define a method called right_child that takes an index as input and returns the index of its right child
    def right_child(self, i):
        return 2 * i + 2

    # Define a method called extractMin that removes and returns the element with the lowest priority from the heap
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

    # Define a method called enqueue that adds an element to the heap with a given priority and value
    def enqueue(self, priority, value):
    	# Append the element to the end of the heap and increase the size by 1
        self.heap.append((priority, value))
        self.size += 1
        # Bubble up the element to its correct position in the heap
        i = self.size - 1
        while i != 0 and self.heap[self.cameFrom(i)][0] > self.heap[i][0]:
            self.heap[i], self.heap[self.cameFrom(i)] = self.heap[self.cameFrom(i)], self.heap[i]
            i = self.cameFrom(i)

    # Define a method called _minHeapify that maintains the min-heap property for a given node in the heap
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

    # Define a method to return the size of the queue
    def getSize(self):
        return self.size

    # Define a method to return true if an item is in the queue
    def contains(self, value):
    	# Iterate over the items in the queue and check if its equal
        for _, v in self.heap:
            if v == value:
                return True
        return False

    # Define a method to return the contents of the queue
    def toString(self):
        return str(self.heap)


def aStar(adjacencyList, root, goal):
	# Set the heuristic multiplier to 10.
	multiplier = 10

	# Create a dictionary to hold the distances from the root to each vertex.
	# Initialize the distance to the root to be the heuristic distance.
	distance = {root: heuristic(root, goal, multiplier)}

	# Create a dictionary to hold the parent of each vertex in the shortest path from the root to that vertex.
	cameFrom = {root: None}

	# Create a binary heap priority queue to store the vertices.
	heap = BinaryHeapPriorityQueue()

	# Enqueue the root with a priority of 0.
	heap.enqueue(0, root)

	# Keep track of the number of nodes explored.
	nodesExplored = 0

	# While there are vertices in the heap.
	while heap.getSize() > 0:
		# Extract the vertex with the lowest priority.
		current = heap.extractMin()[1]
		nodesExplored += 1
	
		# If the current vertex is the goal, return the shortest path.
		if current == goal:
			return cameFrom, nodesExplored

		# For each neighbor of the current vertex.
		for neighbor in adjacencyList[current]:
			# Calculate the tentative distance from the root to the neighbor through the current vertex.
			tentative_distance = distance[current] + heuristic(neighbor, current)

			# If the tentative distance is less than the current distance to the neighbor, update the distance.
			if neighbor not in distance or tentative_distance < distance[neighbor]:
				distance[neighbor] = tentative_distance
				# Calculate the priority of the neighbor as the sum of the tentative distance and the heuristic distance to the goal.
				priority = tentative_distance + heuristic(neighbor, goal, multiplier)
				# Enqueue the neighbor with the calculated priority.
				heap.enqueue(priority, neighbor)

				# Set the parent of the neighbor to the current vertex.
				cameFrom[neighbor] = current

	# If there is no path from the root to the goal, return 0 for the path and the number of nodes explored.
	return 0, nodesExplored

# Heuristic function that calculates the manhatten distance between two points
def heuristic(current, goal, m=1):
	return (abs(current[0] - goal[0]) + abs(current[1] - goal[1])) * m




# Create a list of maze files in the current directory, exclude solution files.
availableMazeFiles = [x for x in os.listdir() if ("maze" in x and "Solution" not in x)]

# Print the available files and allow user to select a maze file.
c.print("[*] Available files:")
for i, availableMaze in enumerate(availableMazeFiles):
	c.print(f"[{i+1}] {availableMaze}")
mazeFileName = availableMazeFiles[int(c.input("\n[*] Maze: ")) - 1]

# Read maze file into memory and build adjacency list.
c.print("\n[*] Reading file into memory...")
mazeFile = readMazeFile(mazeFileName)
c.print("[*] File read into memory\n")
c.print("[*] Constructing adjacency list...")
adjacencyList = buildAdjacencyList(mazeFile)
c.print("[*] Adjacency list built\n")

# Get the root and goal nodes for the maze (first and last nodes in adjacencyList)
root = list(adjacencyList.keys())[0]
goal = list(adjacencyList.keys())[-1]

# Define a function to create a table of statistics.
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

# Use depth-first search to solve the maze.
c.print("\n[*] DFS Solving started...")
DFS_start = time.time()
DFS_solutionMap, DFS_explored = depthFirstSearch(adjacencyList, root, goal)
if DFS_solutionMap != 0:
	c.print("[*] [green] Solution found\n")
	c.print("[*] Constructing solution from map...")
	DFS_path = backtrackSolution(DFS_solutionMap, root, goal)
	c.print("[*] Solution constructed\n")
	DFS_end = time.time()
	# Print statistics table for DFS solution.
	c.print(statsTable(f"DFS on {mazeFileName}", DFS_explored, adjacencyList, DFS_path, DFS_start, DFS_end))
	# Save DFS solution to file.
	c.print("[*] Saving solution...")
	saveSolution(mazeFileName, mazeFile.copy(), DFS_path, "DFS")
	c.print("[*] DFS Solution saved")
else:
	c.print(f"[*] [red]No solution possible[white], {DFS_explored} vertices explored")

# Use A* algorithm to solve the maze.
c.print("\n\n[*] A* Solving started...")
ASTAR_start = time.time()
ASTAR_solutionMap, ASTAR_explored = aStar(adjacencyList, root, goal)
if ASTAR_solutionMap != 0:
	c.print("[*] Constructing solution from map...")
	ASTAR_path = backtrackSolution(ASTAR_solutionMap, root, goal)
	c.print("[*] Solution constructed\n")
	ASTAR_end = time.time()
	# Print statistics table for A* solution.
	c.print(statsTable(f"A* on {mazeFileName}", ASTAR_explored, adjacencyList, ASTAR_path, ASTAR_start, ASTAR_end))
	# Save A* solution to file.
	c.print("[*] Saving solution...")
	saveSolution(mazeFileName, mazeFile.copy(), ASTAR_path, "DFS")
	c.print("[*] A* Solution saved")
else:
	c.print(f"[*] [red]No solution possible[white], {ASTAR_explored} vertices explored")


