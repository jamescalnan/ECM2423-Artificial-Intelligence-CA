from collections import deque, defaultdict
from typing import Dict, List, Tuple


def depthFirstSearch(adjacencyList: Dict[Tuple, List[Tuple]], root: Tuple, goal: Tuple) -> Tuple[Dict[Tuple, Tuple], int]:
    """
    Traverses a graph represented by an adjacency list, starting from a specified root node, and searches for a goal node.
    
    Args:
    	adjacencyList (dictionary of list): a dictionary that maps each node in the graph to a list of its adjacent nodes.
    	root (tuple): the node to start the search from.
    	goal (tuple): the node to search for.
    
    Returns:
    	If the goal node is found, returns a tuple containing a dictionary that maps each visited node to its parent in the search tree, and the number of nodes explored during the traversal.
    	If the goal node is not found, returns a tuple containing None for the path dictionary, and the number of nodes explored during the traversal.
    """
    
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
