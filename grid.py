from enum import Enum, auto


class State(Enum):
    EMPTY    = auto()
    WALL     = auto()
    START    = auto()
    GOAL     = auto()
    VISITED  = auto()
    FRONTIER = auto()
    PATH     = auto()


class Cell:
    def __init__(self, row, col, weight=1):
        self.row    = row
        self.col    = col
        self.state  = State.EMPTY
        self.weight = weight

    def __repr__(self):
        return f"Cell({self.row},{self.col},{self.state.name})"


class Grid:
    def __init__(self, rows, cols):
        self.rows   = rows
        self.cols   = cols
        self._cells = [[Cell(r, c) for c in range(cols)] for r in range(rows)]

    def get(self, row, col):
        return self._cells[row][col]

    def set_state(self, row, col, state):
        self._cells[row][col].state = state

    def get_neighbors(self, cell):
        """Return the 4-directional non-wall neighbors of cell."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            r, c = cell.row + dr, cell.col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                neighbor = self._cells[r][c]
                if neighbor.state != State.WALL:
                    neighbors.append(neighbor)
        return neighbors

    def reset(self):
        """Clear the entire grid back to empty."""
        for row in self._cells:
            for cell in row:
                cell.state  = State.EMPTY
                cell.weight = 1

    def clear_search(self):
        """Remove visited/frontier/path markings but keep walls, start, and goal."""
        transient = {State.VISITED, State.FRONTIER, State.PATH}
        for row in self._cells:
            for cell in row:
                if cell.state in transient:
                    cell.state = State.EMPTY
