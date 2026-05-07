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
    State.WEIGHTED: (180, 120, 220),  # purple — passable but costly
}
GRID_LINE_COLOUR = (200, 200, 200)
BACKGROUND       = (245, 245, 245)
STATS_BG         = (30,  30,  30, 180)
STATS_TEXT       = (255, 255, 255)
FONT_SIZE        = 14


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
        self._font = pygame.font.SysFont("monospace", FONT_SIZE, bold=True)

        # stats — updated by step_generator and reset by caller
        self.visited_count = 0
        self.path_length   = 0

    def reset_stats(self):
        self.visited_count = 0
        self.path_length   = 0

    def draw(self, algo_name="", status="idle", speed=1):
        self.screen.fill(BACKGROUND)
        cs = self.cell_size

        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                cell   = self.grid.get(r, c)
                colour = COLOURS[cell.state]
                rect   = pygame.Rect(c * cs, r * cs, cs, cs)
                pygame.draw.rect(self.screen, colour, rect)
                pygame.draw.rect(self.screen, GRID_LINE_COLOUR, rect, 1)

        self._draw_stats(algo_name, status, speed)
        pygame.display.flip()

    def _draw_stats(self, algo_name, status, speed):
        lines = [
            f"algo:    {algo_name}",
            f"status:  {status}",
            f"visited: {self.visited_count}",
            f"path:    {self.path_length if self.path_length else '--'} cells",
            f"speed:   {speed}x  (+/- to change)",
        ]
        pad    = 6
        lh     = FONT_SIZE + 4
        box_w  = 160
        box_h  = pad * 2 + lh * len(lines)
        box_x  = 6
        box_y  = 6

        surface = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        surface.fill((30, 30, 30, 180))
        self.screen.blit(surface, (box_x, box_y))

        for i, line in enumerate(lines):
            text = self._font.render(line, True, STATS_TEXT)
            self.screen.blit(text, (box_x + pad, box_y + pad + i * lh))

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
            self.visited_count += 1

        elif kind == PATH:
            for r, c in event[1]:
                cell = self.grid.get(r, c)
                if cell.state not in (State.START, State.GOAL):
                    self.grid.set_state(r, c, State.PATH)
            self.path_length = len(event[1])
            return "done"

        elif kind == NO_PATH:
            return "no_path"

        return "running"

    def tick(self, fps=60):
        self.clock.tick(fps)

    def quit(self):
        pygame.quit()
