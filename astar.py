from heapq import heappush, heappop
from typing import Dict, List, Tuple
from collections import defaultdict

def aStarSolver(adjacencyList: Dict[str, List[str]], root: str, goal: str) -> Tuple[Dict[str, str], int]:
	"""
	A* algorithm implementation to find the shortest path between two nodes in a graph.

	Args:
		adjacencyList (dictionary of list): a dictionary that maps each node in the graph to a list of its adjacent nodes.
		root (tuple): the node to start the search from.
		goal (tuple): the node to search for.

	Returns:
		If the goal node is found, returns a tuple containing a dictionary that maps each visited node to its parent in the search tree, and the number of nodes explored during the traversal.
		If the goal node is not found, returns a tuple containing None for the path dictionary, and the number of nodes explored during the traversal.
	"""


	# Set the heuristic multiplier.
	multiplier = .8

	# Create a dictionary to hold the distances from the root to each node.
	# Initialize the distance to the root to be the heuristic distance.
	distance = defaultdict(lambda: float('inf'))
	distance[root] = heuristic(root, goal, multiplier)

	# Create a dictionary to hold the parent of each node in the shortest path from the root to that node.
	cameFrom = {root: None}

	# Create a binary heap priority queue to store the nodes.
	prioQueue = []

	# Enqueue the root with a priority of 0.
	heappush(prioQueue, (0, root))

	# Keep track of the number of nodes explored.
	nodesExplored = 0

	# Create a cache for the heuristic values.
	heuristicCache = defaultdict()


	# While there are nodes in the heap.
	while prioQueue:
		# Extract the node with the lowest priority.
		_, current = heappop(prioQueue)
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
				heappush(prioQueue, (priority, neighbor))
				# Set the parent of the neighbor to the current node.
				cameFrom[neighbor] = current

	# If there is no path from the root to the goal, return None for the path and the number of nodes explored.
	return None, nodesExplored


def heuristic(current: Tuple[int, int], goal: Tuple[int, int], m: int = 1) -> int:
	"""
	Calculate the Manhattan distance between two nodes.

	Args:
		current (Tuple[int, int]): The current node.
		goal (Tuple[int, int]): The goal node.
		m (int): The weight to multiply the Manhattan distance by.

	Returns:
		int: The calculated heuristic value.
	"""
	return (abs(current[0] - goal[0]) + abs(current[1] - goal[1])) * m