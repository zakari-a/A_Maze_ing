from typing import List, Set
from maze import Maze
import random

def opened_walls(maze:Maze, x: int, y: int) -> List[tuple]:
    opened: List[tuple] = []
    if not maze.grid[y][x].N:
        opened.append((x, y-1))
    if not maze.grid[y][x].E:
        opened.append((x+1, y))
    if not maze.grid[y][x].S:
        opened.append((x, y+1))
    if not maze.grid[y][x].W:
        opened.append((x-1, y))

    return opened

def path_converter(stack: List[tuple]) -> str:
    path: str = ""
    for n in range(len(stack)-1):
        x, y = stack[n]
        nx, ny = stack[n+1]
        if nx == x and ny == y - 1:
            path += 'N'
        elif nx == x + 1 and ny == y:
            path += 'E'
        elif nx == x and ny == y + 1:
            path += 'S'
        elif nx == x - 1 and ny == y:
            path += 'W'

    return path

def DFS_algo(maze: Maze, entry: tuple, exit_:tuple) -> str:
    stack: List[tuple] = []
    visited: Set[tuple] = set()

    x, y = entry
    visited.add((x, y))
    stack.append((x, y))
    while stack and stack[-1] != exit_:
        x, y = stack[-1]
        ways = opened_walls(maze, x, y)

        unvisited = []
        for nx, ny in ways:
            if (nx, ny) not in visited:
                unvisited.append((nx, ny))

        if not unvisited:
            stack.pop()
            continue
        
        nx, ny = unvisited[0]
        visited.add((nx, ny))
        stack.append((nx, ny))

    return stack