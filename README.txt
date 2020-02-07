### Uninformed:

1. IDS/BFS: Try and compare.

### Informed Search(A*):

1. h1: sum of Manhattan distance
2. h2: n-Max Swap Assume you can swap any tile with the ‘space’. Use the cost of the optimal solution to this problem as a heuristic for the 8-puzzle.
3. h3: Number of tiles out of row + Number of tiles out of column

### Empirical Experiments:
1. How to test solvable: https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable