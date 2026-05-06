from collections import deque
from algorithms import FRONTIER, VISIT, PATH, NO_PATH


def bfs(grid, start, goal):
    queue     = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()
        yield (VISIT, (current.row, current.col))

        if current is goal:
            yield (PATH, _reconstruct(came_from, goal))
            return

        for neighbor in grid.get_neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                yield (FRONTIER, (neighbor.row, neighbor.col))
                queue.append(neighbor)

    yield (NO_PATH,)


def _reconstruct(came_from, goal):
    path = []
    node = goal
    while node is not None:
        path.append((node.row, node.col))
        node = came_from[node]
    path.reverse()
    return path
