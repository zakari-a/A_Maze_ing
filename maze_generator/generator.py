from typing import List, Optional, Tuple
from collections import deque
import random
from parsing.errors import MazeError


class Cell:
    """Represents a single node in the maze grid
    with wall states and visitation status."""
    def __init__(self) -> None:
        """It initializes the attributes for different variables"""
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False
        self.is_pattern = False


class MazeGenerator:
    """Handles the generation, modification,
    and solving of a grid-based maze."""
    def __init__(self, width: int, height: int, entry: tuple, exit_p: tuple,
                 output_file: str, perfect: bool,
                 seed: Optional[int] = None) -> None:
        """It initializes the attributes for different variables"""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_p = exit_p
        self.output_file = output_file
        self.perfect = perfect
        self.grid: List[List[Cell]] = []
        self.path: List[Tuple[int, int]] = []
        self.seed = seed

    def _set_42(self, grid: List[List[Cell]]) -> None:
        """Marks the 42 cells as visited, so they don't get broken
        and so they can form a valid 42 sign"""
        mid_x = self.width // 2
        mid_y = self.height // 2
        grid[mid_y][mid_x - 1].is_pattern = True
        grid[mid_y][mid_x - 2].is_pattern = True
        grid[mid_y][mid_x - 3].is_pattern = True
        grid[mid_y - 1][mid_x - 3].is_pattern = True
        grid[mid_y - 2][mid_x - 3].is_pattern = True
        grid[mid_y + 1][mid_x - 1].is_pattern = True
        grid[mid_y + 2][mid_x - 1].is_pattern = True
        grid[mid_y][mid_x + 1].is_pattern = True
        grid[mid_y][mid_x + 2].is_pattern = True
        grid[mid_y][mid_x + 3].is_pattern = True
        grid[mid_y - 1][mid_x + 3].is_pattern = True
        grid[mid_y - 2][mid_x + 3].is_pattern = True
        grid[mid_y - 2][mid_x + 2].is_pattern = True
        grid[mid_y - 2][mid_x + 1].is_pattern = True
        grid[mid_y + 1][mid_x + 1].is_pattern = True
        grid[mid_y + 2][mid_x + 1].is_pattern = True
        grid[mid_y + 2][mid_x + 2].is_pattern = True
        grid[mid_y + 2][mid_x + 3].is_pattern = True

    def _grid_generator(self) -> List[List[Cell]]:
        """Initializes a 2D array of Cell objects
        and prepares the mandatory 42 pattern."""
        height = self.height
        width = self.width
        rows = []
        for _ in range(height):
            current_row = []
            for _ in range(width):
                cell = Cell()
                current_row.append(cell)
            rows.append(current_row)
        if height <= 12 or width <= 14:
            print("Maze is too small for 42. "
                  "Grid won't contain the 42 pattern")
            return (rows)
        self._set_42(rows)

        return (rows)

    def _cords_42(self) -> set[tuple]:
        """Identifies all the 42 cells so they can stay
        intact and unvisited while creation or solving"""
        height = self.height
        weight = self.width
        x = weight // 2
        y = height // 2
        cords = [(x - 1, y), (x - 2, y), (x - 3, y),
                 (x - 3, y - 1), (x - 3, y - 2),
                 (x - 1, y + 1), (x - 1, y + 2),
                 (x + 1, y), (x + 2, y), (x + 3, y),
                 (x + 3, y - 1), (x + 3, y - 2),
                 (x + 2, y - 2), (x + 1, y - 2),
                 (x + 1, y + 1), (x + 1, y + 2),
                 (x + 2, y + 2), (x + 3, y + 2)]
        return (set(cords))

    def _is_inside(self, coor: tuple) -> List[tuple]:
        """Calculates valid neighboring coordinates
        within the boundaries of the grid."""
        height = self.height
        width = self.width
        x, y = coor
        inside = []
        if x - 1 >= 0 and x - 1 < width:
            inside.append((x - 1, y))
        if x + 1 >= 0 and x + 1 < width:
            inside.append((x + 1, y))
        if y + 1 >= 0 and y + 1 < height:
            inside.append((x, y + 1))
        if y - 1 >= 0 and y - 1 < height:
            inside.append((x, y - 1))
        return (inside)

    def _has_enough(self, grid: List[List[Cell]], coor: tuple) -> bool:
        """Checks wheter the current cell has enough walls in order
        to break some wallls and make an imperfect maze"""
        count = 0
        x, y = coor
        if (grid[y][x].north):
            count += 1
        if (grid[y][x].south):
            count += 1
        if (grid[y][x].east):
            count += 1
        if (grid[y][x].west):
            count += 1
        if count >= 1:
            return True
        return False

    def _wall_breaker(self, current_pos: tuple, neighbour_pos: tuple,
                      grid: List[List[Cell]]) -> None:
        """Removes the walls between two adjacent cells to create a passage."""
        nx, ny = neighbour_pos
        cx, cy = current_pos
        if ny > cy:
            grid[ny][nx].north = False
            grid[cy][cx].south = False
        elif ny < cy:
            grid[ny][nx].south = False
            grid[cy][cx].north = False
        elif nx > cx:
            grid[ny][nx].west = False
            grid[cy][cx].east = False
        elif nx < cx:
            grid[ny][nx].east = False
            grid[cy][cx].west = False

    def _make_it_imperfect(self, grid: List[List[Cell]]) -> None:
        """Breaks more walls in the grid so that it can
        have more than one valid path"""
        height = self.height
        width = self.width
        count = int(0.13 * width * height)
        unauthorized = self._cords_42()
        for _ in range(count):
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)
            if (x, y) in unauthorized:
                continue
            if (grid[y][x].north and grid[y][x].south
                    and grid[y][x].east and grid[y][x].west):
                continue
            if self._has_enough(grid, (x, y)):
                neighbours = self._is_inside((x, y))
                neighbour = random.choice(neighbours)
                if neighbour not in unauthorized:
                    self._wall_breaker((x, y), neighbour, grid)

    def generate(self) -> None:
        """Executes the randomized Depth-First Search
        algorithm to carve the maze."""
        self.grid = self._grid_generator()
        self._grid_check()

        if self.seed is not None:
            random.seed(self.seed)
        grid = self.grid
        stack = []
        entry_x, entry_y = self.entry
        grid[entry_y][entry_x].visited = True
        stack.append(self.entry)
        while (len(stack)) > 0:
            inside = self._is_inside(stack[-1])
            valid = []
            for cell in inside:
                x, y = cell
                if (
                    grid[y][x].visited is False
                    and not grid[y][x].is_pattern
                ):
                    valid.append(cell)
            if len(valid) > 0:
                chosen = random.choice(valid)
                nx, ny = chosen
                self._wall_breaker(stack[-1], chosen, grid)
                grid[ny][nx].visited = True
                stack.append(chosen)
            else:
                stack.pop()
        if not self.perfect:
            self._make_it_imperfect(grid)

    def generate2(self) -> None:
        """Executes the randomized Prim's algorithm
        to carve the maze."""
        self.grid = self._grid_generator()
        self._grid_check()
        if self.seed is not None:
            random.seed(self.seed)
        grid = self.grid
        ex, ey = self.entry
        grid[ey][ex].visited = True
        neighbours = self._is_inside(self.entry)
        frontier = set()
        for x, y in neighbours:
            if not grid[y][x].visited and not grid[y][x].is_pattern:
                frontier.add((x, y))
        while len(frontier) > 0:
            visited = []
            chosen = random.choice(list(frontier))
            nx, ny = chosen
            nbrs = self._is_inside(chosen)
            for tx, ty in nbrs:
                if grid[ty][tx].visited and not grid[ty][tx].is_pattern:
                    visited.append((tx, ty))
            v_neighbour = random.choice(visited)
            self._wall_breaker(chosen, v_neighbour, grid)
            grid[ny][nx].visited = True
            for cord in nbrs:
                tx, ty = cord
                if not grid[ty][tx].visited and not grid[ty][tx].is_pattern:
                    if (tx, ty) not in frontier:
                        frontier.add((tx, ty))
            frontier.remove(chosen)
        if not self.perfect:
            self._make_it_imperfect(grid)

    def _reset(self, grid: List[List[Cell]]) -> None:
        """Sets all cells as not visited for the path finding algo"""
        for row in grid:
            for cell in row:
                cell.visited = False
        if self.height > 12 and self.width > 14:
            self._set_42(grid)

    def _is_accessible(self, current: tuple, neighbour: tuple,
                       grid: List[List[Cell]]) -> bool:
        """Checks if there is an open passage
        between two adjacent cells."""
        nx, ny = neighbour
        cx, cy = current
        if ny > cy:
            if not grid[cy][cx].south:
                return True
        if ny < cy:
            if not grid[cy][cx].north:
                return True
        if nx > cx:
            if not grid[cy][cx].east:
                return True
        if nx < cx:
            if not grid[cy][cx].west:
                return True
        return (False)

    def _maze_solver(self) -> List[Tuple[int, int]]:
        """Perform the Breadth-First Search algo to search for
        the shortest path from the entry point to the exit point"""
        grid = self.grid
        self._reset(grid)
        queue = deque([self.entry])
        visited: set[Tuple[int, int]] = set()
        parents: dict[Tuple[int, int], Tuple[int, int]] = {}
        visited.add(self.entry)
        while len(queue) > 0:
            cx, cy = queue.popleft()
            if (cx, cy) == self.exit_p:
                break
            inside = self._is_inside((cx, cy))
            for coor in inside:
                nx, ny = coor
                if (grid[ny][nx].visited) is False:
                    if (self._is_accessible((cx, cy), (nx, ny), grid)
                            and coor not in visited):
                        visited.add(coor)
                        grid[ny][nx].visited = True
                        queue.append(coor)
                        parents[coor] = (cx, cy)
        the_way: List[Tuple[int, int]] = []
        start: Optional[Tuple[int, int]] = self.exit_p
        while start is not None:
            the_way.append(start)
            start = parents.get(start)
        return (the_way[::-1])

    def solve(self) -> List[str]:
        """Returns the solution path as a sequence of
        cardinal directions (N, S, E, W)."""
        path = self._maze_solver()
        self.path = path
        directions = []
        for i in range(len(path) - 1):
            nx, ny = path[i + 1]
            cx, cy = path[i]
            if ny > cy:
                directions.append("S")
            elif ny < cy:
                directions.append("N")
            elif nx > cx:
                directions.append("E")
            elif nx < cx:
                directions.append("W")
        return (directions)

    def get_hex_grid(self) -> List[List[str]]:
        """Converts the cell wall states into a
        2D list of hexadecimal characters."""
        grid = self.grid
        text = []
        for row in grid:
            tmp = []
            for cor in row:
                count = 0
                if cor.north:
                    count += 1
                if cor.east:
                    count += 2
                if cor.south:
                    count += 4
                if cor.west:
                    count += 8
                tmp.append(format(count, 'X'))
            text.append(tmp)
        return (text)

    def _grid_check(self) -> None:
        ex, ey = self.entry
        ox, oy = self.exit_p

        if self.grid[ey][ex].is_pattern:
            raise MazeError("Entry is inside '42' pattern")

        if self.grid[oy][ox].is_pattern:
            raise MazeError("Exit is inside '42' pattern")
