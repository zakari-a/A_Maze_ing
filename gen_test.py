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

def print_maze(maze, path=None):
    w, h = maze.width, maze.height
    grid = maze.grid

    path_set = set(path) if path else set()

    print("+" + "--+" * w)
    for y in range(h):
        row = "|"
        for x in range(w):
            cell = grid[y][x]

            if (x, y) in path_set:
                row += f" X "
            else:
                row += "  "

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