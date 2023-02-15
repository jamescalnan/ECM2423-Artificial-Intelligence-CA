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
python -c "import rich; print(rich.__version__)"
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
[*] File read into memory

[*] Constructing adjacency list...
[*] Adjacency list built


[*] DFS Solving started...
[*] Solution found

[*] Constructing solution from map...
[*] Solution constructed

       Statistics for DFS on maze-Large.txt
┌──────────────────────────────┬─────────────────┐
│ Statistic                    │ Value           │
├──────────────────────────────┼─────────────────┤
│ Vertices visited             │ 10939           │
│ Percentage of maze explored  │ 13%             │
│ Solution length              │ 1121            │
│ Time taken to solve the maze │ 3.55459 seconds │
│ Solution percentage          │ 1%              │
└──────────────────────────────┴─────────────────┘
[*] Saving solution...
[*] DFS Solution saved


[*] A* Solving started...
[*] Solution found

[*] Constructing solution from map...
[*] Solution constructed

      Statistics for A* on maze-Large.txt
┌──────────────────────────────┬───────────────┐
│ Statistic                    │ Value         │
├──────────────────────────────┼───────────────┤
│ Vertices visited             │ 14405         │
│ Percentage of maze explored  │ 17%           │
│ Solution length              │ 1097          │
│ Time taken to solve the maze │ 0.128 seconds │
│ Solution percentage          │ 1%            │
└──────────────────────────────┴───────────────┘
[*] Saving solution...
[*] A* Solution saved
```

In this case, the maze solutions will then be saved in the following files:

```bash
maze-Large-ASTAR-Solution.txt
maze-Large-DFS-Solution.txt
```




