import pygame
from grid import State
from algorithms import FRONTIER, VISIT, PATH, NO_PATH

# --- colours ---
COLOURS = {
    State.EMPTY:    (255, 255, 255),
    State.WALL:     (30,  30,  30),
    State.START:    (0,   200, 80),
    State.GOAL:     (220, 50,  50),
    State.VISITED:  (135, 206, 235),
    State.FRONTIER: (255, 165, 0),
    State.PATH:     (255, 230, 0),
}
GRID_LINE_COLOUR = (200, 200, 200)
BACKGROUND      = (245, 245, 245)


class Visualizer:
    def __init__(self, grid, cell_size=20):
        self.grid      = grid
        self.cell_size = cell_size

        width  = grid.cols * cell_size
        height = grid.rows * cell_size

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pathfinding Visualizer")
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill(BACKGROUND)
        cs = self.cell_size

        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                cell   = self.grid.get(r, c)
                colour = COLOURS[cell.state]
                rect   = pygame.Rect(c * cs, r * cs, cs, cs)
                pygame.draw.rect(self.screen, colour, rect)
                pygame.draw.rect(self.screen, GRID_LINE_COLOUR, rect, 1)

        pygame.display.flip()

    def step_generator(self, gen):
        """Consume one event from the algorithm generator.

        Returns:
            "running"  — event processed, algorithm still going
            "done"     — path found and drawn
            "no_path"  — search exhausted, no route exists
        """
        try:
            event = next(gen)
        except StopIteration:
            return "done"

        kind = event[0]

        if kind == FRONTIER:
            r, c = event[1]
            cell = self.grid.get(r, c)
            if cell.state not in (State.START, State.GOAL):
                self.grid.set_state(r, c, State.FRONTIER)

        elif kind == VISIT:
            r, c = event[1]
            cell = self.grid.get(r, c)
            if cell.state not in (State.START, State.GOAL):
                self.grid.set_state(r, c, State.VISITED)

        elif kind == PATH:
            for r, c in event[1]:
                cell = self.grid.get(r, c)
                if cell.state not in (State.START, State.GOAL):
                    self.grid.set_state(r, c, State.PATH)
            return "done"

        elif kind == NO_PATH:
            return "no_path"

        return "running"

    def tick(self, fps=60):
        self.clock.tick(fps)

    def quit(self):
        pygame.quit()
