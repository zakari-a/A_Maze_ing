from mlx import Mlx
from errors import MazeError
from maze_gen import MazeGenerator
from config_parser import final_parse
import random
from algorithm import DFS_algo
import time

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
    exit(1)

path = DFS_algo(maze, configs.entry, configs.exit)

CELL = 32

mlx = Mlx()
ctx = mlx.mlx_init()
win_w = maze.width * CELL 
win_h = maze.height * CELL

win = mlx.mlx_new_window(ctx, win_w, win_h + 40, "Maze")

pattern_img_result = mlx.mlx_xpm_file_to_image(ctx, "notgrey.xpm")
pattern_img = pattern_img_result[0] 
pattern_width = pattern_img_result[1] 
pattern_height = pattern_img_result[2]


img = mlx.mlx_new_image(ctx, win_w, win_h)
result = mlx.mlx_get_data_addr(img)
data = result[0]
size_line = result[2]

def put_pixel(x, y, color):
    if 0 <= x < win_w and 0 <= y < win_h:
        off = y * size_line + x * 4
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        data[off] = b
        data[off + 1] = g
        data[off + 2] = r
        data[off + 3] = 255

def hline(x1, x2, y, color):
    for x in range(x1, x2):
        put_pixel(x, y, color)

def vline(x, y1, y2, color):
    for y in range(y1, y2):
        put_pixel(x, y, color)

def clear(color=0x000000):
    for y in range(win_h):
        for x in range(win_w):
            put_pixel(x, y, color)


def neighbors(maze, x:int, y:int) -> list:
        cells = []
        if maze.in_bounds(x, y-1):
            cells.append((x, y-1))
        if maze.in_bounds(x+1, y):
            cells.append((x+1, y))
        if maze.in_bounds(x, y+1):
            cells.append((x, y+1))
        if maze.in_bounds(x-1, y):
            cells.append((x-1, y))
        return cells

def neighbors_cells(maze):
    visited = set()
    x = maze.width // 2
    y = maze.height // 2
    visited.add((x, y))
    cells = []
    cells.append([(x, y)])
    cells.append(neighbors(maze, x, y))
    for n in cells[1]:
        visited.add(n)
    i = 1
    while cells[i] and i < len(cells):
        cell = []
        for n in cells[i]:
            neigh = neighbors(maze, n[0], n[1])
            for k in neigh:
                if k not in visited:
                    cell.append(k)
                    visited.add(k)
        cells.append(cell)
        i += 1
    return cells

maze_index = 0
maze_animating = True
cells = neighbors_cells(maze)

def animate_maze(_):
    global maze_index, maze_animating, saved, cells

    if not maze_animating:
        return 0

    if maze_index < len(cells):
        c = cells[maze_index]
        for k in c:
            x, y = k
            cell = maze.grid[y][x]
            x *= CELL
            y *= CELL
            n = 2
            if cell.N:
                for i in range(n + 1):
                    hline(x - n , x + CELL + n, y + i, saved)
            if cell.S:
                for i in range(n + 1):
                    hline(x - n, x + CELL + n, y + CELL - i, saved)

            if cell.W:
                for i in range(n):
                    vline(x + i, y - n, y + CELL, saved)

            if cell.E:
                for i in range(n + 1):
                    vline(x + CELL - i, y - n, y + CELL, saved)
        time.sleep(0.01)
        mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)
        maze_index += 1
    else:
        maze_animating = False
        ex, ey = path[0]
        ox, oy = path[-1]
        ex *= CELL
        ey *= CELL
        ox *= CELL
        oy *= CELL

        for y in range(4, CELL - 4):
            for x in range(4, CELL - 4):
                if saved == 0x00FF00:
                    put_pixel(ex + x, ey + y, 0xFFFF00)
                else:
                    put_pixel(ex + x, ey + y, 0x00FF00)
            
        for y in range(4, CELL - 4):
            for x in range(4, CELL - 4):
                if saved == 0xFF0000:
                    put_pixel(ox + x, oy + y, 0xFF00FF)
                else:
                    put_pixel(ox + x, oy + y, 0xFF0000)
    return 0
        

def animate_pattern(_):
    global is_animating, animation_index, saved

    if not is_animating:
        return 0
    
    patt = pattern_coords(maze)
    for _ in range(1):
        if animation_index < len(patt):
            x, y = patt[animation_index]
            x *= CELL
            y *= CELL

            for ny in range(-1, CELL + 2):
                for nx in range(-1, CELL + 2):
                    if saved == 0xFFFFFF:
                        put_pixel(x + nx, y + ny, 0x000000)
                    else:
                        put_pixel(x + nx, y + ny, 0xFFFFFF)
            mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)
            # time.sleep(0.05)
            animation_index += 1
        else:
            is_animating = False
            break
            
    return 0

