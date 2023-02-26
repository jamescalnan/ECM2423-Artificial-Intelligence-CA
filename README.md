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

Install the rich library by running the following command:
```bash
pip install rich
```
Wait for the package installation process to complete.

Verify that the package was installed successfully by running the following command:
```bash
pip show rich
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

[*] Reading file into memory...
[*] File read into memory, time taken: 0.00408 seconds

[*] Constructing adjacency list...
[*] Adjacency list built, time taken: 0.12608 seconds


[*] DFS Solving started...
[*] Solution found, time taken: 0.05004

[*] Constructing solution from map...
[*] Solution constructed, time taken: 0.001

      Statistics for DFS on maze-Large.txt
┌──────────────────────────────┬───────────────┐
│ Statistic                    │ Value         │
├──────────────────────────────┼───────────────┤
│ Vertices visited             │ 70512         │
│ Percentage of maze explored  │ 85%           │
│ Solution length              │ 1051          │
│ Time taken to solve the maze │ 0.055 seconds │
│ Solution percentage          │ 1%            │
└──────────────────────────────┴───────────────┘
[*] Saving solution...
[*] DFS Solution saved

[*] ASTAR Solving started...
[*] Solution found, time taken: 0.21654

[*] Constructing solution from map...
[*] Solution constructed, time taken: 0.0021

     Statistics for ASTAR on maze-Large.txt
┌──────────────────────────────┬────────────────┐
│ Statistic                    │ Value          │
├──────────────────────────────┼────────────────┤
│ Vertices visited             │ 41752          │
│ Percentage of maze explored  │ 50%            │
│ Solution length              │ 975            │
│ Time taken to solve the maze │ 0.2235 seconds │
│ Solution percentage          │ 1%             │
└──────────────────────────────┴────────────────┘
[*] Saving solution...
[*] ASTAR Solution saved
```

In this case, the maze solutions will then be saved in their respective directories as the following:

```bash
maze-Large-ASTAR-Solution.txt
maze-Large-DFS-Solution.txt
```

# Author
- James Calnan

# License
MIT License


