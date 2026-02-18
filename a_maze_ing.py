import sys
import os
from config_parser import final_parse, Config
from generator import MazeGenerator
from typing import List
from animation import maze_animation


def main() -> None:
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if os.path.exists(filename):
            data = final_parse(filename)
        else:
            print(f"Error: I can't find the file '{filename}'."
                  "Check your spelling!")
            sys.exit(0)
    gen = MazeGenerator(data.width, data.height, data.entry,
                                  data.exit, data.output_file, data.perfect)
    
    maze_animation(gen)
    # hex_list = gen.get_hex_grid()
    # path_directions = gen.solve()
    # write_to_file(hex_list, path_directions, data)
    
main()