def animate_path(_):
    global is_animating_path, path_animation_index
    global path, path_color

    if not is_animating_path:
        return 0
    if path_animation_index  < len(path) - 2: 
        x1, y1 = path[path_animation_index + 1]
        px = x1 * CELL
        py = y1 * CELL
        for dy in range(8, CELL - 8):
            for dx in range(8, CELL - 8):
                put_pixel(px + dx, py + dy, path_color)
    
        if path_animation_index  < len(path):
            x2, y2 = path[path_animation_index]
            c1_x = x1 * CELL + CELL // 2
            c1_y = y1 * CELL + CELL // 2
            c2_x = x2 * CELL + CELL // 2
            c2_y = y2 * CELL + CELL // 2

            if c1_x == c2_x:
                start_x = x1 * CELL + 8
                end_x = x1 * CELL + CELL - 8
                
                start_y = min(y1 * CELL + 8, y2 * CELL + 8)
                end_y = max(y1 * CELL + CELL - 8, y2 * CELL + CELL - 8)
                for y in range(start_y, end_y):
                    for x in range(start_x, end_x):
                        put_pixel(x, y, path_color)

            elif c1_y == c2_y:
                start_y = y1 * CELL + 8
                end_y = y1 * CELL + CELL - 8
                
                start_x = min(x1 * CELL + 8, x2 * CELL + 8)
                end_x = max(x1 * CELL + CELL - 8, x2 * CELL + CELL - 8)
                for y in range(start_y, end_y):
                    for x in range(start_x, end_x):
                            put_pixel(x, y, path_color)

        mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)
        path_animation_index += 1 

    else:
        is_animating_path = False
    return 0

def pattern_coords(maze):
    patt = []
    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x].is_pattern:
                patt.append((x, y))

    return patt


def darw_pattern(_):
    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x].is_pattern:
                px = x * CELL
                py = y * CELL
                offset_x = (CELL - pattern_width) // 2
                offset_y = (CELL - pattern_height) // 2
                mlx.mlx_put_image_to_window(ctx, win, pattern_img, px + offset_x, py + offset_y)


def draw_maze(wall_color, maze, path):

    ex, ey = path[0]
    ox, oy = path[-1]
    ex *= CELL
    ey *= CELL
    ox *= CELL
    oy *= CELL

    for y in range(4, CELL - 4):
        for x in range(4, CELL - 4):
            if saved == 0x00FF00:
                put_pixel(ex + x, ey + y, 0xFFFF00)
            else:
                put_pixel(ex + x, ey + y, 0x00FF00)
           
    for y in range(4, CELL - 4):
        for x in range(4, CELL - 4):
            if saved == 0xFF0000:
                put_pixel(ox + x, oy + y, 0xFF00FF)
            else:
                put_pixel(ox + x, oy + y, 0xFF0000)

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            px = x * CELL
            py = y * CELL
            n = 2
            if cell.N:
                for i in range(n + 1):
                    hline(px - n, px + CELL + n, py + i, wall_color)
            if cell.S:
                for i in range(n + 1):
                    hline(px - n, px + CELL + n, py + CELL - i, wall_color)

            if cell.W:
                for i in range(n):
                    vline(px + i, py - n, py + CELL, wall_color)

            if cell.E:
                for i in range(n + 1):
                    vline(px + CELL - i, py - n, py + CELL, wall_color)
    
    mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)
        
    # for y in range(maze.height):
    #     for x in range(maze.width):
    #         cell = maze.grid[y][x]
    #         if cell.is_pattern:
    #             px = x * CELL
    #             py = y * CELL
    #          new   mlx.mlx_put_image_to_window(ctx, win, pattern_img, px, py)

def draw_path(path, color=0xFFFFFF):
    for x, y in path[1:len(path)- 1]:
        px = x * CELL
        py = y * CELL
        for dy in range(14, CELL - 14):
            for dx in range(14, CELL - 14):
                put_pixel(px + dx, py + dy, color)
    mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)

def print_keys(keys):
    y = win_h + 10
    x = 40
    for key in keys:
        mlx.mlx_string_put(ctx, win, x, y, 0xFFFFFF, key)
        x += 200

colors = [0xFFFFFF, 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF]
strings = ["'1' : Regen", "'2' : Path", "'3' : Color","'4' : Quit"]
saved = random.choice(colors)

path_color = colors[0]
clear(0x000000)
cleared_buffer = bytes(data)

is_animating = True
animation_index = 0
print_keys(strings)
p = True

show_path = False
is_animating_path = False
path_animation_index = 1

i = 0
def on_key(keycode, _):
    global saved
    global path
    global maze, i, maze_index, maze_animating
    global is_animating, animation_index
    if keycode == 52:
        mlx.mlx_loop_exit(ctx)
    
    elif keycode == 51:
        if maze_animating:
            return
        saved = colors[i % len(colors)]
        draw_maze(saved, maze, path)
        i += 1
        animation_index = 0
        is_animating = True


    elif keycode == 50:
        global show_path, is_animating_path, path_animation_index
        if is_animating_path or is_animating:
            return
        
        if not show_path:
            path_animation_index = 1
            is_animating_path = True
            show_path = True
        else:
            data[:] = cleared_buffer
            draw_maze(saved, maze, path)
            show_path = False
            animation_index = 0
            is_animating = True

    elif keycode == 49:

        if is_animating_path or is_animating:
            return
          
        maze = gen.generate(configs.entry, configs.exit, configs.perfect)
        path = DFS_algo(maze, configs.entry, configs.exit)
        show_path = False
        data[:] = cleared_buffer
        maze_animating = True
        maze_index = 0
        animation_index = 0
        is_animating = True

    elif keycode == 118:
        if is_animating_path:
            return

        global p
        if p:
            draw_path(path)
            p = False
        else:
            data[:] = cleared_buffer
            draw_maze(saved, maze, path)
            p = True
            animation_index = 0
            is_animating = True
            

def animation_loop(_):
    animate_maze(_)
    if not maze_animating:
        animate_pattern(_)
    animate_path(_)
    darw_pattern(_)
    return 0

mlx.mlx_loop_hook(ctx, animation_loop, None)
mlx.mlx_key_hook(win, on_key, None)
mlx.mlx_loop(ctx)