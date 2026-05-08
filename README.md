# Pathfinding Visualizer

An interactive grid app that animates BFS, DFS, Dijkstra, and A* in real time using Pygame.

**Core design rule:** algorithms emit state changes — the visualizer draws them. Search code never touches Pygame.

---

## Algorithms

| Key | Algorithm | Guarantees shortest path | Handles weights |
|-----|-----------|--------------------------|-----------------|
| `1` | BFS | ✅ (unweighted) | ❌ |
| `2` | DFS | ❌ | ❌ |
| `3` | Dijkstra | ✅ | ✅ |
| `4` | A* | ✅ | ✅ |

---

## Controls

| Input | Action |
|-------|--------|
| Left click | Place start → goal → walls (in order) |
| Left click + drag | Draw walls continuously |
| Right click / drag | Erase cells |
| `1` `2` `3` `4` | Select algorithm |
| `Space` | Run selected algorithm |
| `C` | Clear search (keep walls) |
| `R` | Full reset |
| `W` | Toggle weighted terrain paint mode (purple, cost ×5) |
| `M` | Generate a random maze |
| `+` / `-` | Increase / decrease animation speed (1×–50×) |
| `Esc` | Quit |

---

## Setup

```bash
pip install pygame
python3 main.py
```

Requires Python 3.10+ and Pygame 2.x.

---

## Project structure

```
pathfinding-visualizer/
├── grid.py             # Cell + Grid data model, State enum
├── visualizer.py       # All Pygame rendering, step_generator()
├── maze_gen.py         # Recursive backtracker maze generation
├── main.py             # Entry point, event loop, controls
├── requirements.txt
└── algorithms/
    ├── __init__.py     # Event protocol definition
    ├── bfs.py
    ├── dfs.py
    ├── dijkstra.py
    └── astar.py
```

---

## How the event protocol works

Every algorithm is a Python generator that yields events:

```python
("frontier", (row, col))        # cell added to queue/stack/heap
("visit",    (row, col))        # cell being processed
("path",     [(row, col), ...]) # final path, start → goal
("no_path",)                    # no route exists
```

The visualizer calls `next()` on the generator once per frame and updates cell colours accordingly. Algorithms never import from `visualizer.py`.
