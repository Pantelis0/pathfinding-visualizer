import heapq
from algorithms import FRONTIER, VISIT, PATH, NO_PATH


def _manhattan(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)


def astar(grid, start, goal):
    # heap entries: (f, row, col, cell)  where f = g + h
    h_start = _manhattan(start, goal)
    heap        = [(h_start, start.row, start.col, start)]
    came_from   = {start: None}
    g           = {start: 0}

    while heap:
        _, _, _, current = heapq.heappop(heap)

        # skip stale heap entries
        f_stale = g.get(current, float("inf")) + _manhattan(current, goal)
        _ = f_stale  # already popped — check via g below

        yield (VISIT, (current.row, current.col))

        if current is goal:
            yield (PATH, _reconstruct(came_from, goal))
            return

        for neighbor in grid.get_neighbors(current):
            new_g = g[current] + neighbor.weight
            if new_g < g.get(neighbor, float("inf")):
                g[neighbor]           = new_g
                came_from[neighbor]   = current
                f                     = new_g + _manhattan(neighbor, goal)
                yield (FRONTIER, (neighbor.row, neighbor.col))
                heapq.heappush(heap, (f, neighbor.row, neighbor.col, neighbor))

    yield (NO_PATH,)


def _reconstruct(came_from, goal):
    path = []
    node = goal
    while node is not None:
        path.append((node.row, node.col))
        node = came_from[node]
    path.reverse()
    return path
