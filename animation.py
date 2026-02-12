from mlx import Mlx
from errors import MazeError
from maze import Maze
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

CELL = 40

mlx = Mlx()
ctx = mlx.mlx_init()
win_w = maze.width * CELL 
win_h = maze.height * CELL

win = mlx.mlx_new_window(ctx, win_w, win_h, "Maze")


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


def animate_maze(_):
    global is_animating, animation_index, saved

    if not is_animating:
        return 0
    
    if animation_index < maze.width * maze.height:
        x = animation_index % maze.width
        y = animation_index // maze.width

        cell = maze.grid[y][x]
        px = x * CELL
        py = y * CELL
        n = 9
        if cell.N:
            for i in range(n + 1):
                hline(px - n , px + CELL + n, py + i, saved)
        if cell.S:
            for i in range(n + 1):
                hline(px - n, px + CELL + n, py + CELL - i, saved)

        if cell.W:
            for i in range(n):
                vline(px + i, py - n, py + CELL, saved)

        if cell.E:
            for i in range(n + 1):
                vline(px + CELL - i, py - n, py + CELL, saved)



        if cell.is_pattern:
            for ny in range(CELL + 1):
                for nx in range(CELL + 1):
                    put_pixel(px + nx, py + ny, 0xFFFFFF)

        mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)
        animation_index += 1
    else:
        is_animating = False
        
    return 0


def animate_path(_):
    global is_animating_path, path_animation_index
    global path, path_color

    if not is_animating_path:
        return 0
    if path_animation_index < len(path):
        x, y = path[path_animation_index]
        px = x * CELL
        py = y * CELL
        for dy in range(10, CELL -10):
            for dx in range(10, CELL - 10):
                put_pixel(px + dx, py + dy, path_color)
        time.sleep(0.05)
        mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)
        path_animation_index += 1
    
    else:
        is_animating_path = False
    
    return 0


def draw_maze(wall_color, maze):

    clear(0x000000)
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            px = x * CELL
            py = y * CELL
            n = 9
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
                for i in range(n):
                    vline(px + CELL - i, py - n, py + CELL, wall_color)

            if cell.is_pattern:
                for ny in range(CELL + 1):
                    for nx in range(CELL + 1):
                        put_pixel(px + nx, py + ny, 0xFFFFFF)
                    
    # if show_path:
    #     draw_path(path, path_color)
        
    mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)

def draw_path(path, color):

    for x, y in path:
        px = x * CELL
        py = y * CELL
        for dy in range(10, CELL -10):
            for dx in range(10, CELL - 10):
                put_pixel(px + dx, py + dy, color)


colors = [0xFFFFFF, 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF]
saved = random.choice(colors)
path_color = colors[0]

clear(0x000000)
is_animating = True
animation_index = 0
show_path = False
is_animating_path = False
path_animation_index = 0

def on_key(keycode, _):
    global saved
    global path
    global maze
    if keycode == 65307:
        mlx.mlx_loop_exit(ctx)
    
    elif keycode == 99:
        saved = random.choice(colors)
        draw_maze(saved, maze)

    elif keycode == 115:
        global show_path, is_animating_path, path_animation_index
        if not show_path:
            path_animation_index = 0
            is_animating_path = True
            show_path = True
        else:
            draw_maze(saved, maze)
            show_path = False

    elif keycode == 103:
        global is_animating, animation_index
        maze = gen.generate(configs.entry, configs.exit, configs.perfect)
        path = DFS_algo(maze, configs.entry, configs.exit)
        show_path = False 
        clear(0x000000)
        animation_index = 0
        is_animating = True

def animation_loop(_):
    animate_maze(_)
    animate_path(_)
    return 0

mlx.mlx_loop_hook(ctx, animation_loop, None)
mlx.mlx_key_hook(win, on_key, None)
mlx.mlx_loop(ctx)
