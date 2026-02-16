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
            # cell = maze.grid[y][x]
            # n = 2
            # if cell.N:
            #     for i in range(n + 1):
            #         hline(px - n , px + CELL + n, py + i, saved)
            # if cell.S:
            #     for i in range(n + 1):
            #         hline(px - n, px + CELL + n, py + CELL - i, saved)

            # if cell.W:
            #     for i in range(n):
            #         vline(px + i, py - n, py + CELL, saved)

            # if cell.E:
            #     for i in range(n + 1):
            #         vline(px + CELL - i, py - n, py + CELL, saved)
            for ny in range(-1, CELL + 2):
                for nx in range(-1, CELL + 2):
                    if saved == 0xFFFFFF:
                        put_pixel(x + nx, y + ny, 0x000000)
                    else:
                        put_pixel(x + nx, y + ny, 0xFFFFFF)
            time.sleep(0.01)
            mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)
            animation_index += 1
        else:
            is_animating = False
            break
            
    return 0


def animate_path(pl_coords, ppl_coords):

    x1, y1 = ppl_coords
    px = x1 * CELL
    py = y1 * CELL
    for dy in range(8, CELL - 8):
        for dx in range(8, CELL - 8):
            put_pixel(px + dx, py + dy, path_color)
    # x2, y2 = ppl_coords
    # c1_x = x1 * CELL + CELL // 2
    # c1_y = y1 * CELL + CELL // 2
    # c2_x = x2 * CELL + CELL // 2
    # c2_y = y2 * CELL + CELL // 2

    # if c1_x == c2_x:
    #     start_x = x1 * CELL + 8
    #     end_x = x1 * CELL + CELL - 8

    #     start_y = min(y1 * CELL + 8, y2 * CELL + 8)
    #     end_y = max(y1 * CELL + CELL - 8, y2 * CELL + CELL - 8)
    #     for y in range(start_y, end_y):
    #         for x in range(start_x, end_x):
    #             put_pixel(x, y, 0xFF0000)

    # elif c1_y == c2_y:
    #     start_y = y1 * CELL + 8
    #     end_y = y1 * CELL + CELL - 8

    #     start_x = min(x1 * CELL + 8, x2 * CELL + 8)
    #     end_x = max(x1 * CELL + CELL - 8, x2 * CELL + CELL - 8)
    #     for y in range(start_y, end_y):
    #         for x in range(start_x, end_x):
    #                 put_pixel(x, y, 0x000000)

    mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)


    x1, y1 = pl_coords
    px = x1 * CELL
    py = y1 * CELL
    for dy in range(8, CELL - 8):
        for dx in range(8, CELL - 8):
            put_pixel(px + dx, py + dy, path_color)

    x2, y2 = ppl_coords
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


colors = [0xFFFFFF, 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF]
saved = random.choice(colors)

path_color = colors[0]
clear(0x000000)
cleared_buffer = bytes(data)
draw_maze(saved, maze, path)

player_x, player_y = path[1]
prev_coords = path[0]
is_animating = True
animation_index = 0

p = True

show_path = False    # elif keycode == 115:
    #     global show_path, is_animating_path, path_animation_index
    #     if is_animating_path:
    #         return
        
    #     if not show_path:
    #         path_animation_index = 1
    #         is_animating_path = True
    #         show_path = True
    #     else:
    #         data[:] = cleared_buffer
    #         draw_maze(saved, maze, path)
    #         show_path = False
    #         animation_index = 0
    #         is_animating = True
is_animating_path = False
path_animation_index = 2

i = 0
def on_key(keycode, _):
    global saved
    global path
    global maze, i
    global is_animating, animation_index
    global player_x, player_y, prev_coords
    if keycode == 65307:
        mlx.mlx_loop_exit(ctx)
    
    elif keycode == 99:
        saved = colors[i % len(colors)]
        draw_maze(saved, maze, path)
        i += 1
        animation_index = 0
        is_animating = True


    # elif keycode == 115:
    #     global show_path, is_animating_path, path_animation_index
    #     if is_animating_path:
    #         return
        
    #     if not show_path:
    #         path_animation_index = 1
    #         is_animating_path = True
    #         show_path = True
    #     else:
    #         data[:] = cleared_buffer
    #         draw_maze(saved, maze, path)
    #         show_path = False
    #         animation_index = 0
    #         is_animating = True

    elif keycode == 103:

        if is_animating_path:
            return
        
        maze = gen.generate(configs.entry, configs.exit, configs.perfect)
        path = DFS_algo(maze, configs.entry, configs.exit)
        show_path = False
        data[:] = cleared_buffer
        draw_maze(saved, maze, path)
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
            
    elif keycode == 65362:
        if not maze.grid[player_y][player_x].N:
            prev_coords = ((player_x, player_y))
            player_y -= 1
            animate_path((player_x, player_y), prev_coords)
        else:
            return
    elif keycode == 65364:
        if not maze.grid[player_y][player_x].S:
            prev_coords = ((player_x, player_y))
            player_y += 1
            animate_path((player_x, player_y), prev_coords)
        else:
            return
    elif keycode == 65361:
        if not maze.grid[player_y][player_x].W:
            prev_coords = ((player_x, player_y))
            player_x -= 1
            animate_path((player_x, player_y), prev_coords)
        else:
            return
    elif keycode == 65363:
        if not maze.grid[player_y][player_x].E:
            prev_coords = ((player_x, player_y))
            player_x += 1
            animate_path((player_x, player_y), prev_coords)
        else:
            return

def animation_loop(_):
    animate_pattern(_)
    darw_pattern(_)
    return 0

mlx.mlx_loop_hook(ctx, animation_loop, None)
mlx.mlx_key_hook(win, on_key, None)
mlx.mlx_loop(ctx)