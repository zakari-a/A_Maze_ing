import sys
import os
from parsing.errors import MazeError
from parsing.config_parser import final_parse
from maze_generator.generator import MazeGenerator
from rendering.render import maze_animation
from utils.utils import write_to_file


def main() -> None:
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if os.path.exists(filename):
            try:
                data = final_parse(filename)
            except MazeError as e:
                print(e)
                sys.exit(1)
        else:
            print(f"Error: I can't find the file '{filename}'."
                  "Check your spelling!")
            sys.exit(1)

        gen = MazeGenerator(data.width, data.height, data.entry,
                            data.exit, data.output_file, data.perfect)

    else:
        print("Can't find the config.txt file. Please provide "
              "a valid config file")
        sys.exit(1)
    try:
        gen.generate()
        hex_list = gen.get_hex_grid()
        path_directions = gen.solve()
        write_to_file(hex_list, path_directions, gen.entry, gen.exit_p)
        maze_animation(gen)
    except MazeError as e:
        print(e)
        sys.exit(1)


main()
