import math
import os
import time
from astar import aStarSolver
from dfs import depthFirstSearch
from typing import Dict, List, Tuple
from queue import PriorityQueue
from collections import deque, defaultdict
from rich.table import Table
from rich.console import Console
from rich.progress import track


c = Console()


def readMazeFile(name: str) -> list:
    """
    Reads in the contents of a maze file and returns a list of strings.

    Args:
        name (str): The filename of the maze file.

    Returns:
        list: A list of strings representing the maze.
    """
    # Open the file in read mode and automatically close it when finished
    with open(name) as f:
        # Read the contents of the file as a string
        maze_str = f.read()
        # Remove any leading or trailing whitespace from the string
        maze_str = maze_str.strip()
        # Split the string into a list of strings based on the newline character
        maze_list = maze_str.split("\n")
        # Return the resulting list of strings
        return maze_list


def returnNeighbours(maze: List[List[str]], x: int, y: int) -> List[Tuple[int, int]]:
    """
    Returns the coordinates of all the neighboring cells that are valid paths (represented by a `-` character).

    Args:
        maze (list[list[str]]): A 2D list of strings representing the maze.
        x (int): The x-coordinate of the cell in the maze.
        y (int): The y-coordinate of the cell in the maze.

    Returns:
        list[tuple[int, int]]: A list of coordinates of all the neighboring cells that are valid paths.
    """
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


def buildAdjacencyList(maze: List[List[str]]) -> defaultdict:
    """
    Build an adjacency list representation of the given maze.
    
    Args:
        maze (list of lists): A 2D grid representation of the maze, where "-" represents a wall and " " represents a path
    
    Returns:
        adjacencyList (defaultdict): A defaultdict where each key is a tuple representing a cell in the maze, and the value is a list of its neighbours
    """
    bounds = (0, len(maze), 0, len(maze[0])) # set the bounds of the maze as a tuple
    
    adjacencyList = defaultdict(list) # initialize an empty defaultdict to store the adjacency list representation of the maze
    
    for y in range(bounds[1]): # loop through all rows in the maze
        for x in range(0, bounds[3], 2): # loop through every other column in the maze
            if maze[y][x] == "-": # if the current cell is a wall, add its neighbours to the adjacency list
                adjacencyList[(x, y)] = returnNeighbours(maze, x, y)
    
    return adjacencyList


def backtrackSolution(solutionMap: dict, root: Tuple, goal: Tuple) -> list:
    """
    Trace the solution path from the goal to the root node using the provided solution map.

    Args:
        solutionMap (dict): A dictionary where each key is a node and each value is the node that leads to it in a solution path.
        root: The starting node in the solution path.
        goal: The end node in the solution path.

    Returns:
        path (set): A set of nodes representing the solution path from the goal to the root node.
    """
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
    return set(path)


def saveSolution(mazeFileName: str, maze: list, solution: list, algorithm: str) -> None:
    """
    Takes a maze file name, the maze itself, the solution path, and the algorithm used to find the solution.
    Modifies the maze by replacing the characters on the solution path with an 'X' and saves the modified maze 
    as a new file with the original maze file name, algorithm used, and "-Solution" appended to the file name.

    Args:
        mazeFileName (str): The name of the original maze file.
        maze (list): A list of strings representing the maze.
        solution (list): A list of tuples representing the nodes in the solution path.
        algorithm (str): A string representing the algorithm used to find the solution.

    Returns:
        bool: if the function completes its execution

    Raises:
        Raises an exception if the file can't be saved
    """

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

    directory = "solutions/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        # Open a file with a name that includes the original maze file name, the name of the algorithm used, and the string "-Solution" 
        with open(f"{directory}{mazeFileName.split('.')[0]}-{algorithm}-Solution.txt", "w") as file:
            # Write the output string to the file
            file.write(outputString)
    except Exception as e:
        c.print(f"\n[*] Error in saving file, {e}")


    return True


def statsTable(algorithm: str, explored: int, adjacencyList: list, path: list, start: float, end: float) -> Table:
    """
    Creates a table of statistics for a given algorithm run on a maze.

    Parameters:
        algorithm (str): The name of the algorithm used to solve the maze.
        explored (int): The number of nodes visited during the algorithm's execution.
        adjacencyList (list): The adjacency list representation of the maze.
        path (list): The solution path obtained by the algorithm.
        start (float): The start time of the algorithm.
        end (float): The end time of the algorithm.

    Returns:
        Table: A rich Table object containing the statistics of the algorithm execution.
    """

    # Create a new table object with the title being the name of the algorithm
    table = Table(title=f"Statistics for {algorithm}")

    # Add columns for the statistic and its value
    table.add_column("[bold]Statistic")
    table.add_column("[bold]Value")

    # Add rows for the various statistics being measured
    table.add_row("Nodes visited", str(explored))
    table.add_row("Percentage of maze explored", f"{int((explored/len(adjacencyList)) * 100)}%")
    table.add_row("Solution length", str(len(path)))
    table.add_row("Time taken to solve the maze", f"{round(end-start, 7)} seconds")
    table.add_row("Solution percentage", f"[green]{int(len(path)/len(adjacencyList) * 100)}%")

    # Return the table object
    return table


