import pygame
from grid import Grid, State
from visualizer import Visualizer

ROWS      = 40
COLS      = 40
CELL_SIZE = 20


def main():
    grid = Grid(ROWS, COLS)
    vis  = Visualizer(grid, cell_size=CELL_SIZE)

    # Seed a few cells so every colour is visible on first launch
    grid.set_state(0,  0,  State.START)
    grid.set_state(39, 39, State.GOAL)
    grid.set_state(5,  5,  State.WALL)
    grid.set_state(5,  6,  State.WALL)
    grid.set_state(5,  7,  State.WALL)
    grid.set_state(10, 10, State.VISITED)
    grid.set_state(10, 11, State.FRONTIER)
    grid.set_state(20, 20, State.PATH)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        vis.draw()
        vis.tick(60)

    vis.quit()


if __name__ == "__main__":
    main()
