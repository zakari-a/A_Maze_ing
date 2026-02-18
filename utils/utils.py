from typing import List, Tuple
from config_parser import Config

def write_to_file(hex_list:List[List[str]], path:List[str],
                  entry:Tuple[int, int], exit: Tuple[int, int]) -> None:
    x1, y1 = entry
    x2, y2 = exit
    # print(path)
    with open("maze.txt", "w") as file:
        for row in hex_list:
            for data in row:
                file.write(data)
            file.write('\n')
        file.write('\n')  
        file.write(f"{x1},{y1}")
        file.write('\n')
        file.write(f"{x2},{y2}")
        file.write('\n')
        for digit in path:
            # print("d5l lpath")
            file.write(digit)