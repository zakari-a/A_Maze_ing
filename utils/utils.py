from typing import List, Tuple


def write_to_file(hex_list: List[List[str]], path: List[str],
                  entry: Tuple[int, int], exit: Tuple[int, int]) -> None:
    """
    Writes the maze data, entry and exit points,
    and the path to the output file.
    """
    x1, y1 = entry
    x2, y2 = exit
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
            file.write(digit)