def solveMaze(adjacencyList: Dict[int, List[Tuple[int, int]]], root: int, goal: int,
              mazeFileName: str, algorithmType: str, print: bool = True) -> Tuple[float, str]:
    """
    Solves a maze using the specified algorithm and prints/saves the solution if needed.

    Parameters:
        adjacencyList (Dict[int, List[Tuple[int, int]]]): The adjacency list of the maze, where each key is a node
          and each value is a list of adjacent nodes and their corresponding edge weights.
        root (int): The starting node for the maze.
        goal (int): The goal node for the maze.
        mazeFileName (str): The name of the maze file.
        algorithmType (str): The type of algorithm to use. Must be either "DFS" or "ASTAR".
        print (bool, optional): Whether to print the solution or not. Default is True.

    Returns:
        Tuple[float, str]: A tuple containing the time taken to solve the maze and the statistics table for the solution.

    Raises:
        ValueError: If the specified algorithm type is not valid.
    """

    # Determine which algorithm to use.
    if algorithmType == "DFS":
        solveFunc = depthFirstSearch
    elif algorithmType == "ASTAR":
        solveFunc = aStarSolver
    else:
        raise ValueError(f"Invalid algorithm type '{algorithmType}'")

    # Solve the maze using the specified algorithm.
    if print:
        c.print(f"\n[*] {algorithmType} Solving started...")

    start = time.time()
    solutionMap, explored = solveFunc(adjacencyList, root, goal)
    if solutionMap is not None:
        if print:
            c.print(f"[*] [green]Solution found, [white]time taken: [cyan]{round(time.time() - start, 5)}\n")
        backtrackTime = time.time()
        if print:
            c.print("[*] Constructing solution from map...")
        path = backtrackSolution(solutionMap, root, goal)
        if print:
            c.print(f"[*] Solution constructed, time taken: {round(time.time() - backtrackTime, 5)}\n")
        end = time.time()

        # Print statistics table for solution.
        if print:
            c.print(statsTable(f"{algorithmType} on {mazeFileName}", explored, adjacencyList, path, start, end))
        # Save solution to file.
        if print:
            c.print("[*] Saving solution...")
        saved = saveSolution(mazeFileName, mazeFile.copy(), path, algorithmType)
        if print:
            if saved:
                c.print(f"[*] {algorithmType} Solution saved in /solutions/ directory")
            else:
                c.print(f"[*] Solution failed to save")

    else:
        # If no solution is found.
        c.print(f"[*] [red]No solution possible[white], {explored} nodes explored, {round(time.time() - start, 5)} seconds taken")
    return end - start, statsTable(f"{algorithmType} on {mazeFileName}", explored, adjacencyList, path, start, end)



if __name__ == "__main__":
    # Create a list of maze files in the current directory, exclude solution files.
    availableMazeFiles = [x for x in os.listdir() if ("maze" in x and "Solution" not in x)]

    # Print the available files and allow user to select a maze file.
    c.print("[*] Available files:")
    for i, availableMaze in enumerate(availableMazeFiles):
        c.print(f"[{i+1}] {availableMaze}")

    # Get the users input
    mazeFileName = availableMazeFiles[int(c.input("\n[*] Maze: ")) - 1]

    # Define the amount of times the algorithms will run
    runs = 0

    # Prompt the user for an input
    a = c.input("\n[*] Average solving time over x runs? (y/n) ").lower()

    average = True if a == "y" else False
    
    # If the user chose to run the algorithms multiple times, ask them how many
    if average:
        runs = int(c.input("\n[*] Amount of runs: "))


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
    if average:
        # If the algorithms need to be run multiple times, store the time taken to solve the maze
        DFSVals = []
        ASTARvals = []

        # Store the stats for the table
        DFSstats = None
        ASTARstats = None

        # Run the algorithms
        for i in track(range(runs), description="[*] Solving mazes..."):
            DFStime, DFSstats = (solveMaze(adjacencyList, root, goal, mazeFileName, "DFS", False))
            ASTARtime, ASTARstats = (solveMaze(adjacencyList, root, goal, mazeFileName, "ASTAR", False))
            DFSVals.append(DFStime)
            ASTARvals.append(ASTARtime)

        # Create a table for the averaged times
        table = Table(title=f"Time statistics over {runs} runs")

        # Add columns to the table
        table.add_column("[bold]Algorithm")
        table.add_column("[bold]Average time")
        table.add_column("[bold]Minimum time")
        table.add_column("[bold]Maximum time")

        # Add the various statistics (algorithm, average time, minimum time, maximum time)
        table.add_row("A*", str(round(sum(ASTARvals)/len(ASTARvals), 7)), str(round(min(ASTARvals),7)), str(round(max(ASTARvals),7)))
        table.add_row("DFS", str(round(sum(DFSVals)/len(DFSVals), 7)), str(round(min(DFSVals),7)), str(round(max(DFSVals),7)))
        
        # Print the table
        c.print("\n")
        c.print(table)

        # if i == runs-1:
        # Print the statistics for a single run
        c.print("\n[*] Statistics for a single run:\n")
        c.print(DFSstats)

        c.print(ASTARstats)

        c.print("\n[*] Solutions saved in /solutions/ directory")        

    else:
        solveMaze(adjacencyList, root, goal, mazeFileName, "DFS")
        solveMaze(adjacencyList, root, goal, mazeFileName, "ASTAR")