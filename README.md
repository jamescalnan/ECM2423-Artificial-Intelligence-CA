# ECM2423 Artificial Intelligence CA
 Coursework

## Setup

The rich console library was used to make console outputs more readable
```bash
rich.table
rich.console
```

Prerequisites
Python 3.6 or higher
Pip package installer

Installation Steps
Open a terminal window on your computer.

Install the rich and typing library by running the following command:
```bash
pip install rich
pip install typing
```
Wait for the package installation process to complete.

Verify that the packages were installed successfully by running the following commands:
```bash
pip show rich
pip show typing
```

## Run

To run the program, place the maze text files in the same directory as main.py.

Then run the program with the following command:

```bash
py main.py
```

You will then be prompted to select which maze to run DFS and A* on

```bash
[*] Available files:
[1] maze-Easy.txt
[2] maze-Large.txt
[3] maze-Medium.txt
[4] maze-VLarge.txt

[*] Maze:
```


Inputting option 2 will yield the following output:

```bash
[*] Maze: 2

[*] Average solving time over x runs? (y/n) n

[*] Reading file into memory...
[*] File read into memory, time taken: 0.002 seconds

[*] Constructing adjacency list...
[*] Adjacency list built, time taken: 0.11004 seconds


[*] DFS Solving started...
[*] Solution found, time taken: 0.05005

[*] Constructing solution from map...
[*] Solution constructed, time taken: 0.001

        Statistics for DFS on maze-Large.txt
┌──────────────────────────────┬───────────────────┐
│ Statistic                    │ Value             │
├──────────────────────────────┼───────────────────┤
│ Nodes visited                │ 70512             │
│ Percentage of maze explored  │ 85%               │
│ Solution length              │ 1051              │
│ Time taken to solve the maze │ 0.0580637 seconds │
│ Solution percentage          │ 1%                │
└──────────────────────────────┴───────────────────┘
[*] Saving solution...
[*] DFS Solution saved

[*] ASTAR Solving started...
[*] Solution found, time taken: 0.09303

[*] Constructing solution from map...
[*] Solution constructed, time taken: 0.001

       Statistics for ASTAR on maze-Large.txt
┌──────────────────────────────┬───────────────────┐
│ Statistic                    │ Value             │
├──────────────────────────────┼───────────────────┤
│ Nodes visited                │ 41752             │
│ Percentage of maze explored  │ 50%               │
│ Solution length              │ 975               │
│ Time taken to solve the maze │ 0.0979979 seconds │
│ Solution percentage          │ 1%                │
└──────────────────────────────┴───────────────────┘
[*] Saving solution...
[*] ASTAR Solution saved
```

You can also choose to run the two algorithms on the same maze any number of times and then average the time taken to solve the maze:

```bash
[*] Average solving time over x runs? (y/n) y

[*] Amount of runs: 100

[*] Reading file into memory...
[*] File read into memory, time taken: 0.001 seconds

[*] Constructing adjacency list...
[*] Adjacency list built, time taken: 0.11704 seconds

[*] Solving mazes... ---------------------------------------- 100% 0:00:00

[*] DFS stats over 100 runs: average: 0.0493907, min: 0.0459976

[*] A* stats over 100 runs: average: 0.0930812, min: 0.0889952

[*] Stats for a single run
        Statistics for DFS on maze-Large.txt
┌──────────────────────────────┬───────────────────┐
│ Statistic                    │ Value             │
├──────────────────────────────┼───────────────────┤
│ Nodes visited                │ 70512             │
│ Percentage of maze explored  │ 85%               │
│ Solution length              │ 1051              │
│ Time taken to solve the maze │ 0.0510449 seconds │
│ Solution percentage          │ 1%                │
└──────────────────────────────┴───────────────────┘
       Statistics for ASTAR on maze-Large.txt
┌──────────────────────────────┬───────────────────┐
│ Statistic                    │ Value             │
├──────────────────────────────┼───────────────────┤
│ Nodes visited                │ 41752             │
│ Percentage of maze explored  │ 50%               │
│ Solution length              │ 975               │
│ Time taken to solve the maze │ 0.0919619 seconds │
│ Solution percentage          │ 1%                │
└──────────────────────────────┴───────────────────┘
```



In this case, the maze solutions will then be saved in the same directory as the python file, the names of the solutions will be:

```bash
maze-Large-ASTAR-Solution.txt
maze-Large-DFS-Solution.txt
```

# Author
- James Calnan

# License
MIT License


