import random
from grid import State

WEIGHTED_COST = 5


def generate_maze(grid):
    """Fill the grid with a perfect maze using recursive backtracker (DFS).

    Rooms sit at even-coordinate cells; odd-coordinate cells are the walls
    between them. With a 40x40 grid this gives a 20x20 room grid.
    Start and goal are placed in opposite corners after carving.
    """
    # fill everything with walls
    for r in range(grid.rows):
        for c in range(grid.cols):
            grid.get(r, c).state  = State.WALL
            grid.get(r, c).weight = 1

    # rooms are at even (r, c) positions
    visited = set()

    def neighbors(r, c):
        """Room neighbors 2 steps away that are still inside the grid."""
        dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        result = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid.rows and 0 <= nc < grid.cols:
                result.append((nr, nc))
        return result

    def carve(r, c):
        visited.add((r, c))
        grid.get(r, c).state = State.EMPTY
        nbrs = neighbors(r, c)
        random.shuffle(nbrs)
        for nr, nc in nbrs:
            if (nr, nc) not in visited:
                # carve the wall between current room and neighbor
                wall_r = (r + nr) // 2
                wall_c = (c + nc) // 2
                grid.get(wall_r, wall_c).state = State.EMPTY
                carve(nr, nc)

    # start carving from top-left room
    import sys
    sys.setrecursionlimit(10000)
    carve(0, 0)

    # place start top-left, goal bottom-right (nearest even cell)
    sr = 0
    sc = 0
    gr = grid.rows - 1 if grid.rows % 2 == 1 else grid.rows - 2
    gc = grid.cols - 1 if grid.cols % 2 == 1 else grid.cols - 2

    grid.get(sr, sc).state = State.START
    grid.get(gr, gc).state = State.GOAL


def paint_weighted(grid, cell):
    """Mark a cell as weighted terrain (passable, high cost)."""
    if cell.state in (State.EMPTY,):
        cell.state  = State.WEIGHTED
        cell.weight = WEIGHTED_COST


def erase_weighted(grid, cell):
    """Revert a weighted cell back to empty."""
    if cell.state == State.WEIGHTED:
        cell.state  = State.EMPTY
        cell.weight = 1
