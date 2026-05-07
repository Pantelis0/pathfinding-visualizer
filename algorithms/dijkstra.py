import heapq
from algorithms import FRONTIER, VISIT, PATH, NO_PATH


def dijkstra(grid, start, goal):
    # heap entries: (cost, row, col, cell)
    # row+col included so the heap never needs to compare Cell objects
    heap      = [(0, start.row, start.col, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while heap:
        cost, _, _, current = heapq.heappop(heap)

        # skip stale heap entries
        if cost > cost_so_far.get(current, float("inf")):
            continue

        yield (VISIT, (current.row, current.col))

        if current is goal:
            yield (PATH, _reconstruct(came_from, goal))
            return

        for neighbor in grid.get_neighbors(current):
            new_cost = cost_so_far[current] + neighbor.weight
            if new_cost < cost_so_far.get(neighbor, float("inf")):
                cost_so_far[neighbor] = new_cost
                came_from[neighbor]   = current
                yield (FRONTIER, (neighbor.row, neighbor.col))
                heapq.heappush(heap, (new_cost, neighbor.row, neighbor.col, neighbor))

    yield (NO_PATH,)


def _reconstruct(came_from, goal):
    path = []
    node = goal
    while node is not None:
        path.append((node.row, node.col))
        node = came_from[node]
    path.reverse()
    return path
