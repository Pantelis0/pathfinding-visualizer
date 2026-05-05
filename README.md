# Pathfinding Visualizer

An interactive grid app that animates BFS, DFS, Dijkstra, and A* in real time using Pygame.

The key design rule: **algorithms emit state changes; the visualizer draws them.**

## Project structure

```
pathfinding-visualizer/
├── grid.py             # Grid and cell data model
├── visualizer.py       # Pygame rendering layer
├── maze_gen.py         # Maze generation
├── main.py             # Entry point
└── algorithms/
    ├── bfs.py
    ├── dfs.py
    ├── dijkstra.py
    └── astar.py
```

## Milestone checklist

- [ ] Build the grid data model
- [ ] Open a Pygame window and draw the board
- [ ] Add mouse controls for start, goal, and walls
- [ ] Implement BFS and animate visited cells
- [ ] Implement DFS
- [ ] Implement Dijkstra with `heapq`
- [ ] Implement A* with Manhattan distance heuristic
- [ ] Add path reconstruction visualization
- [ ] Add speed controls / reset / statistics
- [ ] Add weighted terrain
- [ ] Add maze generation

## Running

```bash
pip install pygame
python main.py
```

## Resources

- Red Blob Games pathfinding tutorials
