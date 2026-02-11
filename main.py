from errors import MazeError
from maze import Maze
from typing import List
from maze_gen import MazeGenerator
from algorithm import DFS_algo, path_converter
from config_parser import final_parse

def print_maze(maze, path=None):
    w, h = maze.width, maze.height
    grid = maze.grid

    path_set = set(path) if path else set()

    print("+" + "---+" * w)
    for y in range(h):
        row = "|"
        for x in range(w):
            cell = grid[y][x]

            if (x, y) in path_set:
                row += f" X "
            else:
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


def maze_result(maze: Maze, output_file, path, entry, exit_) -> None:
    cells : List[str] = []
    for y in range(maze.height):
        line = ""
        for x in range(maze.width):
            number = 0
            if maze.grid[y][x].N:
                number += 1
            if maze.grid[y][x].E:
                number += 2
            if maze.grid[y][x].S:
                number += 4
            if maze.grid[y][x].W:
                number += 8
            line = line + format(number, 'X')
        cells.append(line + "\n")
    with open(output_file, "w") as file:
        for line in cells:
            file.write(line)
        file.write("\n")
        file.write(f"{entry[0]},{entry[1]}\n")
        file.write(f"{exit_[0]},{exit_[1]}\n")
        file.write(path)


try:
    configs = final_parse("configs.txt")
except MazeError as e:
    print(f"Error : {e}")
    exit(1)

gen = MazeGenerator(configs.width, configs.height)
try:
    maze = gen.generate(configs.entry, configs.exit, configs.perfect)
except MazeError as e:
    print(f"Error: {e}")


stack = DFS_algo(maze, configs.entry, configs.exit)
path = path_converter(stack)
print_maze(maze, stack)
maze_result(maze, configs.output_file, path, configs.entry, configs.exit)