from mlx import Mlx
from generator import MazeGenerator, Cell
import random
from typing import Any, List, Tuple, Set
from utils.utils import write_to_file


def maze_animation(maze: MazeGenerator) -> None:

    maze.generate()
    maze.solve()
    CELL = 32

    Mlxany: Any = Mlx
    mlx: Any = Mlxany()
    ctx: Any = mlx.mlx_init()
    win_w: int = maze.width * CELL
    win_h: int = maze.height * CELL
    win: Any = mlx.mlx_new_window(ctx, win_w, win_h + 40, "Maze")


    pattern_img_result: Tuple[Any, int, int] = mlx.mlx_xpm_file_to_image(ctx, "./utils/notgrey.xpm")
    pattern_img: Any = pattern_img_result[0]
    pattern_width: int = pattern_img_result[1]
    pattern_height: int = pattern_img_result[2]


    img: Any = mlx.mlx_new_image(ctx, win_w, win_h)
    result: Tuple[Any, int, int, int] = mlx.mlx_get_data_addr(img)
    data: bytearray = result[0]
    size_line: int = result[2]


    def put_pixel(x: int, y: int, color: int) -> None:
        if 0 <= x < win_w and 0 <= y < win_h:
            off: int = y * size_line + x * 4
            r: int = (color >> 16) & 0xFF
            g: int = (color >> 8) & 0xFF
            b: int = color & 0xFF
            data[off] = b
            data[off + 1] = g
            data[off + 2] = r
            data[off + 3] = 255


    def hline(x1: int, x2: int, y: int, color: int) -> None:
        for x in range(x1, x2):
            put_pixel(x, y, color)


    def vline(x: int, y1: int, y2: int, color: int) -> None:
        for y in range(y1, y2):
            put_pixel(x, y, color)


    def clear(color: int = 0x000000) -> None:
        for y in range(win_h):
            for x in range(win_w):
                put_pixel(x, y, color)

    def in_bounds(x:int, y:int) -> bool:
        return True if 0 <= x < maze.width and 0 <= y < maze.height else False

    def neighbors(x: int, y: int) -> List[Tuple[int, int]]:
        cells: List[Tuple[int, int]] = []
        if in_bounds(x, y-1):
            cells.append((x, y-1))
        if in_bounds(x+1, y):
            cells.append((x+1, y))
        if in_bounds(x, y+1):
            cells.append((x, y+1))
        if in_bounds(x-1, y):
            cells.append((x-1, y))
        return cells


    def neighbors_cells(maze: MazeGenerator) -> List[List[Tuple[int, int]]]:
        visited: Set[Tuple[int, int]] = set()
        x: int = maze.width // 2
        y: int = maze.height // 2
        visited.add((x, y))
        cells: List[List[Tuple[int, int]]] = []
        cells.append([(x, y)])
        cells.append(neighbors(x, y))
        for n in cells[1]:
            visited.add(n)
        i: int = 1
        while cells[i] and i < len(cells):
            cell: List[Tuple[int, int]] = []
            for n in cells[i]:
                neigh: List[Tuple[int, int]] = neighbors(n[0], n[1])
                for k in neigh:
                    if k not in visited:
                        cell.append(k)
                        visited.add(k)
            cells.append(cell)
            i += 1
        return cells


    maze_index: int = 0
    maze_animating: bool = True
    cells: List[List[Tuple[int, int]]] = neighbors_cells(maze)
    is_animating: bool = False
    animation_index: int = 0
    is_animating_path: bool = False
    path_animation_index: int = 0
    path_flag: bool = False
    show_path: bool = False


    def animate_maze(_: None) -> int:
        nonlocal maze_index, maze_animating

        if not maze_animating:
            return 0

        if maze_index < len(cells):
            c: List[Tuple[int, int]] = cells[maze_index]
            for k in c:
                x: int
                y: int
                x, y = k
                cell: Cell = maze.grid[y][x]
                x *= CELL
                y *= CELL
                n: int = 2
                if cell.north:
                    for i in range(n + 1):
                        hline(x - n, x + CELL + n, y + i, saved)
                if cell.south:
                    for i in range(n + 1):
                        hline(x - n, x + CELL + n, y + CELL - i, saved)

                if cell.west:
                    for i in range(n):
                        vline(x + i, y - n, y + CELL, saved)

                if cell.east:
                    for i in range(n + 1):
                        vline(x + CELL - i, y - n, y + CELL, saved)
            mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)
            maze_index += 1
        else:
            maze_animating = False
            ex: int
            ey: int
            ox: int
            oy: int
            ex, ey = maze.path[0]
            ox, oy = maze.path[-1]
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


    def animate_pattern(_: Any) -> int:
        nonlocal is_animating, animation_index

        if not is_animating:
            return 0

        patt: List[Tuple[int, int]] = pattern_coords(maze)
        for _ in range(1):
            if animation_index < len(patt):
                x: int
                y: int
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
                animation_index += 1
            else:
                is_animating = False
                break

        return 0


    def animate_path(_: None) -> int:
        nonlocal is_animating_path, path_animation_index

        if not is_animating_path:
            return 0
        if path_animation_index < len(maze.path) - 2:
            x1: int
            y1: int
            x1, y1 = maze.path[path_animation_index + 1]
            px: int = x1 * CELL
            py: int = y1 * CELL
            for dy in range(8, CELL - 8):
                for dx in range(8, CELL - 8):
                    put_pixel(px + dx, py + dy, 0xFFFFFF)

            if path_animation_index < len(maze.path):
                x2: int
                y2: int
                x2, y2 = maze.path[path_animation_index]
                c1_x: int = x1 * CELL + CELL // 2
                c1_y: int = y1 * CELL + CELL // 2
                c2_x: int = x2 * CELL + CELL // 2
                c2_y: int = y2 * CELL + CELL // 2

                if c1_x == c2_x:
                    start_x: int = x1 * CELL + 8
                    end_x: int = x1 * CELL + CELL - 8

                    start_y: int = min(y1 * CELL + 8, y2 * CELL + 8)
                    end_y: int = max(y1 * CELL + CELL - 8, y2 * CELL + CELL - 8)
                    for y in range(start_y, end_y):
                        for x in range(start_x, end_x):
                            put_pixel(x, y, 0xFFFFFF)

                elif c1_y == c2_y:
                    start_y = y1 * CELL + 8
                    end_y = y1 * CELL + CELL - 8

                    start_x = min(x1 * CELL + 8, x2 * CELL + 8)
                    end_x = max(x1 * CELL + CELL - 8, x2 * CELL + CELL - 8)
                    for y in range(start_y, end_y):
                        for x in range(start_x, end_x):
                            put_pixel(x, y, 0xFFFFFF)

            mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)
            path_animation_index += 1

        else:
            is_animating_path = False
        return 0


    def pattern_coords(_: None) -> List[Tuple[int, int]]:
        patt: List[Tuple[int, int]] = []
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.grid[y][x].is_pattern:
                    patt.append((x, y))

        return patt


    def darw_pattern(_: None) -> None:
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.grid[y][x].is_pattern:
                    px: int = x * CELL
                    py: int = y * CELL
                    offset_x: int = (CELL - pattern_width) // 2
                    offset_y: int = (CELL - pattern_height) // 2
                    mlx.mlx_put_image_to_window(
                        ctx, win,
                        pattern_img, px + offset_x, py + offset_y
                        )


    def draw_maze(wall_color: int, maze: MazeGenerator,
                  path: List[Tuple[int, int]]) -> None:
        ex: int
        ey: int
        ox: int
        oy: int

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
                if cell.north:
                    for i in range(n + 1):
                        hline(px - n, px + CELL + n, py + i, wall_color)
                if cell.south:
                    for i in range(n + 1):
                        hline(px - n, px + CELL + n, py + CELL - i, wall_color)

                if cell.west:
                    for i in range(n):
                        vline(px + i, py - n, py + CELL, wall_color)

                if cell.east:
                    for i in range(n + 1):
                        vline(px + CELL - i, py - n, py + CELL, wall_color)

        mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)


    def draw_path(path: List[Tuple[int, int]], color: int = 0xFFFFFF) -> None:
        for x, y in path[1:len(path) - 1]:
            px: int = x * CELL
            py: int = y * CELL
            for dy in range(14, CELL - 14):
                for dx in range(14, CELL - 14):
                    put_pixel(px + dx, py + dy, color)
        mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)


    def print_keys(keys: List[str]) -> None:
        y: int = win_h + 10
        x: int = int(win_w // maze.width)
        for key in keys:
            mlx.mlx_string_put(ctx, win, x, y, 0xFFFFFF, key)
            if key == keys[2]:
                x += 215
            else:
                x += 130


    colors: List[int] = [0xFFFFFF, 0xFF0000, 0x00FF00, 0x0000FF,
                         0xFFFF00, 0x00FFFF, 0xFF00FF]
    strings: List[str] = ["1: Regen", "2: Path", "3: Path animation",
                          "4: Color", "5: Quit"]
    saved: int = random.choice(colors)

    clear(0x000000)
    cleared_buffer: bytes = bytes(data)

    is_animating = True
    animation_index = 0
    if maze.width >= 25:
        print_keys(strings)
    path_flag = True
    show_path = False
    path_animation_index = 1

    index: int = 0

    def on_key(keycode: int, _: None) -> None:
        nonlocal saved, index
        nonlocal maze, maze_index, maze_animating
        nonlocal is_animating, animation_index, is_animating_path

        if keycode == 53:
            mlx.mlx_loop_exit(ctx)

        elif keycode == 52:
            if maze_animating:
                return
            saved = colors[index % len(colors)]
            draw_maze(saved, maze, maze.path)
            index += 1
            animation_index = 0
            is_animating = True

        elif keycode == 51:
            nonlocal show_path, is_animating_path, path_animation_index
            if is_animating_path or is_animating:
                return

            if not show_path:
                path_animation_index = 1
                is_animating_path = True
                show_path = True
            else:
                data[:] = cleared_buffer
                draw_maze(saved, maze, maze.path)
                show_path = False
                animation_index = 0
                is_animating = True

        elif keycode == 49:

            if is_animating_path or is_animating:
                return
            # maze.grid = maze._grid_generator()
            maze.generate()
            maze.solve()
            hex_list = maze.get_hex_grid()
            path_directions = maze.solve()
            write_to_file(hex_list, path_directions, maze.entry, maze.exit_p)
            show_path = False
            data[:] = cleared_buffer
            maze_animating = True
            maze_index = 0
            animation_index = 0
            is_animating = True

        elif keycode == 50:
            if is_animating_path:
                return

            nonlocal path_flag
            if path_flag:
                draw_path(maze.path)
                path_flag = False
            else:
                data[:] = cleared_buffer
                draw_maze(saved, maze, maze.path)
                path_flag = True
                animation_index = 0
                is_animating = True


    def animation_loop(_: None) -> int:
        animate_maze(_)
        if not maze_animating:
            animate_pattern(_)
        animate_path(_)
        darw_pattern(_)
        return 0


    mlx.mlx_loop_hook(ctx, animation_loop, None)
    mlx.mlx_key_hook(win, on_key, None)
    mlx.mlx_loop(ctx)
