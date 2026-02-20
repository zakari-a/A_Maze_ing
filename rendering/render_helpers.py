from typing import List, Set, Tuple
from maze_generator.generator import MazeGenerator


def in_bounds(x: int, y: int, width: int, height: int) -> bool:
    """Check if the coordinates (x, y) are within the maze bounds."""
    return True if 0 <= x < width and 0 <= y < height else False


def neighbors(x: int, y: int, width: int,
              height: int) -> List[Tuple[int, int]]:
    """Get the neighboring cells of (x, y) that are within bounds."""
    cells: List[Tuple[int, int]] = []
    if in_bounds(x, y-1, width, height):
        cells.append((x, y-1))
    if in_bounds(x+1, y, width, height):
        cells.append((x+1, y))
    if in_bounds(x, y+1, width, height):
        cells.append((x, y+1))
    if in_bounds(x-1, y, width, height):
        cells.append((x-1, y))
    return cells


def neighbors_cells(x: int, y: int, width: int,
                    height: int) -> List[List[Tuple[int, int]]]:
    """
    Get all cells in the maze grouped by their distance from the center.
    """
    visited: Set[Tuple[int, int]] = set()
    visited.add((x, y))
    cells: List[List[Tuple[int, int]]] = []
    cells.append([(x, y)])
    cells.append(neighbors(x, y, width, height))
    for n in cells[1]:
        visited.add(n)
    i: int = 1
    while cells[i] and i < len(cells):
        cell: List[Tuple[int, int]] = []
        for n in cells[i]:
            neigh: List[Tuple[int, int]] = neighbors(n[0], n[1],
                                                     width, height)
            for k in neigh:
                if k not in visited:
                    cell.append(k)
                    visited.add(k)
        cells.append(cell)
        i += 1
    return cells


def pattern_coords(maze: MazeGenerator) -> List[Tuple[int, int]]:
    """Get the coordinates of Pattern 42 cells in the maze."""
    patt: List[Tuple[int, int]] = []
    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x].is_pattern:
                patt.append((x, y))

    return patt
