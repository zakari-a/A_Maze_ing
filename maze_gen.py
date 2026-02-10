from maze import Maze, Cell
from config_parser import final_parse
from errors import *
from typing import List
import random

try:
    configs = final_parse("configs.txt")
except ConfigError as e:
    print(e)
    exit(1)

mz = Maze(configs.width, configs.height)


def pattern_check(maze: Maze, entry: tuple, exit: tuple) -> None:
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

    if pattern_left <= ex <= pattern_right and pattern_top <= ey <= pattern_bottom:
        raise Pattern42Error("Entry is inside '42' pattern")

    if pattern_left <= ox <= pattern_right and pattern_top <= oy <= pattern_bottom:
        raise Pattern42Error("Exit is inside '42' pattern")

    set_42pattern(maze)

def set_42pattern(maze: Maze) -> None:
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
    

def maze_generator(maze, entry, exit_, perfect) -> None:
    try:
        pattern_check(maze, entry, exit_)
    except Pattern42Error as e:
        print(f"Error: {e}")
    
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
        total = int((maze.width * maze.height) / 10)
        for _ in range(total+1):
            x, y = (random.randint(0, maze.width - 1), random.randint(0, maze.height - 1))
            while maze.grid[y][x].is_pattern:
                x, y = (random.randint(0, maze.width - 1), random.randint(0, maze.height - 1))
            checked = []
            n_nbrs = maze.neighbors(x, y)
            for direction, nx, ny in n_nbrs:
                if not maze.grid[ny][nx].is_pattern and maze.has_wall(nx, ny, direction):
                    checked.append((direction, nx, ny))
            if checked:
                direction, nx, ny = random.choice(checked)
                maze.remove_wall(x, y, direction)



def print_maze(maze):
    w, h = maze.width, maze.height
    grid = maze.grid

    print("+" + "---+" * w)

    for y in range(h):
        row = "|"
        for x in range(w):
            cell = grid[y][x]
            row += "   "
            if x == w - 1:
                row += "|"
            else:
                row += "|" if cell.E else " "
        print(row)

        row = "+"
        for x in range(w):
            cell = grid[y][x]
            
            if y == h - 1:
                row += "---+"
            else:
                row += "---+" if cell.S else "   +"
        print(row)


maze_generator(mz, configs.entry, configs.exit, configs.perfect)
print_maze(mz)
