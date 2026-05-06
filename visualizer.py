import pygame
from grid import State

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

    def tick(self, fps=60):
        self.clock.tick(fps)

    def quit(self):
        pygame.quit()
