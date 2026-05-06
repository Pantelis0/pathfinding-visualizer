# Algorithm event protocol
# -------------------------
# Every algorithm in this package must be a Python generator function that
# accepts (grid, start_cell, goal_cell) and yields events in this format:
#
#   ("frontier", (row, col))         cell added to queue / stack / heap
#   ("visit",    (row, col))         cell popped and being processed
#   ("path",     [(row, col), ...])  final path start → goal, ordered
#   ("no_path",)                     search ended with no route found
#
# Rules:
#   - Yield one event per step — the visualizer calls next() once per frame.
#   - Never import from visualizer.py — algorithms know nothing about drawing.
#   - Never modify cell.state directly — only yield events; the visualizer
#     applies state changes.
#   - Always yield ("path", [...]) or ("no_path",) as the final event before
#     the generator returns.

FRONTIER = "frontier"
VISIT    = "visit"
PATH     = "path"
NO_PATH  = "no_path"
