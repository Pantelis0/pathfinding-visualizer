from algorithms import FRONTIER, VISIT, PATH, NO_PATH


def dfs(grid, start, goal):
    stack     = [start]
    came_from = {start: None}

    while stack:
        current = stack.pop()
        yield (VISIT, (current.row, current.col))

        if current is goal:
            yield (PATH, _reconstruct(came_from, goal))
            return

        for neighbor in grid.get_neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                yield (FRONTIER, (neighbor.row, neighbor.col))
                stack.append(neighbor)

    yield (NO_PATH,)


def _reconstruct(came_from, goal):
    path = []
    node = goal
    while node is not None:
        path.append((node.row, node.col))
        node = came_from[node]
    path.reverse()
    return path
