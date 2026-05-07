import pygame
from grid import Grid, State
from visualizer import Visualizer
from algorithms import FRONTIER, VISIT, PATH, NO_PATH
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar

ROWS      = 40
COLS      = 40
CELL_SIZE = 20

ALGO_NAMES = {
    pygame.K_1: "BFS",
    pygame.K_2: "DFS",
    pygame.K_3: "Dijkstra",
    pygame.K_4: "A*",
}

# Steps consumed per frame — increase to speed up animation
STEPS_PER_FRAME = 1


def cell_at(grid, cell_size, mouse_pos):
    x, y = mouse_pos
    col = x // cell_size
    row = y // cell_size
    if 0 <= row < grid.rows and 0 <= col < grid.cols:
        return grid.get(row, col)
    return None


def handle_left_click(grid, cell, has_start, has_goal):
    if cell is None:
        return has_start, has_goal
    if cell.state in (State.START, State.GOAL, State.WALL):
        return has_start, has_goal
    if not has_start:
        grid.set_state(cell.row, cell.col, State.START)
        return True, has_goal
    if not has_goal:
        grid.set_state(cell.row, cell.col, State.GOAL)
        return has_start, True
    grid.set_state(cell.row, cell.col, State.WALL)
    return has_start, has_goal


def handle_right_click(grid, cell):
    if cell is None:
        return
    grid.set_state(cell.row, cell.col, State.EMPTY)


def get_algorithm(name, grid, start, goal):
    if name == "BFS":
        return bfs(grid, start, goal)
    if name == "DFS":
        return dfs(grid, start, goal)
    if name == "Dijkstra":
        return dijkstra(grid, start, goal)
    if name == "A*":
        return astar(grid, start, goal)


def main():
    grid = Grid(ROWS, COLS)
    vis  = Visualizer(grid, cell_size=CELL_SIZE)

    has_start     = False
    has_goal      = False
    selected_algo = "BFS"
    active_gen    = None
    algo_status   = "idle"   # idle | running | done | no_path

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_r:
                    grid.reset()
                    has_start  = False
                    has_goal   = False
                    active_gen = None
                    algo_status = "idle"

                elif event.key == pygame.K_c:
                    grid.clear_search()
                    active_gen  = None
                    algo_status = "idle"

                elif event.key in ALGO_NAMES:
                    selected_algo = ALGO_NAMES[event.key]

                elif event.key == pygame.K_SPACE:
                    if has_start and has_goal and algo_status != "running":
                        grid.clear_search()
                        start = next(
                            grid.get(r, c)
                            for r in range(grid.rows)
                            for c in range(grid.cols)
                            if grid.get(r, c).state == State.START
                        )
                        goal = next(
                            grid.get(r, c)
                            for r in range(grid.rows)
                            for c in range(grid.cols)
                            if grid.get(r, c).state == State.GOAL
                        )
                        active_gen  = get_algorithm(selected_algo, grid, start, goal)
                        algo_status = "running"

            # single clicks (only when not running)
            if event.type == pygame.MOUSEBUTTONDOWN and algo_status != "running":
                cell = cell_at(grid, CELL_SIZE, event.pos)
                if event.button == 1:
                    has_start, has_goal = handle_left_click(
                        grid, cell, has_start, has_goal
                    )
                elif event.button == 3:
                    if cell and cell.state == State.START:
                        has_start = False
                    elif cell and cell.state == State.GOAL:
                        has_goal = False
                    handle_right_click(grid, cell)

        # held left-click: drag walls (only when not running)
        if algo_status != "running" and pygame.mouse.get_pressed()[0]:
            cell = cell_at(grid, CELL_SIZE, pygame.mouse.get_pos())
            if cell and cell.state == State.EMPTY and has_start and has_goal:
                grid.set_state(cell.row, cell.col, State.WALL)

        # held right-click: drag erase (only when not running)
        if algo_status != "running" and pygame.mouse.get_pressed()[2]:
            cell = cell_at(grid, CELL_SIZE, pygame.mouse.get_pos())
            if cell:
                if cell.state == State.START:
                    has_start = False
                elif cell.state == State.GOAL:
                    has_goal = False
                handle_right_click(grid, cell)

        # step the generator
        if algo_status == "running" and active_gen is not None:
            for _ in range(STEPS_PER_FRAME):
                result = vis.step_generator(active_gen)
                if result != "running":
                    algo_status = result
                    active_gen  = None
                    break

        # title bar
        if algo_status == "running":
            mode = "running..."
        elif algo_status == "done":
            mode = "done — path found"
        elif algo_status == "no_path":
            mode = "done — no path"
        elif not has_start:
            mode = "draw: start"
        elif not has_goal:
            mode = "draw: goal"
        else:
            mode = "draw: walls"

        pygame.display.set_caption(
            f"Pathfinding Visualizer  |  algo: {selected_algo}  |  {mode}  |  "
            f"R=reset  C=clear  Space=run"
        )

        vis.draw()
        vis.tick(60)

    vis.quit()


if __name__ == "__main__":
    main()
