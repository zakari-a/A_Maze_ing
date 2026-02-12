from maze import Maze
from errors import Pattern42Error, MazeError
from typing import List
import random


class MazeGenerator():
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height


    def generate(self, entry: tuple, exit_: tuple, perfect: bool) -> Maze:
        maze = Maze(self.width, self.height)
        try:
            self._apply_pattern(maze, entry, exit_)
        except Pattern42Error as e:
            print(e)
        self._carve(maze, entry, exit_, perfect)
        
        return maze
        

    def _apply_pattern(self, maze: Maze, entry: tuple, exit: tuple) -> None:
        center_x = maze.width // 2
        center_y = maze.height // 2

        pattern_left   = center_x - 3
        pattern_right  = center_x + 3
        pattern_top    = center_y - 2
        pattern_bottom = center_y + 2
            
        if (
            pattern_left < 0 or
            pattern_right >= maze.width or
            pattern_top < 0 or 
            pattern_bottom >= maze.height
        ):
            raise Pattern42Error("Maze is too small to display '42' pattern")
        ex, ey = entry
        ox, oy = exit

        self._42pattern(maze)

        if maze.grid[ey][ex].is_pattern:
            raise MazeError("Entry is inside '42' pattern")

        if maze.grid[oy][ox].is_pattern:
            raise MazeError("Exit is inside '42' pattern")


    def _42pattern(self, maze: Maze) -> None:
        x = maze.width // 2
        y = maze.height // 2

        maze.grid[y][x - 1].is_pattern = True
        maze.grid[y][x - 2].is_pattern = True
        maze.grid[y][x - 3].is_pattern = True
        maze.grid[y - 1][x - 3].is_pattern = True
        maze.grid[y - 2][x - 3].is_pattern = True
        maze.grid[y + 1][x - 1].is_pattern = True
        maze.grid[y + 2][x - 1].is_pattern = True
        maze.grid[y][x + 1].is_pattern = True
        maze.grid[y][x + 2].is_pattern = True
        maze.grid[y][x + 3].is_pattern = True
        maze.grid[y - 1][x + 3].is_pattern = True
        maze.grid[y - 2][x + 3].is_pattern = True
        maze.grid[y - 2][x + 2].is_pattern = True
        maze.grid[y - 2][x + 1].is_pattern = True
        maze.grid[y + 1][x + 1].is_pattern = True
        maze.grid[y + 2][x + 1].is_pattern = True
        maze.grid[y + 2][x + 2].is_pattern = True
        maze.grid[y + 2][x + 3].is_pattern = True
        

    def _carve(self, maze, entry, exit_, perfect) -> None:
        stack = []
        sx, sy = entry
        maze.grid[sy][sx].visited = True
        stack.append((sx, sy))

        while stack:
            x, y = stack[-1]
            nbrs = maze.neighbors(x, y)

            unvisited = []
            for direction, nx, ny in nbrs:
                if not maze.grid[ny][nx].visited and not maze.grid[ny][nx].is_pattern:
                    unvisited.append((direction, nx, ny))
            
            if not unvisited:
                stack.pop()
                continue
            
            direction, nx, ny = random.choice(unvisited)
            maze.remove_wall(x, y, direction)
            maze.grid[ny][nx].visited = True
            stack.append((nx, ny))

        if not perfect:
            deads = self._dead_ends(maze)
            total = int(len(deads) * 0.50)
            for _ in range(total):
                x, y = random.choice(deads)
                deads.remove((x, y))
                
                checked = []
                n_nbrs = maze.neighbors(x, y)
                for direction, nx, ny in n_nbrs:
                    if not maze.grid[ny][nx].is_pattern and maze.has_wall(x, y, direction):
                        walls = maze.walls_count(nx, ny)
                        if walls <= 2:
                            checked.append((direction, nx, ny))
                
                if checked:
                    direction, nx, ny = random.choice(checked)
                    maze.remove_wall(x, y, direction)
                
                if not deads:
                    break

    def _dead_ends(self, maze: Maze) -> List[tuple]:
        deads : List[tuple] = []

        for y in range(maze.height):
            for x in range(maze.width):
                count: int = 0
                if not maze.grid[y][x].N:
                    count += 1
                if not maze.grid[y][x].E:
                    count += 1
                if not maze.grid[y][x].S:
                    count += 1
                if not maze.grid[y][x].W:
                    count += 1
                if count == 1:
                    deads.append((x, y))

        return deads

