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
CELL = 32

mlx = Mlx()
ctx = mlx.mlx_init()
win_w = maze.width * CELL 
win_h = maze.height * CELL

win = mlx.mlx_new_window(ctx, win_w, win_h, "Maze")


pattern_img_result = mlx.mlx_xpm_file_to_image(ctx, "notgrey.xpm")
pattern_img = pattern_img_result[0] 
pattern_width = pattern_img_result[1] 
pattern_height = pattern_img_result[2]


img = mlx.mlx_new_image(ctx, win_w, win_h)
result = mlx.mlx_get_data_addr(img)
data = result[0]
size_line = result[2]
image1 = ""
image2 = ""

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
    for _ in range(10):
        if animation_index < maze.width * maze.height:
            x = animation_index % maze.width
            y = animation_index // maze.width

            cell = maze.grid[y][x]
            px = x * CELL
            py = y * CELL
            n = 2
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
                for ny in range(CELL + 2):
                    for nx in range(CELL + 2):
                        put_pixel(px + nx, py + ny, 0xFFFFFF)

            mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)
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

    for y in range(3, CELL - 3):
        for x in range(3, CELL - 3):
            put_pixel(ex + x, ey + y, 0x00FF00)

    for y in range(3, CELL - 3):
        for x in range(3, CELL - 3):
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

    # if show_path:
    #     draw_path(path, path_color)
        
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            if cell.is_pattern:
                px = x * CELL
                py = y * CELL
                mlx.mlx_put_image_to_window(ctx, win, pattern_img, px, py)

def draw_path(path, color):

    for x, y in path:
        px = x * CELL
        py = y * CELL
        for dy in range(32, CELL - 32):
            for dx in range(1, CELL - 1):
                put_pixel(px + dx, py + dy, color)


colors = [0xFFFFFF, 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF]
saved = random.choice(colors)

path_color = colors[0]

draw_maze(saved, maze, path)

is_animating = True
animation_index = 0
show_path = False
is_animating_path = False
path_animation_index = 2

# draw_maze(saved, maze)
i = 0
def on_key(keycode, _):
    global saved
    global path
    global maze, i
    if keycode == 65307:
        mlx.mlx_loop_exit(ctx)
    
    elif keycode == 99:
        saved = colors[i % len(colors)]
        draw_maze(saved, maze, path)
        i += 1


    elif keycode == 115:
        global show_path, is_animating_path, path_animation_index

        if is_animating_path:
            return
        
        if not show_path:
            path_animation_index = 1
            is_animating_path = True
            show_path = True
        else:
            clear(0x000000)
            draw_maze(saved, maze, path)
            show_path = False

    elif keycode == 103:

        if is_animating_path:
            return
        
        global is_animating, animation_index
        maze = gen.generate(configs.entry, configs.exit, configs.perfect)
        path = DFS_algo(maze, configs.entry, configs.exit)
        show_path = False
        clear(0x000000)
        draw_maze(saved, maze, path)
        animation_index = 0
        is_animating = True

def animation_loop(_):
    animate_maze(_)
    animate_path(_)
    darw_pattern(_)
    return 0


mlx.mlx_loop_hook(ctx, animation_loop, None)
mlx.mlx_key_hook(win, on_key, None)
mlx.mlx_loop(ctx)