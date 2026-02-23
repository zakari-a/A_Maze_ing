from maze_generator.generator import MazeGenerator, Cell
import random
from typing import Any, List, Tuple
from utils.utils import write_to_file
from rendering.render_helpers import neighbors_cells, pattern_coords
import sys


try:
    from mlx import Mlx
except Exception:
    print("Error can't the find the MLX module try using "
          "make install")
    sys.exit(1)


def maze_animation(maze: MazeGenerator) -> None:
    """Animate the maze generation and solving process."""
    CELL = 32

    # Initializing Mlx window
    mlx: Any = Mlx()
    ctx: Any = mlx.mlx_init()
    win_w: int = maze.width * CELL
    win_h: int = maze.height * CELL
    if maze.width >= 25:
        win: Any = mlx.mlx_new_window(ctx, win_w, win_h + 40, "Maze")
    else:
        win = mlx.mlx_new_window(ctx, win_w, win_h, "Maze")

    # Creating blanck image for the window
    img: Any = mlx.mlx_new_image(ctx, win_w, win_h)
    result: Tuple[Any, int, int, int] = mlx.mlx_get_data_addr(img)
    data: bytearray = result[0]
    size_line: int = result[2]

    # Initializing 42 asset
    pattern_img_result: Tuple[Any, int, int] = mlx.mlx_xpm_file_to_image(
                                                ctx,
                                                "notgrey.xpm")
    pattern_img: Any = pattern_img_result[0]
    if pattern_img is None:
        print("Cant't find 'notgrey.xpm' image")
        sys.exit(1)

    pattern_width: int = pattern_img_result[1]
    pattern_height: int = pattern_img_result[2]

    def put_pixel(x: int, y: int, color: int) -> None:
        """Put a pixel of color at (x, y) in the image."""
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
        """Draw a horizontal line from (x1, y) to (x2, y) with color."""
        for x in range(x1, x2):
            put_pixel(x, y, color)

    def vline(x: int, y1: int, y2: int, color: int) -> None:
        """Draw a vertical line from (x, y1) to (x, y2) with color."""
        for y in range(y1, y2):
            put_pixel(x, y, color)

    def clear(color: int = 0x000000) -> None:
        """Clear the image with a specific color."""
        for y in range(win_h):
            for x in range(win_w):
                put_pixel(x, y, color)

    # Maze animation variables
    maze_index: int = 0
    maze_animating: bool = True
    cells: List[List[Tuple[int, int]]] = neighbors_cells(
                                        maze.width // 2, maze.height // 2,
                                        maze.width, maze.height)

    # 42 animation variables
    is_animating: bool = True
    animation_index: int = 0

    # Path animation variables
    is_animating_path: bool = False
    path_animation_index: int = 0
    path_flag: bool = True
    show_path: bool = False

    # Exit animation variables
    exit_index: int = 0
    exit_animating: bool = False
    cells2: List[List[Tuple[int, int]]] = neighbors_cells(
                                        maze.width - 1, maze.height - 1,
                                        maze.width, maze.height)

    def animate_maze(_: None) -> int:
        """
        Animate the maze generation by drawing
        walls and entry/exit points.
        """
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
            mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)

        return 0

    def animate_pattern(_: Any) -> int:
        """Animate the Pattern 42 by drawing its coordinates."""
        nonlocal is_animating, animation_index

        if not is_animating:
            return 0

        patt: List[Tuple[int, int]] = pattern_coords(maze)
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
                animation_index += 1
            else:
                is_animating = False
                break

        return 0

    def animate_path(_: None) -> int:
        """Animate the path by drawing it step by step."""
        nonlocal is_animating_path, path_animation_index

        if not is_animating_path:
            return 0
        if path_animation_index < len(maze.path) - 2:
            x1, y1 = maze.path[path_animation_index + 1]
            px: int = x1 * CELL
            py: int = y1 * CELL
            for dy in range(8, CELL - 8):
                for dx in range(8, CELL - 8):
                    put_pixel(px + dx, py + dy, 0xFFFFFF)

            if path_animation_index < len(maze.path):
                x2, y2 = maze.path[path_animation_index]
                c1_x: int = x1 * CELL + CELL // 2
                c1_y: int = y1 * CELL + CELL // 2
                c2_x: int = x2 * CELL + CELL // 2
                c2_y: int = y2 * CELL + CELL // 2

                if c1_x == c2_x:
                    start_x: int = x1 * CELL + 8
                    end_x: int = x1 * CELL + CELL - 8

                    start_y: int = min(y1 * CELL + 8, y2 * CELL + 8)
                    end_y: int = max(y1 * CELL + CELL - 8,
                                     y2 * CELL + CELL - 8)
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

    def exit_animation(_: None) -> int:
        """Animate the exit by drawing it step by step."""
        nonlocal exit_index, exit_animating

        if not exit_animating:
            return 0

        if exit_index < len(cells2):
            c: List[Tuple[int, int]] = cells2[exit_index]
            for k in c:
                x, y = k
                x *= CELL
                y *= CELL
                for ny in range(CELL + 1):
                    for nx in range(CELL + 1):
                        put_pixel(nx + x, ny + y, 0x000000)
            mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)
            exit_index += 1
        else:
            exit_animating = False
            ex, ey = maze.path[0]
            ox, oy = maze.path[-1]
            ex *= CELL
            ey *= CELL
            ox *= CELL
            oy *= CELL

            for y in range(CELL):
                for x in range(CELL):
                    put_pixel(ex + x, ey + y, 0x000000)
            for y in range(CELL):
                for x in range(CELL):
                    put_pixel(ox + x, oy + y, 0x000000)
            mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)
            mlx.mlx_loop_exit(ctx)

        return 0

    def draw_pattern(_: None) -> None:
        """Draw the Pattern 42 in the maze."""
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
        """Draw the maze with walls and entry/exit points."""
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
        """Draw the path in the maze."""
        for x, y in path[1:len(path) - 1]:
            px: int = x * CELL
            py: int = y * CELL
            for dy in range(14, CELL - 14):
                for dx in range(14, CELL - 14):
                    put_pixel(px + dx, py + dy, color)
        mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)

    def print_keys(keys: List[str]) -> None:
        """Print the available keys and their actions."""
        y: int = win_h + 10
        x: int = int(win_w // maze.width)
        for key in keys:
            mlx.mlx_string_put(ctx, win, x, y, 0xFFFFFF, key)
            if key == keys[3]:
                x += 190
            else:
                x += 120

    # Colors and strings for the keys
    colors: List[int] = [0xFFFFFF, 0xFF0000, 0x00FF00, 0x0000FF,
                         0xFFFF00, 0x00FFFF, 0xFF00FF]
    strings: List[str] = ["1: algo1", "2: algo2", "3: Path",
                          "4: PT-animation", "5: Color", "6: Quit"]
    saved: int = random.choice(colors)

    # Clear the image and set the initial color
    clear(0x000000)
    cleared_buffer: bytes = bytes(data)

    if maze.width >= 25:
        print_keys(strings)

    index: int = 0

    def on_key(keycode: int, _: None) -> None:
        """Handle key events for the maze animation."""
        nonlocal saved, index, path_flag
        nonlocal maze_index, maze_animating, exit_animating
        nonlocal is_animating, animation_index, is_animating_path

        if keycode == 54:
            if is_animating:
                return
            exit_animating = True
            mlx.mlx_loop_hook(ctx, exit_animation, None)

        elif keycode == 53:
            if maze_animating or exit_animating:
                return
            saved = colors[index % len(colors)]
            draw_maze(saved, maze, maze.path)
            index += 1
            animation_index = 0
            is_animating = True

        elif keycode == 52:
            nonlocal show_path, is_animating_path, path_animation_index
            if is_animating_path or is_animating or exit_animating:
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
                path_flag = True

        elif keycode == 49:
            if is_animating_path or is_animating or exit_animating:
                return

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

        elif keycode == 51:
            if is_animating_path or exit_animating:
                return

            if path_flag:
                draw_path(maze.path)
                path_flag = False

            else:
                data[:] = cleared_buffer
                draw_maze(saved, maze, maze.path)
                path_flag = True
                animation_index = 0
                is_animating = True
                show_path = False

        elif keycode == 50:
            if is_animating_path or is_animating or exit_animating:
                return

            maze.generate2()
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

    def animation_loop(_: None) -> int:
        """Main animation loop to handle maze and pattern animations."""
        animate_maze(_)
        if not maze_animating:
            animate_pattern(_)
        animate_path(_)
        draw_pattern(_)
        return 0

    # Setting up the hooks for the Mlx context
    mlx.mlx_loop_hook(ctx, animation_loop, None)
    mlx.mlx_key_hook(win, on_key, None)
    mlx.mlx_loop(ctx)
