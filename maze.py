from errors import *

class Cell:
    def __init__(self):
        self.N = True
        self.E = True
        self.S = True
        self.W = True
        self.visited = False
        self.is_pattern = False

class Maze:
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        grid = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Cell())
            grid.append(row)
        self.grid = grid

    def in_bounds(self, x:int, y:int) -> bool:
        return True if 0 <= x < self.width and 0 <= y < self.height else False


    def neighbors(self, x:int, y:int) -> list:
        cells = []
        if self.in_bounds(x, y-1):
            cells.append(("N", x, y-1))
        if self.in_bounds(x+1, y):
            cells.append(("E", x+1, y))
        if self.in_bounds(x, y+1):
            cells.append(("S", x, y+1))
        if self.in_bounds(x-1, y):
            cells.append(("W", x-1, y))
        return cells

    def has_wall(self, x: int, y: int, direction: str) -> bool:
        if direction == "N":
            return self.grid[y][x].N
        elif direction == "E":
            return self.grid[y][x].E
        elif direction == "S":
            return self.grid[y][x].S
        elif direction == "W":
            return self.grid[y][x].W
        else:
            raise MazeError(f"Invalid Direction '{direction}'")
                    

    def remove_wall(self, x: int, y: int, direction: str) -> None:
        if direction == "N":
            self.grid[y][x].N = False
            self.grid[y -1][x].S = False
        elif direction == "E":
            self.grid[y][x].E = False
            self.grid[y][x + 1].W = False
        elif direction == "S":
            self.grid[y][x].S = False
            self.grid[y + 1][x].N = False
        elif direction == "W":
            self.grid[y][x].W = False
            self.grid[y][x - 1].E = False
        else:
            raise MazeError(f"Invalid Direction {direction}")
        
    def walls_count(self, x: int, y: int) -> int:
        count: int = 0
        if not self.grid[y][x].N:
            count += 1
        if not self.grid[y][x].E:
            count += 1
        if not self.grid[y][x].S:
            count += 1
        if not self.grid[y][x].W:
            count += 1
        return count