import pygame
from grid import Grid, State
from visualizer import Visualizer

ROWS      = 40
COLS      = 40
CELL_SIZE = 20

ALGO_NAMES = {
    pygame.K_1: "BFS",
    pygame.K_2: "DFS",
    pygame.K_3: "Dijkstra",
    pygame.K_4: "A*",
}


def cell_at(grid, cell_size, mouse_pos):
    """Return the Cell under the mouse position, or None if out of bounds."""
    x, y = mouse_pos
    col = x // cell_size
    row = y // cell_size
    if 0 <= row < grid.rows and 0 <= col < grid.cols:
        return grid.get(row, col)
    return None


def handle_left_click(grid, cell, has_start, has_goal):
    """Place start → goal → wall in that order. Returns updated (has_start, has_goal)."""
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
    """Erase a cell back to empty."""
    if cell is None:
        return
    grid.set_state(cell.row, cell.col, State.EMPTY)


def main():
    grid = Grid(ROWS, COLS)
    vis  = Visualizer(grid, cell_size=CELL_SIZE)

    has_start    = False
    has_goal     = False
    selected_algo = "BFS"

    pygame.display.set_caption(f"Pathfinding Visualizer  |  {selected_algo}  |  draw: start")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- keyboard ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_r:
                    grid.reset()
                    has_start = False
                    has_goal  = False

                elif event.key == pygame.K_c:
                    grid.clear_search()

                elif event.key in ALGO_NAMES:
                    selected_algo = ALGO_NAMES[event.key]

                elif event.key == pygame.K_SPACE:
                    # placeholder — algorithms wired in Phase 5+
                    print(f"[placeholder] would run {selected_algo}")

            # --- single clicks ---
            if event.type == pygame.MOUSEBUTTONDOWN:
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

        # --- held left-click: drag to draw walls ---
        if pygame.mouse.get_pressed()[0]:
            cell = cell_at(grid, CELL_SIZE, pygame.mouse.get_pos())
            if cell and cell.state == State.EMPTY and has_start and has_goal:
                grid.set_state(cell.row, cell.col, State.WALL)

        # --- held right-click: drag to erase ---
        if pygame.mouse.get_pressed()[2]:
            cell = cell_at(grid, CELL_SIZE, pygame.mouse.get_pos())
            if cell:
                if cell.state == State.START:
                    has_start = False
                elif cell.state == State.GOAL:
                    has_goal  = False
                handle_right_click(grid, cell)

        # update title to reflect current mode
        if not has_start:
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
